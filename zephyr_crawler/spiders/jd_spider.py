# coding:utf8
import scrapy
from zephyr_crawler.items import CommenItem
from scrapy.shell import inspect_response
import json
import re
###


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = [
        "jd.com",
        'p.3.cn'    # price json
    ]
    start_urls = [
        'https://list.jd.com/list.html?cat=9987,653,655'
        # 'https://item.jd.com/4139518.html'
        # 'https://item.jd.com/10921539206.html'
    ]
    custom_settings = {
        'COOKIES_DEBUG': False,
        'COOKIES_ENABLED': False,
        #'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        # 'REDIRECT_ENABLED': False,
        # 'HTTPERROR_ALLOWED_CODES': '302',
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'zephyr_crawler.pipelines.CommenPipeline': 500
        },
        'DEPTH_LIMIT': 0,
        # 'DOWNLOAD_DELAY': 1,
        # 'REDIRECT_ENABLED': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 10,
    }

    def __init__(self):
        self.deny_type = [
            'docx', 'doc',
            'xlsx', 'pptx', 'xls',
            'pdf',
            'jpg', 'png',
            'zip', 'rar',
            'exe'
        ]

    def parse(self, response):
        # Get total num of catelog's page
        page_num = int(re.search('共<b>(\d*?)</b>页',response.body).group(1))
        for i in range(1,page_num+1):
            url = 'https://list.jd.com/list.html?cat=9987,653,655&page=%d&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main' % i
            yield scrapy.Request(url=url, callback=self.catelog)
            

    def catelog(self, response):
        print '\nresponse_url : %s\n' %response.url
        return

        # Crawl itempage from catelog

        # If bannde then change proxy
        if not response.body:
            inspect_response(response, self)
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        # getItem url
        items_cel = response.xpath('//div[@id="plist"]/ul/li')
        for item_cel in items_cel:
            item_url = item_cel.xpath('div/div[1]/a/@href').extract_first()
            yield scrapy.Request(item_url, callback=self.getItem)

    def getItem(self, response):
        # Crawl iteminfo from catelog
        # If bannde then change proxy
        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        # Get ItemInfo
        item = {}
        info_li = response.xpath(
            '//ul[@class="parameter2 p-parameter-list"]/li')
        for li in info_li:
            detail = li.xpath('text()').extract_first()
            tmp = li.xpath('a/text()').extract_first()
            if tmp:
                detail = detail+tmp
            detail = detail.split('：')
            item[detail[0]] = detail[1]
        item_jsn = json.dumps(item)
        item_jsn = item_jsn.replace('\'','\\\'')
        item_jsn = item_jsn.replace('\"','\\\"')
        item_jsn = item_jsn.replace('\u','\\\u')
        item_jsn = item_jsn.replace('\\n','')

        item = CommenItem()
        item['lable'] = u'jd_detail'
        item['body'] = item_jsn

        yield item

    def getPrice(slef, response):
        print response.body.replace(',', ',\n')
