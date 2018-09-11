# -*- coding: utf-8 -*-
import scrapy
import json
from multiprocessing import Pool
import time,re
from queue import Queue
from weibo.items import xlweiboItem

class XlweiboSpider(scrapy.Spider):
    name = 'xlweibo'
    allowed_domains = ['https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4288_-_ctg1_4288']
    # start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4288_-_ctg1_4288&openApp=%s']
    def start_requests(self):
        for k in range(1,101):
            url ="https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4288_-_ctg1_4288&openApp=%s"%k
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
            response = json.loads(response.text)
            html_url = response['data']['cards']  #列表页单个全部信息
            for lookfor_url in html_url:
                base_id = lookfor_url["mblog"]["user"]["id"] #单个用户的页面
                for i in range(1,151):
                    new_url = "https://m.weibo.cn/api/container/getIndex?uid="+str(base_id)+"&luicode=10000011&lfid="+str(base_id)+"_-_WEIBO_SECOND_PROFILE_WEIBO&containerid=107603"+str(base_id)+"&page=%s"%i
                    yield scrapy.Request(new_url, callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):   #获得了单个用户的个人主页
        item = xlweiboItem()
        response = response.text
        response = json.loads(response)
        html_url = response['data']['cards']
        for lookfor_url in html_url:
            info_name = lookfor_url["mblog"]["user"]["screen_name"]
            info_time = lookfor_url["mblog"]["created_at"]
            info_body = lookfor_url["mblog"]["text"]
            info_repost = lookfor_url["mblog"]["reposts_count"]
            info_comment = lookfor_url["mblog"]["comments_count"]
            info_attitudes = lookfor_url["mblog"]["attitudes_count"]
            if '小时' in info_time:
                info_time = '07-30'
            item["info_name"] = info_name
            item["info_time"] = info_time
            item["info_body"] = info_body
            item["info_repost"] = info_repost
            item["info_comment"] = info_comment
            item["info_attitudes"] = info_attitudes
            yield item