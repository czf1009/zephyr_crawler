#coding:utf8
import time
import MySQLdb
import sys
import json
from zephyr_crawler.connect_mysql import connect_mysql

######################### PriceStockTable
class PriceStock(object):
    def __init__(self):
        self.t = 0
        self.t = time.time()
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.conn,self.cur = connect_mysql()

    #Get items
    def get_items(self):
        if self.cur.execute('''
            SELECT id,good_id, DATE_FORMAT(`date`, '%Y-%m-%d') as date_day 
            FROM app_test.price_stock 
            order by good_id,date;'''
            ):
            return self.cur.fetchall()
        else:
            print '\n\ninsert data ERROR!!!'

    def del_items(self,ids):
        if self.cur.executemany('delete from price_stock where id = %s;', ids):
            self.conn.commit()
            print "\nDelete price_stock complite.\n"
        else:
            print "Error happend when delete price_stock!!\n"

    def clean_data(self):
        dump_item_ids = []
        items = self.get_items()
        for index in range(1,len(items)):
            # same good_id and date_day
            if items[index][1] == items[index-1][1] and items[index][2] == items[index-1][2]:
                dump_item_ids.append([str(items[index][0])])
        print dump_item_ids
        self.del_items(dump_item_ids)
        self.cur.close()
        self.conn.close()
        print u'process_common_item耗时：' + str(time.time()-self.t) + u' 秒'



if __name__ == '__main__':
    priceStock = PriceStock()
    priceStock.clean_data()
