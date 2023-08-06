#!/usr/bin/env python3
#
# coding: utf-8

# Copyright (c) 2019-2020, NVIDIA CORPORATION.  All Rights Reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

"""
handles image UI operations
"""

import time
import threading
import logging

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

log = logging.getLogger("image_ui")


class ImageUIAction:
    """handle UI actions on images, e.g. delete, pull.."""

    def __init__(self, itvfs, rt_window, runtime, conf):
        # rt_window
        self.images_tvfs = itvfs
        self.rt_window = rt_window
        # local runtime
        self.runtime = runtime
        self.config = conf

    # we will need some handle of the current row
    def do(
        self,
        func,
        local_image,
        tag,
        initial_prompt,
        spinner_title,
        error_header,
        error_detail,
        post_func_sleep,
        path,
    ):
        """calls to perform various functions on images (e.g. delete) come here
        returns True if the user chose to perform the action and False otherwise
        Note that this function is partially async and it may fail in the async part
        the return code will not capture that
        """

        diag = Gtk.MessageDialog(
            parent=self.rt_window,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=initial_prompt,
        )
        ret_c = diag.run()
        diag.destroy()
        if ret_c == Gtk.ResponseType.CANCEL:
            return False

        log.debug("image id: %s, action: %s", local_image["id"], spinner_title)
        spinner_diag = Gtk.MessageDialog(
            parent=self.rt_window,
            message_type=Gtk.MessageType.OTHER,
            text=spinner_title,
        )
        spinner = Gtk.Spinner()
        spinner.show()
        spinner.start()
        spinner_diag.get_message_area().add(spinner)
        spinner_diag.show()
        thread = threading.Thread(
            target=self.async_rt_call,
            args=(
                func,
                local_image,
                tag,
                spinner_diag,
                error_header,
                error_detail,
                post_func_sleep,
                path,
            ),
        )
        thread.daemon = True
        thread.start()

        return True

    def async_rt_call(
        self,
        func,
        local_image,
        tag,
        spinner_diag,
        error_header,
        error_detail,
        post_func_sleep,
        path,
    ):
        """async wrapper around runtime calls that are not instantaneous"""
        # this needs to just call action
        # ret_c = self.runtime.uncache_menu_item_tag(local_image["id"], tag["tag"])
        ret_c = func(local_image["id"], tag["tag"])
        if post_func_sleep > 0:
            log.debug("async_rt_call post_func_sleep: %s", str(post_func_sleep))
            time.sleep(post_func_sleep)
        # we need to remove the spinner widget now
        # doing this without glib will result in a coredump :)
        GLib.idle_add(
            self.async_glib,
            local_image,
            tag,
            spinner_diag,
            ret_c,
            error_header,
            error_detail,
            path,
        )

    def async_glib(
        self, local_image, tag, spinner_diag, ret_c, error_header, error_detail, path
    ):
        """async wrapper around glib sensitive parts"""
        spinner_diag.destroy()
        if not ret_c:
            diag = Gtk.MessageDialog(
                parent=self.rt_window,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=error_header,
            )
            diag.format_secondary_markup(error_detail)
            diag.run()
            diag.destroy()
            return
        # log.debug("async gtk happy! path: %s", path)

        # this will take care of the UI update, there is no need to update it separately
        if path is not None:
            # need to update the row here..
            updated_mi = self.runtime.get_menu_item(local_image["id"])
            updated_tag = updated_mi["tags"][tag["tag"]]
            self.images_tvfs.update_row(updated_mi, updated_tag, path)
        else:
            # the path is none. presumably because it didn't exist at the time of the call.
            # let's refresh the liststore and try to look for it.
            self.images_tvfs.rt_window.refresh_local_images(None, None)
            # print(local_image["name"])
            # print(tag["tag"])
            i = 0
            for row in self.images_tvfs.liststore:
                # print(row[0] + " " + row[1])
                if row[0] == local_image["name"] and row[1] == tag["tag"]:
                    path = i
                    break
                i = i + 1

            if path is None:
                log.warning(
                    "for some reason unable to find a matching row in treeview STILL"
                )
            else:
                # self.images_tvfs.update_row(updated_mi, updated_tag, path)
                ite = self.images_tvfs.treeview.get_model().get_iter(path)
                # select the row
                selection = self.images_tvfs.treeview.get_selection()
                selection.select_iter(ite)
                self.images_tvfs.rt_window.stack.set_visible_child_name("Local Images")
                # the images tab is the third from the bottom
                ind_run_tab = len(self.rt_window.main_listbox.get_children()) - 3
                self.rt_window.main_listbox.select_row(
                    self.rt_window.main_listbox.get_row_at_index(ind_run_tab)
                )

    #    def update_row_glib(self, local_image, tag, path):
    #        """scheduled via glib, therefore safe"""
    #        print("glib before update row")
    #        self.images_tvfs.update_row(local_image, tag, path)
    #        print("glib after update row")

    def do_log(self, local_image, tag, path):
        """this is executed on click, so there should be no need for Glib calls"""
        img_name = local_image["image"] + ":" + tag["tag"]
        # if we got here, we were in status pulling when the button was shown to the user
        # but, is the GUI stale at this point?
        new_status = self.runtime.get_ephem_img_status(img_name)
        if new_status != "pulling":
            # the image status changed from under us.. don't make a fuss,
            # just refresh the row and exit
            updated_mi = self.runtime.get_menu_item(local_image["id"])
            updated_tag = updated_mi["tags"][tag["tag"]]
            # GLib.idle_add(self.update_row_glib, updated_mi, updated_tag, path)
            self.images_tvfs.update_row(updated_mi, updated_tag, path)
            return

        out_diag = Gtk.Dialog(
            title="image build output", transient_for=self.rt_window, modal=False
        )
        out_diag.set_size_request(350, 150)
        out_diag.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        ca = out_diag.get_content_area()
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_border_width(10)
        frame = Gtk.Frame()
        vbox.add(frame)
        ca.add(vbox)

        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        frame.add(sw)

        textview = Gtk.TextView()
        textview.set_editable(False)
        textview.set_left_margin(10)
        textview.set_top_margin(10)
        sw.add(textview)

        out_diag.show_all()
        self.runtime.attach_widget_menu_item_tag_caching(textview, local_image, tag)
        out_diag.run()
        # print("after run")
        self.runtime.remove_widget_menu_item_tag_caching(local_image, tag)
        # print("after removed widget")

        new_new_status = self.runtime.get_ephem_img_status(img_name)
        # print("after got status")
        if new_status != new_new_status:
            # the status has changed.  Neeed to update the GUI
            # print("status changed")
            updated_mi = self.runtime.get_menu_item(local_image["id"])
            # print("after  get menu item")
            updated_tag = updated_mi["tags"][tag["tag"]]
            # print("got the updated tag")
            self.images_tvfs.update_row(updated_mi, updated_tag, path)
            # GLib.idle_add(self.update_row_glib, updated_mi, updated_tag, path)

        # print("before diag destroy")
        out_diag.destroy()
        # print("after diag destroy")
