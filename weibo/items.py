# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class xlweiboItem(scrapy.Item):
    info_name = scrapy.Field()
    info_time = scrapy.Field()
    info_body = scrapy.Field()
    info_repost = scrapy.Field()
    info_comment = scrapy.Field()
    info_attitudes = scrapy.Field()
    def get_insert_sql(self):
        sql = "INSERT INTO xinlangweibo(username,datatime,body,repost,comment,attitudes) VALUES" \
              "(%s,%s,%s,%s,%s,%s)"
        data = (self["info_name"],self["info_time"],self["info_body"],self["info_repost"],self["info_comment"],self["info_attitudes"])
        return (sql,data)

