# coding:utf8
import scrapy
from zephyr_crawler.items import JdCommentItem
from scrapy.shell import inspect_response
import json
import re
from zephyr_crawler.connect_mysql import connect_mysql
import logging
###

logger = logging.getLogger(__name__)
class JdCommentSpider(scrapy.Spider):
    name = "jd_comment"
    allowed_domains = [
        "jd.com",
        'storage.360buyimg.com',
        'jd.hk'
    ]
    start_urls = [
        # 'https://www.baidu.com'
        # 'https://list.jd.com/list.html?cat=9987,653,655'
        # 'https://so.m.jd.com/ware/searchList.action?_format_=json&stock=0&sort=&&page=1&keyword=手机'
        # 'https://item.jd.com/4139518.html'
        # 'https://item.jd.com/10921539206.html'
        # 'https://m.jd.com/'
        'https://item.m.jd.com/product/10921539206.html',
        # 'https://mitem.jd.hk/ware/view.action?wareId=1965454177&cachekey=2127aa99b875ed7f3813b40ec2f0304e'
        # 'https://mitem.jd.hk/ware/view.action?wareId=1965454177&cachekey=4758942049d3c727312910e8670c10f1'
        # 'https://so.m.jd.com/ware/search.action?keyword=手机'
        # 'https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=3499302&offset=2&num=10&type=0&checkParam=LUIPPTP&evokeType='
    ]
    custom_settings = {
        # 'COOKIES_DEBUG': True,
        'COOKIES_ENABLED': True,
        'DUPEFILTER_DEBUG': True,
        'ROBOTSTXT_OBEY': False,
        'DEPTH_LIMIT': 0,
        'DOWNLOAD_DELAY': 1,
        'REDIRECT_ENABLED': True,
        'HTTPERROR_ALLOWED_CODES': [0,302],
        # 'DONT_FILTER': Ture
        'ITEM_PIPELINES': {
            'zephyr_crawler.pipelines.JdCommentPipeline': 299
        },
    }

    def __init__(self):
        self.conn,self.cur = connect_mysql()

    def parse(self, response):
        # self.get_comment_page('10941037480')
        # comment_url = 'https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=10941037480&offset=%d&num=10&type=0&checkParam=LUIPPTP&evokeType='

        # wareid = '10941037480'
        # url = 'https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=%s&offset=1&num=1&type=0&checkParam=LUIPPTP&evokeType=' % wareid
        # yield scrapy.Request(url=url,meta={'wareid':wareid},callback=self.get_comment_total_page)

        # print '\nresponse.body:%s\n' %response.body
        # print response.headers['Set-Cookie']
        # print type(response.headers['Set-Cookie'])
        # for  i,j in response.headers.items():
        #     print i,':',j
        # foo = response.headers['Set-Cookie']
        # values = {k.strip():v for k,v in re.findall(r'(.*?)=(.*?);', foo)}
        # print '\n',values
        
        wareids = self.get_wareids()
        if not wareids:
            logger.error('There is no id witch date is today!!')
            return
        
        # yield scrapy.Request(url=url,headers={'referer':None},callback=self.item)

        url = 'https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=%s&offset=1&num=1&type=0&checkParam=LUIPPTP&evokeType='
        for wareid in wareids:
            wareid = wareid[0]
            yield scrapy.Request(url=url%wareid,meta={'wareid':wareid},dont_filter=True,callback=self.get_comment_total_page)

        # yield scrapy.Request(url='https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=%s&offset=1&num=1&type=0&checkParam=LUIPPTP&evokeType='%11732620240,meta={'wareid':11732620240},dont_filter=True,callback=self.get_comment_total_page)



    def get_comment_total_page(self,response):
        # print '\nurl:%s\nbody:\n%s' %(url,response.body)
        # yield scrapy.Request(url = url ,callback=self.print_body)
        # return
        # print 'response.body:%s' %response.body
        
        jsn = json.loads(response.body)
        total_page = jsn['totalPage']
        wareid = response.meta['wareid']

        comment_url = '''https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=%s&offset=%s&num=10&type=0&checkParam=LUIPPTP&evokeType='''
        meta = {
            'total_page':total_page,
            'wareid':wareid,
            'now_page':1 
        }

        logger.info('Wareid:%s    Total_page:%s,start crawl comment.' % (wareid,total_page))
        if jsn['commentCount'] == 0:
            logger.error('This ware(%s) has no comment!!\n' % wareid)
            yield scrapy.Request(url=comment_url%(wareid,1),meta=meta,dont_filter=True,callback=self.comment_page)

        yield scrapy.Request(url=comment_url%(wareid,1),meta=meta,dont_filter=True,callback=self.comment_page)

    def comment_page(self,response):
        # If bannde then change proxy
        if not response.body:
            logger.error('This page(%s) has no body' % response.url)
            return
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req


        total_page = response.meta['total_page']
        wareid = response.meta['wareid']
        now_page = response.meta['now_page'] + 1

        jsn = json.loads(response.body)
        jsn = jsn['wareDetailComment']
        items = jsn['commentInfoList']

        if not items:
            logger.error('This page(%s) has no items' %response.url)
        for item_jsn in items:
            # if self.is_exist(item_jsn['commentId']):
            #     # this comment has already crawled then stop crawl this ware
            #     return
            item = JdCommentItem() 
            item['comment_id'] = item_jsn['commentId']
            item['comment_data'] = item_jsn['commentData']
            item['comment_date'] = item_jsn['commentDate']
            item['ware_id'] = wareid
            print item
            # yield item

        '''
        if now_page < total_page + 1:
            url = 'https://item.m.jd.com/newComments/newCommentsDetail.json?wareId=%s&offset=%s&num=10&type=0&checkParam=LUIPPTP&evokeType='

            meta = {
                'total_page':total_page,
                'wareid':wareid,
                'now_page':now_page
            }
            yield scrapy.Request(url = url%(wareid,now_page+1),meta=meta,dont_filter=True,callback=self.comment_page)
        '''


        '''        
        # print '\nget_comment.response.body:%s\n' % response.body
        # print 'response.headers:\n%s' % response.headers

        # Crawl itempage from catelog

        # If bannde then change proxy
        if not response.body:
            inspect_response(response, self)
        elif response.body == "banned":
            req = response.request
            req.meta["change_proxy"] = True
            yield req

        # https://item.m.jd.com/newComments/newCommentsDetail.json
        value =json.loads(response.body)['value']
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



    def get_wareids(self):
        # Get wareid which crawl by today
        if self.cur.execute('''
            SELECT ware_id
            FROM app_test.jd 
            WHERE to_days(date) = to_days(now())
            order by ware_id;'''):
            return self.cur.fetchall()
        else:
            print '\n\nget data ERROR!!!'    

    def get_last_comment_date(self,wareid):
        # Get wareid which crawl by today
        if self.cur.execute('''
            SELECT comment_date
            FROM app_test.jd_comment 
            WHERE ware_id = 1
            order by comment_date
            DESC
            LIMIT 1;'''):
            return self.cur.fetchone()
        else:
            print '\n\nget_last_comment_date ERROR!!!' 


    def is_exist(self,comment_id):
        #is comment exist
        if self.cur.execute('''
            SELECT *
            FROM app_test.jd_comment 
            WHERE comment_id = %s;''' % comment_id):
            return True
        else:
            return False      

    def print_body(self,response):        
        with open('test.json','w') as f:
            tmp = response.body.replace(',',',\n')
            tmp = tmp.replace('{','{\n')
            tmp = tmp.replace('[','\n[\n')
            tmp = tmp.replace(']','\n]\n')
            tmp = tmp.replace('}','}\n')
            f.write(tmp)  
        return
        # print '\nitem.response.body:%s\n' % response.body
        # print 'item.response.headers:\n%s' % response.headers
        # yield scrapy.Request(url=comment_url+post_data,callback=self.get_comment)
        pass


