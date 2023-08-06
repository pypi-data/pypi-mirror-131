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
dispays image data in treeview
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
import os
import pathlib
import logging

# import copy
from nvdsw.tools.imageactions import ImageUIAction
from .custom_renderers import CRTCreated
from .custom_renderers import ClickablePixBuf
from .custom_renderers import CRTSize
from .custom_renderers import CRIClickable


PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
log = logging.getLogger("itvf")

# when we pause the image download, we essentially close the generator causing the pull process to die
# that takes time, so if we don't wait a little bit to check the status, it will still be pulling
# and the UI won't update.  The same on resume; we simply add the image to the pull queue and one of the threads will have to grab it.
#  it's not instantaneous
IMG_PULL_PAUSE_POST_FUNC_SLEEP = 0.5
IMG_PULL_RESUME_POST_FUNC_SLEEP = 0.5

# in the default ubuntu light themes, the treeview header boundaries are virually invisible
# we need to make them a little darker so that they are visible - and users can drag them / resize the columns
# notice the these are lifted from nautilus that has its own css [!]
scss = b"""
treeview.view header button {
    border-top-color: rgba(196,196,196, 0.4);
    border-left-color: rgba(196,196,196, 0.4); 
    border-right-color: rgba(196,196,196, 0.4); 
    border-bottom-color: rgba(196,196,196, 0.4);
}
"""

style_provider = Gtk.CssProvider()
style_provider.load_from_data(scss)
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class ImageTreeViewFilterSort:
    """Structure for resources, local and remote"""

    # the last two data columns are button names for the Actions column
    data_column_types = (
        str,
        str,
        str,
        float,
        float,
        object,
        object,
    )

    column_names = (
        "Name",
        "Tag",
        "Status",
        "Size, GB",
        "Created",
        "Actions",
    )
    column_min_sizes = (20, 20, 20, 20, 20, 20)

    column_resizable_flags = (
        True,
        True,
        True,
        True,
        True,
        True,
    )
    column_sortable_flags = (
        True,
        True,
        True,
        True,
        True,
        False,
    )
    init_column_visibilities = (
        True,
        True,
        True,
        True,
        True,
        True,
    )

    # width and height are the same
    ICON_SIZE = 16

    # cell padding
    CELL_PAD_X = 15
    CELL_PAD_Y = 15

    # initially, sort by the created column
    init_sort_column_id = 4

    def __init__(self, rt_window, runtime, conf):
        # rt_window
        self.rt_window = rt_window
        # local runtime
        self.runtime = runtime
        self.config = conf
        self.liststore = Gtk.ListStore(*self.data_column_types)
        # self.filter = self.liststore.filter_new()
        self.treeview = Gtk.TreeView.new_with_model(
            model=Gtk.TreeModelSort(model=self.liststore)
        )

        # we are passing a reference to self so that the ui action can call to update rows
        self.uiaction = ImageUIAction(self, rt_window, runtime, conf)
        # 1 is horizontal
        # 2 == vertinal
        # 3 == both
        self.treeview.set_grid_lines(1)
        self.treeview.props.has_tooltip = True
        self.treeview.connect("query-tooltip", self.on_query_tooltip)
        self.treeview.connect("button-press-event", self.on_button_press)

        ## the below is supposed to be a fine grained way of fixing the vertical grid lines on the column headers, but it does not quite work for some reason.
        #        Gtk.StyleContext.add_provider(
        #            self.treeview.get_style_context(),
        #            style_provider,
        #            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        #        )
        # self.treeview.get_style_context().add_class("blk_header_btn_borders")
        # Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self._build_view()

    def clear(self):
        return self.liststore.clear()

    def get_treeview(self):
        return self.treeview

    def update_row(self, local_image, tag, path):
        datarow = self.make_row(local_image, tag)
        ite = self.liststore.get_iter(path)
        # technically we don't need to update the first two values: image and tag since they don't change
        self.liststore.set(ite, (0, 1, 2, 3, 4, 5, 6), datarow)

    def append_row(self, local_image, tag):
        datarow = self.make_row(local_image, tag)
        self.liststore.append(datarow)
        return

    def make_row(self, local_image, tag):
        """construct a row out of a pair of resource and menu item objects"""

        fcreated = 0
        if tag.get("created") is not None:
            fcreated = float(tag["created"])

        fsize = 0
        if tag.get("size") is not None:
            fsize = float(tag["size"])

        download_button, action_button = self._make_buttons(local_image, tag)

        datarow = (
            local_image["name"],
            tag["tag"],
            tag["status"],
            fsize,
            fcreated,
            download_button,
            action_button,
        )
        return datarow

    def _make_buttons(self, local_image, tag):
        """based on the image status, return the list of appropriate buttons"""
        logs_icon = ClickablePixBuf()
        action_icon = ClickablePixBuf()
        if tag["status"] == "pulled":
            fname = os.path.abspath(
                PKG_DIR + "/../" + self.config["icons"]["RESOURCE_DELETE"]
            )
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            action_icon.set_pixbuf(pixbuf)
            action_icon.set_tooltip_text("delete image")
            # local_image["id"], tag["tag"]
            action_icon.set_meth_params(
                self.uiaction.do,
                self.runtime.uncache_menu_item_tag,
                local_image,
                tag,
                "Delete image?",
                "deleting",
                "image delete error",
                "image "
                + local_image["image"]
                + ":"
                + tag["tag"]
                + " could not be deleted. Please see logs",
                0,
            )
            # action_icon.set_meth_params(
            #     self.rt_window.on_image_delete_clicked,
            #     None,
            #     self.runtime,
            #     local_image,
            #     tag,
            # )

        elif tag["status"] == "pulling" or tag["status"] == "queued":
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["PAUSE"])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            action_icon.set_pixbuf(pixbuf)
            action_icon.set_tooltip_text("pause pull")
            # there will be a 0.5s delay after this command so that the status update will reflect the actual status change
            action_icon.set_meth_params(
                self.uiaction.do,
                self.runtime.pause_caching_menu_item_tag,
                local_image,
                tag,
                "Pause image download?",
                "pausing",
                "image pause error",
                "image "
                + local_image["image"]
                + ":"
                + tag["tag"]
                + " could not be paused. Please see logs",
                IMG_PULL_PAUSE_POST_FUNC_SLEEP,
            )
            # action_icon.set_meth_params(
            #     self.rt_window.on_image_pause_clicked,
            #     None,
            #     self.runtime,
            #     local_image,
            #     tag,
            # )

        elif tag["status"] == "paused":
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["START"])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            action_icon.set_pixbuf(pixbuf)
            action_icon.set_tooltip_text("resume pull")
            # there will be a 0.5s delay after this command so that the status update will reflect the actual status change
            action_icon.set_meth_params(
                self.uiaction.do,
                self.runtime.unpause_caching_menu_item_tag,
                local_image,
                tag,
                "Resume image download?",
                "resuming",
                "image resume error",
                "image "
                + local_image["image"]
                + ":"
                + tag["tag"]
                + " could not be resumed. Please see logs",
                IMG_PULL_RESUME_POST_FUNC_SLEEP,
            )

            # action_icon.set_meth_params(
            #     self.rt_window.on_image_unpause_clicked,
            #     None,
            #     self.runtime,
            #     local_image,
            #     tag,
            # )

        elif tag["status"] == "not pulled":
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["DOWNLOAD"])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            action_icon.set_pixbuf(pixbuf)
            action_icon.set_tooltip_text("pull image")
            action_icon.set_meth_params(
                self.uiaction.do,
                self.runtime.cache_menu_item_tag,
                local_image,
                tag,
                "Pull image?",
                "starting pull",
                "image pull error",
                "image "
                + local_image["image"]
                + ":"
                + tag["tag"]
                + " could not be pulled. Please see logs",
                0,
            )
            # action_icon.set_meth_params(
            #     self.rt_window.on_image_download_clicked,
            #     None,
            #     self.runtime,
            #     local_image,
            #     tag,
            # )

        if tag["status"] == "pulling":
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["LOG"])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            logs_icon.set_pixbuf(pixbuf)
            logs_icon.set_tooltip_text("build output")
            logs_icon.set_meth_params(
                self.uiaction.do_log,
                local_image,
                tag,
            )
            # logs_icon.set_meth_params(
            #     self.rt_window.on_image_build_log_clicked,
            #     None,
            #     self.runtime,
            #     local_image,
            #     tag,
            # )

        return logs_icon, action_icon

    def _build_view(self):
        """builds and returns the TreeView object"""

        # The first five columns are just text
        txt_ren = Gtk.CellRendererText()
        txt_ren.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)

        for i in range(0, 3):
            # i am not sure how to pad column titles, so hacking it
            col = Gtk.TreeViewColumn(
                " " + self.column_names[i] + " ", txt_ren, markup=i
            )
            col.set_resizable(self.column_resizable_flags[i])
            col.set_visible(self.init_column_visibilities[i])
            col.set_min_width(self.column_min_sizes[i])
            if self.column_sortable_flags[i]:
                col.set_sort_column_id(i)
            self.treeview.append_column(col)

        # the third column is size which is a GB float..
        # need to sort by the actual number, not string
        col_num = 3
        size_ren = CRTSize()
        size_ren.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        col = Gtk.TreeViewColumn(
            " " + self.column_names[col_num] + " ", size_ren, size=col_num
        )
        col.set_resizable(self.column_resizable_flags[col_num])
        col.set_visible(self.init_column_visibilities[col_num])
        col.set_min_width(self.column_min_sizes[col_num])

        if self.column_sortable_flags[col_num]:
            col.set_sort_column_id(col_num)
        self.treeview.append_column(col)

        # the fourth column is created which should be a float / long and sorted as such
        # we are displaying a user friendly string
        col_num = 4
        created_ren = CRTCreated()
        created_ren.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        col = Gtk.TreeViewColumn(
            " " + self.column_names[col_num] + " ", created_ren, created=col_num
        )
        col.set_resizable(self.column_resizable_flags[col_num])
        col.set_visible(self.init_column_visibilities[col_num])
        col.set_min_width(self.column_min_sizes[col_num])

        # it's okay to expand this column
        col.set_expand(True)
        if self.column_sortable_flags[col_num]:
            col.set_sort_column_id(col_num)
        self.treeview.append_column(col)

        # the 6th column is one or two action buttons
        # i am not sure how to pad column names, so hacking it
        col = Gtk.TreeViewColumn(title=" " + self.column_names[5] + " ")

        # the last column is aligned to the right
        # this is just the setting for the header
        col.set_alignment(1)

        # self.log_button_renderer = Gtk.CellRendererPixbuf()
        # self.action_button_renderer = Gtk.CellRendererPixbuf()

        self.log_button_renderer = CRIClickable()
        self.action_button_renderer = CRIClickable()
        ### self.log_button_renderer = CRIClickable1()
        ### self.action_button_renderer = CRIClickable1()
        ### self.log_button_renderer.set_property("mode", Gtk.CellRendererMode.ACTIVATABLE)
        ###   self.action_button_renderer.set_property(
        ###       "mode", Gtk.CellRendererMode.ACTIVATABLE
        ###   )

        ### self.log_button_renderer.connect("clickt", self.log_button_renderer.on_clickt)
        ### self.action_button_renderer.connect(
        ###     "clickt", self.action_button_renderer.on_clickt
        ### )

        # the last column is aligned to the right
        self.log_button_renderer.set_alignment(1, 0)
        self.log_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        self.action_button_renderer.set_alignment(1, 0)
        self.action_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)

        col.pack_end(self.action_button_renderer, False)

        # this is a bit of a trick
        # if this column is resized, one of the renderers will need to get the extra space
        # if we don't designate one, it will be the last renderer and it will look ugly
        # since our renderers are clickable, this is a bit suboptimal.. perhaps a fake renderer would be more ideal
        col.pack_end(self.log_button_renderer, True)

        col.set_resizable(self.column_resizable_flags[5])
        col.set_visible(self.init_column_visibilities[5])
        col.set_min_width(self.column_min_sizes[5])

        # the last column should not expand.
        col.set_expand(False)
        col.add_attribute(self.log_button_renderer, "clkpixbuf", 5)
        col.add_attribute(self.action_button_renderer, "clkpixbuf", 6)

        self.treeview.append_column(col)

    def on_button_press(self, treeview, event):
        # there appears to be a shift downwards by about 30 in event.y that needs to be compensanted for
        # when converting event.y compared to the y obtained from the tooltip event
        # this is why we are using tree to bin window instead of widget to bin window here.
        # bin_x, bin_y = treeview.convert_widget_to_bin_window_coords(event.x, event.y)
        bin_x, bin_y = treeview.convert_tree_to_bin_window_coords(event.x, event.y)

        result = treeview.get_path_at_pos(bin_x, bin_y)
        if result == None:
            return False
        path, column, cell_x, cell_y = result
        # remember that we added spaces on the column titles.. ew..
        if column.get_title() != " Actions ":
            return False
        ## log.debug("event.x: %s, event.y is: %s", event.x, event.y)
        iteration = self.liststore.get_iter(path)
        # the log cell is to the left, the action cell to the right
        log_x_offset, log_width = column.cell_get_position(self.log_button_renderer)
        act_x_offset, act_width = column.cell_get_position(self.action_button_renderer)
        if cell_x >= log_x_offset and cell_x <= log_x_offset + log_width:
            # this is the log button cell
            pixbuf = self.liststore.get_value(iteration, 5)
            func, params = pixbuf.get_meth_params()

            if func is not None and params is not None:
                func(*params, path)
                return True
            else:
                return False

        elif cell_x >= act_x_offset and cell_x <= act_x_offset + act_width:
            # this is the action cell
            pixbuf = self.liststore.get_value(iteration, 6)
            func, params = pixbuf.get_meth_params()
            if func is not None and params is not None:
                func(*params, path)
                return True
            else:
                return False
        else:
            # the mouse is over an empty area of the column
            return False

    def on_query_tooltip(self, treeview, x, y, keyboard_mode, tooltip):
        """an incredibly suspiscious way to display tooltips"""
        # this method is hit every time mouse is over the treeview, so it needs to be fast
        if keyboard_mode:
            path, column = treeview.get_cursor()
            if not path:
                return False
        else:
            bin_x, bin_y = treeview.convert_widget_to_bin_window_coords(x, y)
            result = treeview.get_path_at_pos(bin_x, bin_y)
            if result is None:
                return False
        path, column, cell_x, cell_y = result

        # display tooltips on the Actions Column only
        # remember that we added spaces on the column titles.. ew..
        if column.get_title() != " Actions ":
            return False

        ## log.debug("x: %s, y is: %s", x, y)
        iteration = self.liststore.get_iter(path)
        # the log cell is to the left, the action cell to the right
        log_x_offset, log_width = column.cell_get_position(self.log_button_renderer)
        act_x_offset, act_width = column.cell_get_position(self.action_button_renderer)

        if cell_x >= log_x_offset and cell_x <= log_x_offset + log_width:
            # this is the log button cell
            pixbuf = self.liststore.get_value(iteration, 5)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(tooltip, path, column, self.log_button_renderer)
        elif cell_x >= act_x_offset and cell_x <= act_x_offset + act_width:
            # this is the action cell
            pixbuf = self.liststore.get_value(iteration, 6)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(
                tooltip, path, column, self.action_button_renderer
            )
        else:
            # the mouse is over an empty area of the column
            return False

        # Since we calculated where the mouse is above, we know which cell renderer we are over.
        # So, we could call the method below passing None as the cell renderer. This also works
        # but, not sure which is better?
        # treeview.set_tooltip_cell(tooltip, path, column, None)
        return True


##     def filter_func(self, model, iter, data):
##        """Tests if the image in the row is active or not"""
##        if (
##            self.current_filter_language is None
##            or self.current_filter_language == "None"
##        ):
##            return True
##        else:
##            return model[iter][2] == self.current_filter_language
