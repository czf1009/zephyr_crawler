#coding:utf8
import scrapy
from zephyr_crawler.items import CommonItem
from scrapy.shell import inspect_response
import json
import re
###

class BanggoSpider(scrapy.Spider):
    name = "banggo"
    allowed_domains = ["banggo.com"]
    start_urls = [
        'http://search.banggo.com/search/a_a.shtml?avn=1&currentPage=1'
    ]
    custom_settings = {
        'COOKIES_DEBUG': False,
        'COOKIES_ENABLED': False,
        #'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        # 'REDIRECT_ENABLED': False,
        # 'HTTPERROR_ALLOWED_CODES': '302',
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'zephyr_crawler.pipelines.CommonPipeline': 500
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
        #　Get total page num
        total_page_num = response.xpath(u'//a[text()="尾 页"]/@href').extract_first()
        total_page_num = int(re.search('currentPage=(\d*)',total_page_num).group(1))
        for i in range(1,total_page_num+1):
            url = 'http://search.banggo.com/search/a_a.shtml?avn=1&currentPage=%d' % i
            yield scrapy.Request(url=url, callback=self.catelog)

    def catelog(self, response):
        if not response.body:
            inspect_response(response, self)
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        for li in response.xpath('//div[@class="mbshop_pdList"]/ul/li'):
            link = li.xpath('a[1]/@href').extract_first()
            yield scrapy.Request(link, callback=self.getItem)


    def getItem(self,response):

        if response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        #Get target cel
        for i in response.xpath("//script/text()").extract():
            if 'p_zp_prodstype' in i:
                cel = re.search('{[\s\S]*}',i,0).group(0)
                break
        #Delete note in code
        for i in re.findall(" //.*",cel):
            cel = cel.replace(i,'')
        #Get stock number
        stock = re.search('stock: "(\d*?)",',cel).group(1)
        #Get brand
        brand = re.search(
            '([^ ]*?) ',
            response.xpath(
                '//h5[@class="mbshop_detail_goods_title"]/text()'
            ).extract_first()
        ).group(1)
        #Delete last ","
        cel = cel.replace(re.findall('.*,',cel)[-1],re.findall('.*,',cel)[-1][:-1])
        #Get target data
        cel = re.search('p_zp_prods:([^}]*})',cel).group(1)

        
        # Transfer " to \" in description
        desc = re.search('description":.*?"([\s\S]*?)",',cel)
        if desc:
            description = desc.group(1)
            description_tmp = description.replace('\"','\\\"')
            cel = cel.replace(description,description_tmp)

        body = json.loads(cel,strict=False)
        #Insert stock number and brand
        body[u'stock'] = stock
        body[u'brand'] = brand

        #Transfer meaning
        body_jsn = json.dumps(body)
        body_jsn = body_jsn.replace('\'','\\\'')
        body_jsn = body_jsn.replace('\"','\\\"')
        body_jsn = body_jsn.replace('\u','\\\u')
        body_jsn = body_jsn.replace('\\n','')

        item = CommonItem()
        item['lable'] = u'good'
        item['body'] = body_jsn


        yield item
