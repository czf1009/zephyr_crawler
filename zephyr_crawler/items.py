# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html
from scrapy import Item,Field

class JdCommentItem(Item):
    comment_id = Field()
    ware_id = Field()
    comment_data = Field()
    comment_date = Field()


class CommonItem(Item):
    lable = Field()
    body = Field()