# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html
from scrapy import Item,Field


class DmozItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    link = Field()
    desc = Field()


class LinkItem(Item):
    title = Field()
    link = Field()
    date = Field()
    click_times = Field()


class TextItem(Item):
    text = Field()

class GoodItem(Item):
    tag = Field()
    brand_name = Field()
    name = Field()
    price = Field()
    link = Field()

class CommonItem(Item):
    lable = Field()
    body = Field()