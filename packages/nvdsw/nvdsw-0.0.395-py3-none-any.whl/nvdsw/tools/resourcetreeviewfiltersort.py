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
displays resources, local and remote
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango
import os
import pathlib
import logging
import math
import subprocess

from nvdsw.tools.resourceactions import ResourceUIAction
from .custom_renderers import CRTCreated
from .custom_renderers import ClickablePixBuf
from .custom_renderers import CRTClickable
from .custom_renderers import CRIClickable
from .custom_renderers import StrUrlListTooltip

PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
log = logging.getLogger("rtvf")

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


class ResourceTreeViewFilterSort:
    """Structure for resources, local and remote"""

    column_names = (
        "Name",
        "Status",
        "Type",
        "Image name",
        "Tag",
        "GPUs",
        "Ports",
        "Volumes",
        "Created",
        "Actions",
    )

    # we have up to four data columns in the visible Action column.
    # the last one is always the delete icon
    # before that, there's always the restart
    # before that, there's either a start or a stop.
    # and, before that, if the container is running, there's the connect via browser icon.
    # otherwise it's empty
    data_column_types = (
        str,
        str,
        str,
        str,
        str,
        str,
        object,
        str,
        float,
        object,
        object,
        object,
        object,
    )
    column_min_sizes = (20, 20, 20, 20, 20, 20, 20, 20, 20, 20)

    column_resizable_flags = (
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
    )
    column_sortable_flags = (
        True,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
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
    init_sort_column_id = 8

    def __init__(self, rt_window, local_rt, nvaie_rt, conf):
        # rt_window
        self.rt_window = rt_window
        # local runtime
        self.local_rt = local_rt
        self.nvaie_rt = nvaie_rt
        self.config = conf
        self.liststore = Gtk.ListStore(*self.data_column_types)
        self.sorted_model = Gtk.TreeModelSort(model=self.liststore)
        # self.filter = self.liststore.filter_new()
        self.treeview = Gtk.TreeView.new_with_model(model=self.sorted_model)

        # we are passing a reference to self so that the ui action can call to update rows
        self.uiaction = ResourceUIAction(self, rt_window, conf)

        # 1 is horizontal
        # 2 == vertinal
        # 3 == both
        self.treeview.set_grid_lines(1)
        self.treeview.props.has_tooltip = True
        self.treeview.connect("query-tooltip", self.on_query_tooltip)
        self.treeview.connect("button-press-event", self.on_button_press)

        self._build_view()

    def clear(self):
        return self.liststore.clear()

    def get_treeview(self):
        return self.treeview

    def update_row(self, res, path):
        if res["rtype"] == "local":
            datarow = self.make_local_row(res)
        else:
            datarow = self.make_nvaie_row(res)
        ite = self.liststore.get_iter(path)
        # technically we don't need to update all values...
        self.liststore.set(ite, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), datarow)

    def remove_row(self, path):
        ite = self.liststore.get_iter(path)
        self.liststore.remove(ite)

    def append_local_row(self, res):
        datarow = self.make_local_row(res)
        self.liststore.append(datarow)
        return

    def append_nvaie_row(self, res):
        datarow = self.make_nvaie_row(res)
        self.liststore.append(datarow)
        return

    def make_local_row(self, res):
        """construct a row out of a pair of resource and menu item objects"""
        log.debug("making row for %s", res["name"])
        fcreated = 0
        if res.get("created") is not None:
            fcreated = float(res["created"])

        menu_item = self.local_rt.get_menu_item(
            res["menu_item_id"], pull_tag_status=False
        )

        sports, port_urls = self._ports2text(res["ports"])
        ports = StrUrlListTooltip()
        ports.set_str_list(sports)
        ports.set_url_list(port_urls)
        ports.set_tooltip_text("open port in browser")

        datarow = (
            res["name"],
            res["status"],
            res["rtype"],
            menu_item["name"],
            res["tag"],
            self._gpus2text(res["gpus"]),
            ports,
            self._volumes2text(res["volumes"]),
            fcreated,
            *self._make_buttons(self.local_rt, res),
        )
        return datarow

    def make_nvaie_row(self, res):
        """construct a row out of a pair of resource and menu item objects"""
        log.debug("making nvaie row for %s", res["id"])
        fcreated = 0
        if res.get("created") is not None:
            fcreated = float(res["created"])

        mi = self.nvaie_rt.get_menu_item(res["menu_item_id"])
        fl = self.nvaie_rt.get_flavor(res["flavor_id"])

        datarow = (
            res["id"],
            res["status"],
            res["rtype"],
            mi["name"],
            fl["name"],
            None,  # gpus
            None,  # ports
            None,  # volumes
            fcreated,
            *self._make_buttons(self.nvaie_rt, res),  # need to make buttons here
        )
        return datarow

    def _gpus2text(self, gpus):
        """convert the list of gpus to something we can display"""
        if gpus is None:
            return ""

        gstrs = []
        for g in gpus:
            gstrs.append(str(g))

        return "\n".join(gstrs)

    def ports2str(self, port_tuple):
        c = port_tuple[0]
        h = port_tuple[1]
        pstr = c.split("/")[0] + ":" + h
        return pstr

    def ports2url(self, port_tuple):
        BASE_URL = "http://localhost"
        return BASE_URL + ":" + port_tuple[1]

    def _ports2text(self, ports):
        """convert the port information to something we can display along with clickable links"""

        # if len(local_resource["ports"]) == 0 or len(local_resource["ports"]) == 1:
        #             if len(local_resource["ports"]) == 1:
        #                 port = list(local_resource["ports"].items())[0]
        #                 ports_label = (
        #                     "<a href='http://localhost:"
        #                     + port[1]
        #                     + "/lab'>"
        #                    + self.ports2str(port)
        #                    + "</a>"
        #                )
        #                 l = Gtk.Label()
        #                 l.set_markup(ports_label)
        #             else:
        #                 l = Gtk.Label(label="")

        #        c = port_tuple[0]
        #        h = port_tuple[1]
        #        pstr = c.split("/")[0] + ":" + h
        #        return pstr
        if ports is None:
            return ""

        # this needs to be made clickable and that will be tricky.
        port_labels = []
        for port in ports.items():
            port_labels.append(self.ports2str(port))

        port_urls = []
        for port in ports.items():
            port_urls.append(self.ports2url(port))

        return port_labels, port_urls
        # return "\n".join(port_labels)

    def _volumes2text(self, volumes):
        """convert the volumes information to something we can display"""
        if volumes is None or len(volumes) == 0:
            return ""

        vstrs = []
        for v in volumes:
            v = ":".join(v.split(":")[:2])
            vstrs.append(v)
        return "\n".join(vstrs)

    def _make_buttons(self, runtime, res):
        """based on the image status, return the list of appropriate buttons"""
        browser_icon = ClickablePixBuf()
        stop_start_icon = ClickablePixBuf()
        restart_icon = ClickablePixBuf()
        delete_icon = ClickablePixBuf()

        rstat = res["status"]

        # there always is the delete button
        fname = os.path.abspath(
            PKG_DIR + "/../" + self.config["icons"]["RESOURCE_DELETE"]
        )
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=fname,
            width=self.ICON_SIZE,
            height=self.ICON_SIZE,
            preserve_aspect_ratio=True,
        )
        delete_icon.set_pixbuf(pixbuf)
        delete_icon.set_tooltip_text("delete")
        delete_icon.set_meth_params(
            self.uiaction.do,
            runtime,
            runtime.delete_resource,
            res,
            "Remove resource?",
            "removing",
            "resource remove error",
            "resource " + res["id"] + " could not be removed. Please see logs",
            0,
        )
        # b.connect(
        #     "clicked", self.on_restart_clicked, self.local_rt, local_resource["id"]
        # )

        # there always is the restart button
        fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["SYNC"])
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=fname,
            width=self.ICON_SIZE,
            height=self.ICON_SIZE,
            preserve_aspect_ratio=True,
        )
        restart_icon.set_pixbuf(pixbuf)
        restart_icon.set_tooltip_text("restart")
        restart_icon.set_meth_params(
            self.uiaction.do,
            runtime,
            runtime.restart_resource,
            res,
            "Restart resource?",
            "restarting",
            "resource restart error",
            "resource " + res["id"] + " could not be restarted. Please see logs",
            0,
        )
        # b.connect(
        #     "clicked", self.on_restart_clicked, self.local_rt, local_resource["id"]
        # )

        # if the resource is running, show the stop option. otherwise, show the start option.

        if rstat == "running":
            # show the stop
            icon = "STOP"
            stxt = "stop"
            meth_params = (
                self.uiaction.do,
                runtime,
                runtime.stop_resource,
                res,
                "Stop resource?",
                "stopping",
                "resource stop error",
                "resource " + res["id"] + " could not be stopped. Please see logs",
                0,
            )
        elif rstat == "exited":
            icon = "START"
            stxt = "start"
            meth_params = (
                self.uiaction.do,
                runtime,
                runtime.start_resource,
                res,
                "Start resource?",
                "starting",
                "resource start error",
                "resource " + res["id"] + " could not be started. Please see logs",
                0,
            )
        else:
            icon = None
            stxt = None
            meth_params = None

        if icon is not None:
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"][icon])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            stop_start_icon.set_pixbuf(pixbuf)
            stop_start_icon.set_tooltip_text(stxt)
            stop_start_icon.set_meth_params(*meth_params)

        if rstat == "running":
            fname = os.path.abspath(PKG_DIR + "/../" + self.config["icons"]["TERMINAL"])
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=fname,
                width=self.ICON_SIZE,
                height=self.ICON_SIZE,
                preserve_aspect_ratio=True,
            )
            browser_icon.set_pixbuf(pixbuf)
            browser_icon.set_tooltip_text("open in browser")
            browser_icon.set_meth_params(
                self.uiaction.open_url,
                res["url"],
            )

        return browser_icon, stop_start_icon, restart_icon, delete_icon

    def get_line_num(self, cell_height, num_entries, font_size_px, y):
        """compute which line of text is below us for clicking purposes"""
        line_num = None

        # y coordinate wrt middle of the cell
        y_mid = y - cell_height / 2
        # same but in lines of text
        y_mid_lns = y_mid / font_size_px
        # if num_entries % 2 == 0:
        # line_num = num_entries / 2 + math.floor(y_mid_lns)
        line_num = math.floor(num_entries / 2 + y_mid_lns)
        if line_num < 0 or line_num >= num_entries:
            line_num = None

        return line_num

    def open_url(self, url):
        """launch generic browser against a given URL"""
        cmd = ["/usr/bin/x-www-browser", url]
        subprocess.Popen(cmd)

    def on_button_press(self, treeview, event):
        """handle button clicks"""
        # there appears to be a shift downwards by about 30 in event.y that needs to be compensanted for
        # when converting event.y compared to the y obtained from the tooltip event
        # this is why we are using tree to bin window instead of widget to bin window here.
        # bin_x, bin_y = treeview.convert_widget_to_bin_window_coords(event.x, event.y)
        bin_x, bin_y = treeview.convert_tree_to_bin_window_coords(event.x, event.y)
        result = treeview.get_path_at_pos(bin_x, bin_y)
        if result == None:
            return False
        sorted_path, column, cell_x, cell_y = result

        path = self.sorted_model.convert_path_to_child_path(sorted_path)
        # print(path)
        # remember that we added spaces on the column titles.. ew..
        if column.get_title() != " Actions " and column.get_title() != " Ports ":
            return False
        iteration = self.liststore.get_iter(path)

        if column.get_title() == " Ports ":
            sult = self.liststore.get_value(iteration, 6)
            if sult is None:
                # NVAIE does not have ports yet
                return False
            if sult.get_str_list() is None or len(sult.get_str_list()) == 0:
                # nothing to click on
                return False

            urls = sult.get_url_list()
            style = self.treeview.get_style_context()
            # 0 means normal css element
            font = style.get_font(0)
            font_size = font.get_size()
            if font.get_size_is_absolute():
                font_size_px = font_size
            else:
                # size (px) = 1.33 size (pts)
                font_size_px = font_size / 1024 * (96 / 72)

            cell = self.treeview.get_cell_area(path, column)
            line_num = self.get_line_num(cell.height, len(urls), font_size_px, cell_y)
            if line_num is None:
                # this area is not clickable
                return False

            self.open_url(urls[line_num])
            # print(line_num)
            return True

        # browser, stop_start, restart, delete..
        browser_x_offset, browser_width = column.cell_get_position(
            self.browser_button_renderer
        )
        stopstart_x_offset, stopstart_width = column.cell_get_position(
            self.stopstart_button_renderer
        )
        restart_x_offset, restart_width = column.cell_get_position(
            self.restart_button_renderer
        )
        delete_x_offset, delete_width = column.cell_get_position(
            self.delete_button_renderer
        )

        if cell_x >= browser_x_offset and cell_x <= browser_x_offset + browser_width:
            pixbuf = self.liststore.get_value(iteration, 9)
            func, params = pixbuf.get_meth_params()

            if func is not None and params is not None:
                func(*params, path)
                return True
            else:
                return False

        elif (
            cell_x >= stopstart_x_offset
            and cell_x <= stopstart_x_offset + stopstart_width
        ):
            pixbuf = self.liststore.get_value(iteration, 10)
            func, params = pixbuf.get_meth_params()
            if func is not None and params is not None:
                func(*params, path)
                return True
            else:
                return False
        elif cell_x >= restart_x_offset and cell_x <= restart_x_offset + restart_width:
            pixbuf = self.liststore.get_value(iteration, 11)
            func, params = pixbuf.get_meth_params()
            if func is not None and params is not None:
                func(*params, path)
                return True
            else:
                return False
        elif cell_x >= delete_x_offset and cell_x <= delete_x_offset + delete_width:
            pixbuf = self.liststore.get_value(iteration, 12)
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
        if column.get_title() != " Actions " and column.get_title() != " Ports ":
            return False

        iteration = self.liststore.get_iter(path)

        if column.get_title() == " Ports ":
            # the ports column has just one tooltip.. simple

            sult = self.liststore.get_value(iteration, 6)
            if sult is None:
                # NVAIE does not have ports yet
                return False

            if sult.get_str_list() is None or len(sult.get_str_list()) == 0:
                # nothing to click on
                return False

            text = sult.get_tooltip_text()
            # print(sult.get_url_list())
            if text is None:
                # just to be careful in case we didn't set it for some reason
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(tooltip, path, column, self.ports_renderer)
            return True

        # browser, stop_start, restart, delete..

        browser_x_offset, browser_width = column.cell_get_position(
            self.browser_button_renderer
        )
        stopstart_x_offset, stopstart_width = column.cell_get_position(
            self.stopstart_button_renderer
        )
        restart_x_offset, restart_width = column.cell_get_position(
            self.restart_button_renderer
        )
        delete_x_offset, delete_width = column.cell_get_position(
            self.delete_button_renderer
        )

        if cell_x >= browser_x_offset and cell_x <= browser_x_offset + browser_width:
            pixbuf = self.liststore.get_value(iteration, 9)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(
                tooltip, path, column, self.browser_button_renderer
            )
        elif (
            cell_x >= stopstart_x_offset
            and cell_x <= stopstart_x_offset + stopstart_width
        ):
            pixbuf = self.liststore.get_value(iteration, 10)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(
                tooltip, path, column, self.stopstart_button_renderer
            )
        elif cell_x >= restart_x_offset and cell_x <= restart_x_offset + restart_width:
            pixbuf = self.liststore.get_value(iteration, 11)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(
                tooltip, path, column, self.restart_button_renderer
            )
        elif cell_x >= delete_x_offset and cell_x <= delete_x_offset + delete_width:
            pixbuf = self.liststore.get_value(iteration, 12)
            text = pixbuf.get_tooltip_text()
            if text is None:
                # what if the button is empty?
                return False
            tooltip.set_text(text)
            treeview.set_tooltip_cell(
                tooltip, path, column, self.delete_button_renderer
            )
        else:
            # the mouse is over an empty area of the column
            return False

        # Since we calculated where the mouse is above, we know which cell renderer we are over.
        # So, we could call the method below passing None as the cell renderer. This also works
        # but, not sure which is better?
        # treeview.set_tooltip_cell(tooltip, path, column, None)
        return True

    def _build_view(self):
        """builds and returns the TreeView object"""

        # The first five columns are just text
        txt_ren = Gtk.CellRendererText()
        txt_ren.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)

        self.ports_renderer = CRTClickable()

        for i in range(0, 6):
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

        # the 6th column is a custom text cell renderer for ports such that it could be clickable.
        col_num = 6
        # col = Gtk.TreeViewColumn(
        #     " " + self.column_names[col_num] + " ", txt_ren, markup=col_num
        # )
        col = Gtk.TreeViewColumn(
            " " + self.column_names[col_num] + " ", self.ports_renderer, sultt=col_num
        )
        col.set_resizable(self.column_resizable_flags[col_num])
        col.set_visible(self.init_column_visibilities[col_num])
        col.set_min_width(self.column_min_sizes[col_num])
        if self.column_sortable_flags[col_num]:
            col.set_sort_column_id(col_num)
        self.treeview.append_column(col)

        # the 7th column is volumes but we are treating it just like regular text
        col_num = 7
        col = Gtk.TreeViewColumn(
            " " + self.column_names[col_num] + " ", txt_ren, markup=col_num
        )
        col.set_resizable(self.column_resizable_flags[col_num])
        col.set_visible(self.init_column_visibilities[col_num])
        col.set_min_width(self.column_min_sizes[col_num])
        if self.column_sortable_flags[col_num]:
            col.set_sort_column_id(col_num)
        self.treeview.append_column(col)

        # the 8th column is created which should be a float / long and sorted as such
        # we are displaying a user friendly string
        col_num = 8
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

        # the 9th column is three or four action buttons
        # i am not sure how to pad column names, so hacking it
        col_num = 9
        col = Gtk.TreeViewColumn(title=" " + self.column_names[col_num] + " ")

        # the last column is aligned to the right
        # this is just the setting for the header
        col.set_alignment(1)

        self.browser_button_renderer = CRIClickable()
        self.stopstart_button_renderer = CRIClickable()
        self.restart_button_renderer = CRIClickable()
        self.delete_button_renderer = CRIClickable()

        # the last column is aligned to the right
        # 0 means left or top, 0.5 means middle, 1 means right or bottom
        self.browser_button_renderer.set_alignment(1, 0.5)
        self.browser_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        self.stopstart_button_renderer.set_alignment(1, 0.5)
        self.stopstart_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        self.restart_button_renderer.set_alignment(1, 0.5)
        self.restart_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)
        self.delete_button_renderer.set_alignment(1, 0.5)
        self.delete_button_renderer.set_padding(self.CELL_PAD_X, self.CELL_PAD_Y)

        col.pack_end(self.delete_button_renderer, False)
        col.pack_end(self.restart_button_renderer, False)
        col.pack_end(self.stopstart_button_renderer, False)

        # this is a bit of a trick
        # if this column is resized, one of the renderers will need to get the extra space
        # if we don't designate one, it will be the last renderer and it will look ugly
        # since our renderers are clickable, this is a bit suboptimal.. perhaps a fake renderer would be more ideal
        col.pack_end(self.browser_button_renderer, True)

        col.set_resizable(self.column_resizable_flags[col_num])
        col.set_visible(self.init_column_visibilities[col_num])
        col.set_min_width(self.column_min_sizes[col_num])

        # the last column should not expand.
        col.set_expand(False)
        col.add_attribute(self.browser_button_renderer, "clkpixbuf", 9)
        col.add_attribute(self.stopstart_button_renderer, "clkpixbuf", 10)
        col.add_attribute(self.restart_button_renderer, "clkpixbuf", 11)
        col.add_attribute(self.delete_button_renderer, "clkpixbuf", 12)

        self.treeview.append_column(col)
