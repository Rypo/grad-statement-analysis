# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from bs4 import BeautifulSoup


def strip_ads(html):
    soup = BeautifulSoup(html, "lxml")
    ads = soup.select_one('.ads')
    if ads: ads.extract()
    # leaving <div class="pTx"> tag to be processed as a start_sequence tag later
    return str(soup.body.next)


class FlatDoc(scrapy.Item):
    url_id = scrapy.Field()
    slug = scrapy.Field()
    thread_title = scrapy.Field()

    post_date = scrapy.Field()
    seqnum = scrapy.Field(
        output_processor=TakeFirst()
    )
    post_content = scrapy.Field(
        input_processor=MapCompose(strip_ads),
        output_processor=Join()
    )
    user_id = scrapy.Field(input_processor=MapCompose(lambda x: x.split('=')[-1]))
    name = scrapy.Field(input_processor=MapCompose(lambda x: x.strip('Author: ')))
    username = scrapy.Field()

    user_threads = scrapy.Field()
    user_posts = scrapy.Field()
    user_likes = scrapy.Field()


class Document(scrapy.Item):
    url_id = scrapy.Field()
    sup_title = scrapy.Field()
    posts = scrapy.Field()


class Post(scrapy.Item):
    post_date = scrapy.Field()
    post_id = scrapy.Field()
    # SoP content
    # sub_title = scrapy.Field()
    post_content = scrapy.Field()
    post_author = scrapy.Field()
    is_sop = scrapy.Field(serializer=bool)


class Author(scrapy.Item):
    name = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()

    n_threads = scrapy.Field()
    n_posts = scrapy.Field()
    n_likes = scrapy.Field()

    is_op = scrapy.Field(serializer=bool)



