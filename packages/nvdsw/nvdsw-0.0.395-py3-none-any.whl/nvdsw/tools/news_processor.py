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


import logging

# import os
import sys

# import time
import traceback

# from copy import copy
import feedparser
import datetime

log = logging.getLogger("news_processor")


class NewsItem:
    def __init__(self, title, description, href, timestamp):
        self.title = title
        self.description = description
        self.href = href
        self.timestamp = timestamp

    @classmethod
    def from_rss_entry(cls, entry, max_title_length):
        try:
            title = entry["title"][:max_title_length]
            href = entry["link"]
            desc = entry["description"]
            pubdate = entry["published"]
            pubDate = "-".join(pubdate.split()[1:5])
            timestamp = datetime.datetime.strptime(
                pubDate, "%d-%b-%Y-%H:%M:%S"
            ).timestamp()
        except Exception:
            log.error("unable to parse entry %s", entry)
            exc_type, exc_value, exc_tb = sys.exc_info()
            log.error(traceback.format_exception(exc_type, exc_value, exc_tb))
            return None

        return NewsItem(title, desc, href, timestamp)

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_href(self):
        return self.href

    def get_timestamp(self):
        return self.timestamp


# always an ordered list of NewsItem
# class NewsItems:
#   def __init__(self):

#   def get(num_items):
# returm the top num items

#   def merge_feeds(rss_feeds):
# add the feeds
# get the list of items for notifications

#  def get_notifications?

# the genetal idea.
# we pull the feed.
# we parse the feed into items
# we merge the items with the ones we currently have
# we update the friggin menu item.
# we figure out which ones are new and need to be notif
# we notify
# we clean periodically

# --------------------------------
# without notifications...
# we pull the feeds
# we create a News Item from each RSS item.
# we sort them, descending, by time.
# we take N off the top, display them (generate the menu items.)
# don't even need to remember anything.

# with notifications...
# preserve the timestamp of the news item from the previous pull
# once we generate the new list of items to display, get the list of those that are newer than that time stamp
# take N_NOTIFY items off that top
# notify about those.


class NewsProcessor:
    def __init__(self, settings):
        self.settings = settings
        self.newest_item_timestamp = -1

        self.titles = None
        self.hrefs = None

    # current_items, new_items = NewsProcessor.parseFeeds()
    def parseFeeds(self):

        log.debug("parseFeeds starting...")
        # extracting these here AGAIN because we don't want crazy concurrency side effects
        feed_urls = self.settings.get()["News"]["RSS_FEED_URLS"]
        max_title_length = self.settings.get()["News"]["MAX_ITEM_TITLE_LEN"]
        max_display_items = self.settings.get()["News"]["MAX_DISPLAY_ITEMS"]
        max_notify_items = self.settings.get()["News"]["MAX_ITEM_NOTIFICATIONS"]

        feeds = []
        # the idea is that the the href of a news item is unique
        href_set = set()
        newsItems = []
        new_newsItems = []

        log.debug("parseFeeds retrieving feeds...")
        for f in feed_urls:
            try:
                feeds.append(feedparser.parse(f))
            except Exception:
                log.error("unable to parse feed %s", f)
                exc_type, exc_value, exc_tb = sys.exc_info()
                log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))

        log.debug("parseFeeds pulled %s feeds...", str(len(feeds)))
        if len(feeds) == 0:
            log.warning("unable to pull any feeds")
            # this could be a network issue so we should simply retry
            return None, None

        for feed in feeds:
            for entry in feed["entries"]:
                newsItem = NewsItem.from_rss_entry(entry, max_title_length)
                if newsItem is not None:
                    # eliminate duplicate urls
                    if not newsItem.get_href() in href_set:
                        href_set.add(newsItem.get_href())
                        newsItems.append(newsItem)

        log.debug("parseFeeds fetched %s news items...", str(len(newsItems)))
        if len(newsItems) == 0:
            # this is weird, we should try again
            return None, None

        # we need to sort these descending by the time stamp
        # and then take MAX_DISPLAY_ITEMS off the top
        newsItems.sort(reverse=True, key=lambda item: item.get_timestamp())

        newest_item_timestamp = newsItems[0].get_timestamp()
        if newest_item_timestamp > self.newest_item_timestamp:
            for newsItem in newsItems:
                if newsItem.get_timestamp() > self.newest_item_timestamp:
                    new_newsItems.append(newsItem)

            log.debug(
                "parseFeeds fetched %s new news items...", str(len(new_newsItems))
            )
            self.newest_item_timestamp = newest_item_timestamp
            if len(new_newsItems) > max_notify_items:
                log.debug(
                    "parseFeeds limiting notifications to %s new news items...",
                    str(max_notify_items),
                )
                new_newsItems = new_newsItems[:max_notify_items]

        if len(newsItems) > max_display_items:
            log.debug(
                "parseFeeds limiting display to %s news items...",
                str(max_display_items),
            )
            newsItems = newsItems[:max_display_items]

        return newsItems, new_newsItems
