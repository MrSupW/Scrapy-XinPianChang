# -*- coding: utf-8 -*-
import scrapy
import re
import json
import random
import string
from scrapy import Request
from xpc.items import PostItem, CommentItem, ComposerItem, CopyrightItem


def strip(string):
    if string:
        return string.strip(" ")
    else:
        return ""


cookies = dict(Authorization='5BB1AFB20CA56C10D0CA56493D0CA56AA890CA56348A747FBA9A')


def genNewSESS():
    lis = list(string.ascii_lowercase + string.digits)
    return "".join(random.choices(lis, k=26))


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/page-1']
    page_count = 0

    def parse(self, response, **kwargs):
        self.page_count += 1
        if self.page_count >= 100:
            cookies.update(PHPSESSID=genNewSESS())
            self.page_count = 0
        post_list = response.xpath(
            '//li[@class="enter-filmplay"]')
        url = "https://www.xinpianchang.com/a{}?from=ArticleList"
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            request = response.follow(url.format(pid), self.parse_post)
            request.meta['pid'] = pid
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            yield request
        page_list = response.xpath('//div[@class="page"]/a/@href').extract()
        for page in page_list:
            yield response.follow(page, self.parse, cookies=cookies)

    def parse_post(self, response):
        pid = response.meta['pid']
        post = PostItem(pid=pid)
        post['thumbnail'] = response.meta['thumbnail']
        # get() 与  extract_first() 是一样的效果
        post['title'] = response.xpath(
            '//div[@class="title-wrap"]/h3/text()').get()
        cates = response.xpath(
            '//span[contains(@class,"cate")]//text()').extract()
        post['category'] = "".join([cate.strip() for cate in cates])
        vid = re.findall('vid: \"(\w+)\",', response.text)
        post["created_at"] = response.xpath('//span[contains(@class,"update")]//text()').get()
        post["play_counts"] = response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').get()
        post["like_counts"] = response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get()
        post["description"] = strip(response.xpath('//p[contains(@class,"desc")]//text()').get())
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/{}?expand=resource&usage=x'
        request = Request(video_url.format(vid[0]), callback=self.parse_video)
        request.meta["post"] = post
        yield request
        comment_url = 'https://app.xinpianchang.com/comments?resource_id={}'.format(pid)
        request = Request(comment_url, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request
        creator_list = response.xpath(
            '//ul[@class="creator-list"]/li')
        if creator_list:
            for creator in creator_list:
                uid = creator.xpath('./a/@data-userid').get()
                if uid:
                    url = "https://www.xinpianchang.com/u{}?from=articleList".format(uid)
                    request = response.follow(url, self.parse_composer, cookies=cookies)
                    request.meta['uid'] = uid
                    request.meta['dont_merge_cookies'] = True
                    yield request
                    cr = CopyrightItem()
                    cr['puid'] = "{}_{}".format(pid, uid)
                    cr['pid'] = pid
                    cr['uid'] = uid
                    cr['roles'] = creator.xpath('./div[@class="creator-info"]/span/text()').get()
                    yield cr

    def parse_video(self, response):
        post = response.meta['post']
        result = json.loads(response.text)
        post['video'] = result['data']['resource']['default']['url']
        post['preview'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        yield post

    def parse_comment(self, response):
        result = json.loads(response.text)

        for c in result['data']['list']:
            comment = CommentItem()
            comment['uname'] = c['userInfo']['username']
            comment['uid'] = c['userid']
            comment['avatar'] = c['userInfo']['avatar']
            comment['commentid'] = c['id']
            comment['pid'] = c['resource_id']
            comment['created_at'] = c['addtime']
            comment['like_counts'] = c['count_approve']
            comment['content'] = c['content']
            if c.get('referer'):
                comment['reply'] = c['referer']['id'] or 0
            yield comment
            next_page = result['data']['next_page_url']
            if next_page:
                yield response.follow(next_page, self.parse_comment)

    def parse_composer(self, response):
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer = ComposerItem()
        composer['uid'] = response.meta['uid']
        composer['banner'] = re.findall('background-image:url\((https://.+?.(?:jpg|jpeg|png|gif))\)', banner)[0]
        composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath('//p[contains(@class,"creator-name")]//text()').get()
        composer['introduction'] = response.xpath('//p[contains(@class,"creator-desc")]//text()').get()
        composer['like_counts'] = int(
            response.xpath('//span[contains(@class,"like-counts")]//text()').get().replace(",", ""))
        composer['fans_counts'] = int(response.xpath('//span[contains(@class,"fans-counts ")]/@data-counts').get())
        composer['follow_counts'] = int(
            response.xpath('//span[@class="follow-wrap"]/span[contains(@class,"fw_600")]/text()').get().replace(",",
                                                                                                                ""))
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/following-sibling::span[1]//text()').get() or ""
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]//following-sibling::span[1]//text()').get() or ""
        yield composer
