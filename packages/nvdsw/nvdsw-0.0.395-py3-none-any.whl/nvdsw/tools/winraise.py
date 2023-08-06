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
Deals with raising the X window to the top of the visible stack
This module is essentially a hack, we need it to fix the issues with
the appindicator which appears to have
a bug that does not connect the clicks to the status of the resulting
popups so they don't get to the foreground
"""

import logging
import Xlib
from ewmh import EWMH

LOG = logging.getLogger("winraise")
WMH = EWMH()


def winraise(window_name):
    """
    Actually raise the xwindow. We just need to know its name
    This function is scheduled via the GTK loop
    So the return codes are false if the operation is done done
    (as in, do NOT REPEAT) ir true (please keep trying)
    """

    wins = WMH.getClientList()
    for win in wins:
        wname = None
        try:
            wname = win.get_wm_name()
        except Xlib.error.BadWindow:
            continue

        if wname is None:
            continue

        #     print("wname: " + wname)
        if wname == window_name:
            WMH.setActiveWindow(win)
            #       print('Window raised')
            wtop = WMH.getActiveWindow()
            if wtop == win:
                LOG.debug(
                    "window to raise: %s was raised and the operation took effect",
                    window_name,
                )
                return False
            else:
                # print("raised window but the operation did not go through")
                LOG.debug(
                    "window to raise: %s was raised but the operation did not take effect",
                    window_name,
                )
                return True

    LOG.debug("window to raise: %s was not found", window_name)
    return True
