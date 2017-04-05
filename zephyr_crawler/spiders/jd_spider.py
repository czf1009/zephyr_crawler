# coding:utf8
import scrapy
from zephyr_crawler.items import CommonItem
from scrapy.shell import inspect_response
import json
import re
###


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = [
        "jd.com",
        'p.3.cn',    # price json
        'm.360buyimg.com',   # json  from    m.jd.com
    ]
    start_urls = [
        # 'https://list.jd.com/list.html?cat=9987,653,655'
        'https://so.m.jd.com/ware/searchList.action?_format_=json&stock=0&sort=&&page=1&keyword=手机'
        # 'https://item.jd.com/4139518.html'
        # 'https://item.jd.com/10921539206.html'
    ]
    custom_settings = {
        # 'COOKIES_DEBUG': True,
        # 'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'DEPTH_LIMIT': 0,
        # 'DOWNLOAD_DELAY': 1,
        # 'REDIRECT_ENABLED': True,
        # 'HTTPERROR_ALLOWED_CODES': [302,]
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
        # https://m.jd.com
        page_url = 'https://so.m.jd.com/ware/searchList.action?_format_=json&stock=0&sort=&&page=%d&keyword=手机'
        value  =json.loads(response.body)['value']
        wareList1 = json.loads(value)['wareList']
        page_num = self.get_page(wareList1['wareCount'])
        for i in range(1,page_num+1):
            url = page_url % i
            yield scrapy.Request(url=url, callback=self.catelog)

        # https://www.jd.com
        '''
        page_num = int(re.search('共<b>(\d*?)</b>页',response.body).group(1))
        cookies = {
            '__jda':'122270672.1886363307.1479022584.1491309048.1491311168.37',
            ' __jdu':'1886363307',
            ' TrackID':'1-A5W_DvLIjqqHoYqho9Sm2hd2TMFkl2ce4-clEGxxCjJOIwQwdrJPo_ceSCiadUOBYAggS3EusQDH9gp8YsMKYmGG8mQVwNG0CY6YfcnHu7BI8foOhCtaSAo7I5_mjGB',
            ' pinId':'pGlmQysu0EYFQIdj_tVFObV9-x-f3wj7',
            ' ipLoc-djd':'1-72-2799-0',
            ' __jdv':'122270672|dmp|dmp_154|cpc|dmp_154_474052_d49872e478084cfb6762f23b8ed61dd16ab34_1490451014|1490451014091',
            ' ipLocation':'%u5317%u4EAC',
            ' unick':'jd_132668ldx',
            ' _tp':'mESLajU9pSYlArGqpoEIdLmceWzTd1%2BIobXpkx%2BOOq8%3D',
            ' _pst':'jd_4433487821be9',
            ' user-key':'12693b71-6adf-4843-b4c0-8424d0ce94b9',
            ' cn':'0',
            ' listck':'c9c09e9498e561cb141d94fb7e3e8a33',
            ' dmpjs':'dmp-d433810fe34a16c8d3fff324144db7928043683',
            ' mt_xid':'V2_52007VwMbW1paVVgdSB9sDGACQgAIWVZGGhkRWBliABNQQQhSCR5VGFlWY1BBAlVQBl5MeRpdBWEfE1BBWlNLHEoSXQNsAxViX2hSah9IHFoEbgAXWm1YUVkd',
            ' __jdc':'122270672',
            ' __jdb':'122270672.10.1886363307|37.1491311168',
            ' _jrda':'1',
            ' _jrdb':'1491311217896',
            ' 3AB9D23F7A4B3C9B':'CKH7NYH65DLNEYIZJNWP6W4RDSFCIC5ALY65DMPJ37EA27V7KHJLSUYZ4QV3ZZGJLJVJAFWRRPVTDKIEN3XISRDDCE',
            ' ceshi3.com':'000'
        }
        for i in range(6,7):
            url = 'https://list.jd.com/list.html?cat=9987,653,655&page=%d&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main' % i
            yield scrapy.Request(url=url, cookies=cookies, callback=self.catelog)
        '''


    def get_page(self,item_num):
        return int((item_num+10-1)/10)
     

    def catelog(self, response):
        #  test pc page category
        '''
        with open('test.html','w') as f:
            f.write(response.body)
            print '\nresponse.url:%s\n\
            eate file test.html\n\
            response.headers:%s\n\
            response.meta:%s\n' \
            % (response.url,response.headers,response.meta)
        return
        '''
        # Crawl itempage from catelog

        # If bannde then change proxy
        if not response.body:
            inspect_response(response, self)
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        # https://m.jd.com
        value  =json.loads(response.body)['value']
        wareList1 = json.loads(value)['wareList']
        items = wareList1['wareList']
        for i in items:
            i = json.dumps(i)
            i = i.replace('\'','\\\'')
            i = i.replace('\"','\\\"')
            i = i.replace('\u','\\u')
            i = i.replace('\\n','')
            item =CommonItem()
            item['lable'] = u'jd'
            item['body'] = json.dumps(i)     
            yield item
 
        '''
        # used when crawl from pc page
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

        item = CommonItem()
        item['lable'] = u'jd_detail'
        item['body'] = item_jsn

        yield item
    '''