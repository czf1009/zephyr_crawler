# -*- coding: utf-8 -*-
import time
import MySQLdb
from scrapy.exceptions import DropItem
import sys
from connect_mysql import connect_mysql

class CommonPipeline(object):
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
        if self.cur.execute('insert into common(`lable`,`body`) values(\'%s\',\'%s\');' % (lable,body)):
            self.conn.commit()
        else:
            print '\n\ninsert data ERROR!!!'        
