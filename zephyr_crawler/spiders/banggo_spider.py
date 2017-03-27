#coding:utf8
import scrapy
from zephyr_crawler.items import GoodItem
from zephyr_crawler.items import CommenItem
from scrapy.shell import inspect_response
import json
import re
###

class BanggoSpider(scrapy.Spider):
    name = "banggo"
    allowed_domains = ["banggo.com"]
    start_urls = [
        'http://search.banggo.com/search/a_a.shtml?avn=1&currentPage=1',
        # 'http://www.banggo.com/goods/819647.shtml'
        # 'http://www.banggo.com/goods/882249.shtml',
        # 'http://www.banggo.com/goods/247002.shtml',
        # 'http://www.banggo.com/goods/225049.shtml',
        # 'http://www.banggo.com/goods/816757.shtml',
        # 'http://www.banggo.com/goods/247038.shtml',
        # 'http://search.banggo.com/brand/a_a_a_LEVI-S.shtml'
        # 'http://search.banggo.com/search/a_a.shtml?word=adidas'
    ]
    custom_settings = {
        'COOKIES_DEBUG': False,
        'COOKIES_ENABLED': False,
        #'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        # 'REDIRECT_ENABLED': False,
        # 'HTTPERROR_ALLOWED_CODES': '302',
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {
            'zephyr_crawler.pipelines.CommenPipeline': 500,
            # 'zephyr_crawler.pipelines.BanggoPipeline': 300,
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
        yield scrapy.Request(url=response.url, callback=self.next)
        # yield scrapy.Request(url=response.url, callback=self.getItem)

    def next(self, response):
        if not response.body:
            inspect_response(response, self)
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        # print response.headers,'\n\n\n'

        '''
        for li in response.xpath('//div[@class="mbshop_pdList"]/ul/li'):
            good = GoodItem()

            good['tag'] = li.xpath('a[2]/em/text()').extract_first()

            span = li.xpath('span')
            good['brand_name'] = span[0].xpath('a/text()').extract_first()
            good['name'] = span[1].xpath('a/text()').extract_first()
            good['price'] = span[2].xpath('b/text()').extract_first()
            good['link'] = li.xpath('a[1]/@href').extract_first()

            yield good
        '''
        for li in response.xpath('//div[@class="mbshop_pdList"]/ul/li'):
            link = li.xpath('a[1]/@href').extract_first()
            yield scrapy.Request(link, callback=self.getItem)

        next_url = response.xpath(u'//a[text()="下一页"]/@href').extract_first()
        next_url = response.urljoin(next_url)

        #print u'\nNow page is:',next_url

        yield scrapy.Request(next_url, callback=self.next)

    def getItem(self,response):

        #print u'\nNow url is:',response.url

        #Get target cel
        for i in response.xpath("//script/text()").extract():
            if 'p_zp_prodstype' in i:
                cel = re.search('{[\s\S]*}',i,0).group(0)
                break
        #Delete commented out code
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

        # print '\n\n',cel,'\n\n'
        
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

        # body['description'] = ""
        # body['description'] = body['description'].replace('『','')
        # body['description'] = body['description'].replace('』','')
        # body['description'] = body['description'].replace('！','')
        # print ('\n\ndescription',body['description'].decode('utf8'))
        # print 'description',body['description'].decode('utf8')

        #Transfer meaning
        body_jsn = json.dumps(body)
        body_jsn = body_jsn.replace('\'','\\\'')
        body_jsn = body_jsn.replace('\"','\\\"')
        body_jsn = body_jsn.replace('\u','\\\u')
        # body_jsn = body_jsn.replace('.','\.')
        # body_jsn = body_jsn.replace('%','\%')
        body_jsn = body_jsn.replace('\\n','')


        #Test
        # print '\n\nbody\n'
        # for i,j in body.items():
        #     print i,':',j
        # body['description'] = body['description'].replace('\n','')
        # print ('',body['description'])
        # print '\n\nbody_jsn:\n',re.search('description[^,]*?,',body_jsn).group(0),'\n\n'


        item = CommenItem()
        item['lable'] = u'good'
        item['body'] = body_jsn


        yield item
