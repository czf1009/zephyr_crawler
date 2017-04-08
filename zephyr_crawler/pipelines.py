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
        print u'\n\n程序耗时：' + str((time.time()-self.t)/60) + u' 分'

    def process_item(self, item, spider):
        self.enter_item(item['lable'],item['body'])
        return item


    def enter_item(self,lable,body):
        if self.cur.execute('insert into common(`lable`,`body`) values(\'%s\',\'%s\');' % (lable,body)):
            self.conn.commit()
        else:
            print '\n\ninsert data ERROR!!!'        


class JdCommentPipeline(object):
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
        print u'\n\n程序耗时：' + str((time.time()-self.t)/60) + u' 分'

    def process_item(self, item, spider):
        self.enter_item(item['comment_id'],item['ware_id'],item['comment_data'],item['comment_date'])
        return item

    def enter_item(self,comment_id,ware_id,comment_data,comment_date):
        comment_data = comment_data.replace('\'','\\\'')
        comment_data = comment_data.replace('\"','\\\"')
        comment_data = comment_data.replace('\u','\\u')
        comment_data = comment_data.replace('\\n','')
        if self.cur.execute('''INSERT INTO `app_test`.`jd_comment` 
            (`comment_id`, `ware_id`, `comment_data`, `comment_date`) 
            values(\'%s\',\'%s\',\'%s\',\'%s\');''' % (comment_id,ware_id,comment_data,comment_date)):
            self.conn.commit()
        else:
            print '\n\ninsert data ERROR!!!'        
