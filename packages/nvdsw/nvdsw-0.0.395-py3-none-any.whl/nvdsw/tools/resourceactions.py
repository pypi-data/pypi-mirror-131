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
handles resource UI operations
"""

import time
import threading
import logging
import subprocess

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from nvdsw.tools.claunch import CLaunchDialog
from nvdsw.tools.rtlaunch import NVAIELaunchDialog

log = logging.getLogger("resource_ui")


class ResourceUIAction:
    """handle UI actions on resources, e.g. create, start, restart, delete.."""

    def __init__(self, rtvfs, rt_window, conf):
        # rt_window
        self.resources_tvfs = rtvfs
        self.rt_window = rt_window

        # self.runtime = runtime
        self.config = conf

    def do(
        self,
        runtime,
        func,
        local_resource,
        initial_prompt,
        spinner_title,
        error_header,
        error_detail,
        post_func_sleep,
        path,
    ):
        """calls to perform various functions on resources (e.g. delete) come here
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

        log.debug("resource id: %s, action: %s", local_resource["id"], spinner_title)
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
                runtime,
                func,
                local_resource,
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
        runtime,
        func,
        local_resource,
        spinner_diag,
        error_header,
        error_detail,
        post_func_sleep,
        path,
    ):
        """async wrapper around runtime calls that are not instantaneous"""
        # this needs to just call action
        # ret_c = self.runtime.uncache_menu_item_tag(local_image["id"], tag["tag"])
        ret_c = func(local_resource["id"])
        if post_func_sleep > 0:
            log.debug("async_rt_call post_func_sleep: %s", str(post_func_sleep))
            time.sleep(post_func_sleep)
        # we need to remove the spinner widget now
        # doing this without glib will result in a coredump :)
        GLib.idle_add(
            self.async_glib,
            runtime,
            local_resource,
            spinner_diag,
            ret_c,
            error_header,
            error_detail,
            path,
        )

    def async_glib(
        self,
        runtime,
        local_resource,
        spinner_diag,
        ret_c,
        error_header,
        error_detail,
        path,
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
            updated_res = runtime.get_resource(local_resource["id"])
            if updated_res is None:
                # the resource was deleted, so..
                self.resources_tvfs.remove_row(path)
            else:
                self.resources_tvfs.update_row(updated_res, path)
        else:
            # the path is none. presumably because it didn't exist at the time of the call.
            # let's refresh the liststore and try to look for it.
            self.resources_tvfs.rt_window.refresh_resources(None, None)
            i = 0
            for row in self.resources_tvfs.liststore:
                if row[0] == local_resource["name"]:
                    path = i
                    break
                i = i + 1

            if path is None:
                log.warning(
                    "for some reason unable to find a matching row in treeview STILL"
                )
            else:
                # self.images_tvfs.update_row(updated_mi, updated_tag, path)
                ite = self.resources_tvfs.treeview.get_model().get_iter(path)
                # select the row
                selection = self.resources_tvfs.treeview.get_selection()
                selection.select_iter(ite)
                self.resources_tvfs.rt_window.stack.set_visible_child_name("Running")
                # the Running tab is the second one from last
                ind_run_tab = len(self.rt_window.main_listbox.get_children()) - 2
                self.rt_window.main_listbox.select_row(
                    self.rt_window.main_listbox.get_row_at_index(ind_run_tab)
                )

    def open_url(self, url, _):
        cmd = ["/usr/bin/x-www-browser", url]
        subprocess.Popen(cmd)

    def create_local(
        self,
        runtime,
        menu_item,
        selected_tag,
        initial_prompt,
        spinner_title,
        error_header,
        error_detail,
        post_func_sleep,
    ):

        win = CLaunchDialog(
            parent=self.rt_window,
            title=initial_prompt,
            description=menu_item["description"],
            license_url=menu_item["license_url"],
            ports=menu_item["ports"],
            volumes=menu_item["volumes"],
            browser=menu_item["browser"],
            gpus=self.rt_window.gpus,
            icon_file=self.rt_window.icon_default,
            settings=self.rt_window.settings,
            selected_tag=selected_tag,
        )
        ret_c = win.run()
        if ret_c == Gtk.ResponseType.CANCEL:
            win.destroy()
            return False

        attrs = win.get_attrs().copy()
        win.destroy()

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
            target=self.async_rt_create_local,
            args=(
                runtime,
                menu_item,
                selected_tag["tag"],
                attrs,
                spinner_diag,
                error_header,
                error_detail,
                post_func_sleep,
            ),
        )
        thread.daemon = True
        thread.start()
        return True

    def async_rt_create_local(
        self,
        runtime,
        menu_item,
        selected_tag_id,
        attrs,
        spinner_diag,
        error_header,
        error_detail,
        post_func_sleep,
    ):
        """async wrapper around the runtime create call"""
        res_id = runtime.create_resource(
            menu_item["id"], flavor_id=None, tag=selected_tag_id, attrs=attrs
        )

        if post_func_sleep > 0:
            log.debug("async_rt_create post_func_sleep: %s", str(post_func_sleep))
            time.sleep(post_func_sleep)
        # we need to remove the spinner widget now
        # doing this without glib will result in a coredump :)
        GLib.idle_add(
            self.async_glib_create,
            runtime,
            res_id,
            spinner_diag,
            error_header,
            error_detail,
        )

    def async_glib_create(
        self, runtime, res_id, spinner_diag, error_header, error_detail
    ):
        """async wrapper around glib sensitive parts"""
        spinner_diag.destroy()
        if res_id is None:
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

        log.debug("created resource with id: %s", res_id)
        resource = runtime.get_resource(res_id)
        self.rt_window.stack.set_visible_child_name("Running")
        # The Running tab is the next to last one..
        ind_run_tab = len(self.rt_window.main_listbox.get_children()) - 2
        self.rt_window.main_listbox.select_row(
            self.rt_window.main_listbox.get_row_at_index(ind_run_tab)
        )
        resource_uid = None
        if resource["rtype"] == "local":
            resource_uid = resource["name"]
        elif resource["rtype"] == "remote":
            resource_uid = resource["id"]

        # let's refresh the liststore and try to look for the created entry
        path = None
        self.rt_window.refresh_resources(None, None)
        i = 0
        for row in self.resources_tvfs.liststore:
            if row[0] == resource_uid:
                path = i
                break
            i = i + 1

        if path is None:
            log.warning(
                "for some reason unable to find a matching row in treeview STILL"
            )
        else:
            # self.images_tvfs.update_row(updated_mi, updated_tag, path)
            ite = self.resources_tvfs.treeview.get_model().get_iter(path)
            # select the row
            selection = self.resources_tvfs.treeview.get_selection()
            selection.select_iter(ite)

    def create_nvaie(
        self,
        runtime,
        menu_item,
        flavors,
        preset_flavor,
        initial_prompt,
        spinner_title,
        error_header,
        error_detail,
        post_func_sleep,
    ):

        win = NVAIELaunchDialog(
            parent=self.rt_window,
            title=initial_prompt,
            menu_item=menu_item,
            flavors=flavors,
            preset_flavor=preset_flavor,
            icon_file=self.rt_window.icon_file,
        )

        ret_c = win.run()
        if ret_c == Gtk.ResponseType.CANCEL:
            win.destroy()
            return False

        selected_flavor_id = win.flavor_box.get_active_id()
        win.destroy()

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
            target=self.async_rt_create_nvaie,
            args=(
                runtime,
                menu_item,
                selected_flavor_id,
                spinner_diag,
                error_header,
                error_detail,
                post_func_sleep,
            ),
        )
        thread.daemon = True
        thread.start()
        return True

    def async_rt_create_nvaie(
        self,
        runtime,
        menu_item,
        selected_flavor_id,
        spinner_diag,
        error_header,
        error_detail,
        post_func_sleep,
    ):
        """async wrapper around the runtime create call"""
        res_id = runtime.create_resource(menu_item["id"], selected_flavor_id)
        log.debug("created resource with id: " + res_id)

        if post_func_sleep > 0:
            log.debug("async_rt_create_nvaie post_func_sleep: %s", str(post_func_sleep))
            time.sleep(post_func_sleep)
        # we need to remove the spinner widget now
        # doing this without glib will result in a coredump :)
        GLib.idle_add(
            self.async_glib_create,
            runtime,
            res_id,
            spinner_diag,
            error_header,
            error_detail,
        )
