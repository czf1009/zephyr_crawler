# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import MySQLdb
from scrapy.exceptions import DropItem
import sys
from connect_mysql import connect_mysql


class EncodingPipeline(object):

    def __init__(self):
        # self.file = open('items.jl', 'wb')
        self.t = 0

    def open_spider(self, spider):
        self.t = time.time()

    def close_spider(self, spider):
        print u'\n\nBanggo Spider 耗时：' + str(time.time()-self.t) + u' 秒'

    def process_item(self, item, spider):
        if item['title']:
            item['title'] = item['title'].encode('gbk')
        item['link'] = item['link']
        item['date'] = item['date']
        item['click_times'] = item['click_times']
        return item


class JinzhongPipeline(object):

    def __init__(self):
        self.t = 0
        try:
            self.conn = MySQLdb.connect(
                host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def open_spider(self, spider):
        self.t = time.time()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        print u'\n\n程序耗时：' + str(time.time()-self.t) + u' 秒'

    def process_item(self, item, spider):
        if not item['text']:
            return
        item['text'].encode('utf8')

        if self.is_exist(item['text']):
            # print item['text'], 'isExist!!!\n\n'
            raise DropItem(item['text'], 'isExist!!!\n\n')
        else:
            if self.cur.execute('insert into jinzhong(`text`) values(%s);', item['text']):
                self.conn.commit()
                return item['text']
            else:
                print '\n\ninsert data ERROR!!!'

    def is_exist(self, text):
        if self.cur.execute('select * from jinzhong where text = %s', text):
            return 1
        else:
            return 0


class BanggoPipeline(object):

    def __init__(self):
        self.t = 0
        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            self.conn = MySQLdb.connect(
                host='localhost', user='root', passwd='123456', db='banggo', port=3306, charset='utf8')
            self.cur = self.conn.cursor()
        except MySQLdb.Error, e:
            print 'Mysql Error %d: %s' % (e.args[0], e.args[1])

    def open_spider(self, spider):
        self.t = time.time()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        print u'\n\n程序耗时：' + str(time.time()-self.t) + u' 秒'

    def process_item(self, item, spider):
        if self.is_exist(item['link']):
            raise DropItem(item['name'],'is already existed!!!\n\n\n')

        tag_id = None
        if item['tag']:
            tag_id = int(self.check('tag',item['tag']))
        if item['brand_name']:
            brand_id = int(self.check('brand',item['brand_name'].replace('\'','\\\'')))
        name = item['name'].encode('utf8')
        price = item['price'].replace(u'\uffe5','')
        price = float(price)
        link = item['link']

        self.enter_item(tag_id,brand_id,name,price,link)
        return item
        re.replace("品牌：","brand")
        re.replace("款名：","good_name")
        re.replace("款号：","good_id")
        re.replace("分类：","category")
        re.replace("吊牌价：","price")
        re.replace("版型：","type")
        re.replace("季节：","season")
        re.replace("系列：","series")
        re.replace("性别：","sex")
        re.replace("品牌：","brand")
        re.replace("品牌：","brand")
        re.replace("品牌：","brand")

    def check(self, column, text):
        values = [column+'_id',column, column+'_name', text]
        if self.cur.execute('select '+values[0]+' from '+values[1]+' where '+values[2]+'=\''+values[3]+'\''):
            return self.cur.fetchone()[0]
        else:
            self.cur.execute('insert into '+values[1]+'(`'+values[2]+'`) values(\''+values[3]+'\')')
            self.conn.commit()
            self.cur.execute('select '+values[0]+' from '+values[1]+' where '+values[2]+'=\''+values[3]+'\'')
            return self.cur.fetchone()[0]

    # def is_exist(self, name,brand_name,tag_name,price):
    #     if self.cur.execute('''
    #                 select 
    #                     name,price,tag_name,brand_name
    #                 from 
    #                     good
    #                 left join
    #                     tag
    #                 on 
    #                     tag.tag_id = good.tag_id
    #                 left join
    #                     brand 
    #                 on 
    #                     brand.brand_id = good.brand_id
    #                 where
    #                     name='%s'
    #                 and
    #                     brand_name='%s'
    #                 and
    #                     tag_name='%s'
    #                 and
    #                     price=%f''' % (name,brand_name,tag_name,price)):
    #         return 1
    #     else:
    #         return 0


    def is_exist(self, link):
        if self.cur.execute('''
                    select 
                        *
                    from 
                        good
                    where
                        link='%s'
                    ''' % (link)):
            return 1
        else:
            return 0

    def enter_item(self,tag_id,brand_id,name,price,link):
        if tag_id:
            if self.cur.execute('insert into good(`tag_id`,`brand_id`,`name`,`price`,`link`) values(%d,%d,\'%s\',%f,\'%s\');' % (tag_id,brand_id,name,price,link)):
                self.conn.commit()
            else:
                print '\n\ninsert data ERROR!!!'
        else:
            if self.cur.execute('insert into good(`brand_id`,`name`,`price`,`link`) values(%d,\'%s\',%f,\'%s\');' % (brand_id,name,price,link)):
                self.conn.commit()
            else:
                print '\n\ninsert data ERROR!!!'           

class CommenPipeline(object):
    def __init__(self):
        self.t = 0
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.conn,self.cur = connect_mysql()

    def open_spider(self, spider):
        self.t = time.time()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
        print u'\n\n程序耗时：' + str(time.time()-self.t) + u' 秒'

    def process_item(self, item, spider):
        # item['body'] = item['body'.encode('utf-8')]
        self.enter_item(item['lable'],item['body'])
        return item


    def enter_item(self,lable,body):
        # print '\n\nbody',body,'\n\n'      #TEST
        if self.cur.execute('insert into commen(`lable`,`body`) values(\'%s\',\'%s\');' % (lable,body)):
            self.conn.commit()
        else:
            print '\n\ninsert data ERROR!!!'        
