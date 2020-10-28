# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PostItem(scrapy.Item):
    table_name = 'posts'
    pid = Field()
    title = Field()
    thumbnail = Field()
    preview = Field()
    video = Field()
    video_format = Field()
    duration = Field()
    category = Field()
    created_at = Field()
    play_counts = Field()
    like_counts = Field()
    description = Field()


class CommentItem(scrapy.Item):
    table_name = 'comments'
    pid = Field()
    uname = Field()
    uid = Field()
    avatar = Field()
    commentid = Field()
    created_at = Field()
    like_counts = Field()
    content = Field()
    reply = Field()


class ComposerItem(scrapy.Item):
    table_name = "composers"
    uid = Field()
    name = Field()
    banner = Field()
    avatar = Field()
    introduction = Field()
    like_counts = Field()
    fans_counts = Field()
    follow_counts = Field()
    location = Field()
    career = Field()


class CopyrightItem(scrapy.Item):
    table_name = "copyrights"
    puid = Field()
    pid = Field()
    uid = Field()
    roles = Field()


class XpcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
