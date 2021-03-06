# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import WeibohotsearchCrawlerItem
from crawl_common.utils import original_dates, new_ts
import json
from scrapy.shell import inspect_response


class WeibohotsearchSpider(Spider):
    name = 'weibohotsearch'
    base_url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=%s&type=realTimeHotSearchList&t=1348245512"
    date_list = original_dates()
    start_urls = [base_url % date for date in date_list]

    def parse(self, response):
        hotsearch = json.loads(response.body)
        for item in hotsearch:
            hotsearch_item = WeibohotsearchCrawlerItem()
            date = response.url.replace('https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=', '')\
                                .replace('&type=realTimeHotSearchList&t=1348245512', '')\
                                .replace('/','-')
            hotsearch_item['ts'] = new_ts(date)
            hotsearch_item['date'] = date
            hotsearch_item['keyword'] = item['keyword']
            hotsearch_item['url'] = item['url']
            hotsearch_item['wbcount'] = item['count']
            hotsearch_item['searchcount'] = item['searchCount']
            hotsearch_item['rank'] = item['rank']

            yield hotsearch_item
