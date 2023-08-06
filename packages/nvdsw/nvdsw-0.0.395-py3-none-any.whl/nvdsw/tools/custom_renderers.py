import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

import timeago
import datetime


class CRTCreated(Gtk.CellRendererText):
    """custom renderer for the created timeago field"""

    @GObject.Property(type=float)
    def created(self):
        return self.created

    @created.setter
    def created(self, created_ts):
        self.created_ts = created_ts
        s_created = None
        if created_ts > 0:
            s_created = timeago.format(created_ts, datetime.datetime.now())
        super().set_property("text", s_created)


class CRTSize(Gtk.CellRendererText):
    """custom cell renderer for sizes in GB"""

    @GObject.Property(type=float)
    def size(self):
        return self.fsize

    @size.setter
    def size(self, fsize):
        self.fsize = fsize
        s_size = None
        if fsize > 0:
            s_size = "{:.1f}".format(fsize / 1024 / 1024 / 1024)
        super().set_property("text", s_size)


class ClickablePixBuf:
    """a data analog of a button, e.g a pixbuf with bound method / params and a tooltip"""

    def __init__(self):
        self.meth = None
        self.pars = None
        self.pixbuf = None
        self.tooltip_text = None

    def set_meth_params(self, meth, *pars):
        """bind a method and params to this data class"""
        self.meth = meth
        self.pars = pars

    def get_meth_params(self):
        """get the associated method and params"""
        return self.meth, self.pars

    def set_pixbuf(self, pixbuf):
        """associate a pixbuf"""
        self.pixbuf = pixbuf

    def get_pixbuf(self):
        """get the associated pixbuf"""
        return self.pixbuf

    def set_tooltip_text(self, tooltip_text):
        """set text only tooltip"""
        self.tooltip_text = tooltip_text

    def get_tooltip_text(self):
        """get text only tooltip"""
        return self.tooltip_text


class CRIClickable(Gtk.CellRendererPixbuf):
    """a pixbuf cell renderer that can work with ClickablePixBuf data type"""

    @GObject.Property(type=object)
    def clkpixbuf(self):
        """gets the associated ClickablePixBuf data type"""
        return self.cpixbuf

    @clkpixbuf.setter
    def clkpixbuf(self, cpixbuf):
        """sets the associated ClickablePixBuf data type"""
        # Note the get_pixbuf() method that matches that of the ClickablePixBuf
        self.cpixbuf = cpixbuf
        pix = cpixbuf.get_pixbuf()
        super().set_property("pixbuf", pix)


class StrUrlListTooltip:
    """a custom data type: list of strings with an associated list of URLs and a tooltip"""

    def __init__(self):
        self.str_list = None
        self.url_list = None
        self.tooltip_text = None

    def get_txt(self):
        """set the text for display, just a newline separated string list for now"""
        return "\n".join(self.str_list)

    def set_str_list(self, str_list):
        """set the list of strings"""
        self.str_list = str_list

    def get_str_list(self):
        """get the list of strings"""
        return self.str_list

    def set_url_list(self, url_list):
        """set the list of urls"""
        self.url_list = url_list

    def get_url_list(self):
        """get the list of urls"""
        return self.url_list

    def set_tooltip_text(self, tooltip_text):
        """set text only tooltip, one per renderer"""
        self.tooltip_text = tooltip_text

    def get_tooltip_text(self):
        """get text only tooltip, one per renderer"""
        return self.tooltip_text


class CRTClickable(Gtk.CellRendererText):
    """a text cell renderer that can work with StrUrlListTooltip data type"""

    @GObject.Property(type=object)
    def sultt(self):
        """gets the associated ClickablePixBuf data type"""
        return self.str_list

    @sultt.setter
    def sultt(self, str_list):
        """sets the associated ClickablePixBuf data type"""
        # Note the get_pixbuf() method that matches that of the ClickablePixBuf
        self.str_list = str_list
        if str_list is not None:
            txt = str_list.get_txt()
        else:
            txt = None
        super().set_property("markup", txt)


#### commenting this out due to intermittent crashes. implementing the activatable seems like the preferred
#### approach but one needs to resolve the crashes
####    def do_activate(self, event, widget, path, background_area, cell_area, flags):
####        """this is triggered when the icon is clicked"""
####        print("activate starting")
####        func, params = self.cpixbuf.get_meth_params()
####        # new_params = copy.deepcopy(list(params))
####        # append path (row num) to the params
####        # new_params.append(path)
####        # we have two icon slots. one of them may be empty so just don't do anything
####        if func is not None and params is not None:
####            # func(*new_params)
####            func(*params, path)
####            print("done with activate call")
####        return True

#### this is the most complete example which includes signal emission and consumption
#### unfortunately, it is not clear how to resolve the intermittent crashes
#### class CRIClickable1(Gtk.CellRendererPixbuf):
####    @GObject.Property(type=object)
####    def clkpixbuf(self):
####        return self.cpixbuf
####
####    @clkpixbuf.setter
####    def clkpixbuf(self, cpixbuf):
####        #        print("in setter")
####        #        print(type(cpixbuf))
####        self.cpixbuf = cpixbuf
####        pix = cpixbuf.get_pixbuf()
####        super().set_property("pixbuf", pix)
####
####    @GObject.Signal(
####        flags=GObject.SignalFlags.RUN_LAST,
####        return_type=bool,
####        arg_types=(
####            object,
####            Gtk.Widget,
####            str,
####        ),
####        accumulator=GObject.signal_accumulator_true_handled,
####    )
####    def clickt(self, event, widget, path):
####        return True
####
####    def do_activate(self, event, widget, path, background_area, cell_area, flags):
####        # self.emit("clickt", object(), widget, path)
####        print("before emit")
####        self.emit("clickt", event, widget, path)
####        print("after emit")
####        return True
####
####    def on_clickt(self, a, b, widget, path, *params):
####        print("onclickt called!")
####        #        print(a)
####        #        print(b)
####        #        print(widget)
####        #        print(path)
####        func, params = self.cpixbuf.get_meth_params()
####        if func is not None and params is not None:
####            func(*params, path)
####            print("done with activate call")
####            return True
####
####        return False


##    def do_activate(self, event, widget, path, background_area, cell_area, flags):
##        """this is triggered when the icon is clicked"""
##        print("activate starting")
##        func, params = self.cpixbuf.get_meth_params()
##        # new_params = copy.deepcopy(list(params))
##        # append path (row num) to the params
##        # new_params.append(path)
##        # we have two icon slots. one of them may be empty so just don't do anything
##        if func is not None and params is not None:
##            # func(*new_params)
##            func(*params, path)
##            print("done with activate call")
##        return True

# leaving this here to show how to do a proper object with signals
# this is workable code, we just don't need it at this point
# class CRIconClickable(Gtk.CellRendererPixbuf):
#     @GObject.Signal(
#         flags=GObject.SignalFlags.RUN_LAST,
#         return_type=bool,
#         arg_types=(
#             object,
#             Gtk.Widget,
#             str,
#         ),
#          accumulator=GObject.signal_accumulator_true_handled,
#     )
#     def clickt(self, event, widget, path):
#         return True

#     def do_activate(self, event, widget, path, background_area, cell_area, flags):
#         self.emit("clickt", object(), widget, path)
#         return True
#
