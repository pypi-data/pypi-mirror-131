#!/usr/bin/env python3
#
# coding: utf-8

# Copyright (c) 2019-2020, vVIDIA CORPORATION.  All Rights Reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
#

"""
abstract stuff
"""
from abc import ABC, abstractmethod


class Runtime(ABC):
    """
    abstract class for all runtimes"""

    @abstractmethod
    def auth(self, creds):
        """
        authenticate
        """

    @abstractmethod
    def logout(self):
        """
        logout
        """

    @abstractmethod
    def authed(self):
        pass

    # get the user stuff provided with the auth data
    @abstractmethod
    def get_user(self):
        pass

    @abstractmethod
    def get_menu(self):
        pass

    @abstractmethod
    def get_flavors(self):
        pass

    @abstractmethod
    def get_flavor(self, flavor_id):
        pass

    @abstractmethod
    def get_menu_item(self, menu_item_id):
        pass

    @abstractmethod
    def create_resource(self, menu_item_id, flavor_id, *params):
        pass

    @abstractmethod
    def get_resource_ids(self):
        pass

    @abstractmethod
    def get_resources(self):
        pass

    # for status purposes
    @abstractmethod
    def get_resource(self, resource_id):
        pass

    @abstractmethod
    def delete_resource(self, resource_id):
        pass

    @abstractmethod
    def stop_resource(self, resource_id):
        pass

    @abstractmethod
    def start_resource(self, resource_id):
        pass

    @abstractmethod
    def restart_resource(self, resource_id):
        pass
