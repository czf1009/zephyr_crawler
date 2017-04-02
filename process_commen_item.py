#coding:utf8
import time
import MySQLdb
import sys
import json
from zephyr_crawler.connect_mysql import connect_mysql

# Commen processor
class CommenItem(object):
    def __init__(self):
        self.t = 0
        self.t = time.time()
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.conn,self.cur = connect_mysql()

    def close_process(self):
        self.cur.close()
        self.conn.close()
        print u'process_commen_item耗时：' + str(time.time()-self.t) + u' 秒'

    ############testing   limit just get good lable item

    def process_item(self):
        good = ''
        jd = ''
        items = self.item_get()
        print '读取数据完成，开始处理。'
        items_len = len(items)
        print '数据总量为：',items_len
        for index,item in enumerate(items,1):
            if index%1000 == 0:
                print '进度： ',items_len,'/',index
            if item[1] == 'good':
                if not good:
                    good = CommenGoodItem(self.cur,self.conn)
                item_body = json.loads(item[2])
                good.item_insert(item_body,item[3])
            elif item[1] == 'jd':
                if not jd:
                    jd = CommenJdItem(self.cur,self.conn)
                item_body = json.loads(item[2])
                item_body = json.loads(item_body)
                jd.item_insert(item_body,item[3])
            else:
                print 'Error lable: ',item[1]
                print 'id: ',item['id'],'\n\n'
        self.item_del(len(items))
        self.close_process()

    #Get items
    def item_get(self):
        if self.cur.execute('select id,lable,body,date from commen order by date;'):
            return self.cur.fetchall()
        else:
            print '\n\ninsert data ERROR!!!'    

    #  Now just delete good lable item
    def item_del(self,items_len):
        if self.cur.execute('delete from commen;') == items_len:
            self.conn.commit()
            print "\nDelete commen complite.\n"
        else:
            print "Items_len: " , items_len
            print "Error number when delete commen!!\n"


######################### Good processor
class CommenGoodItem(object):
    def __init__(self,cur,conn):
        self.cur = cur
        self.conn = conn

    def item_insert(self,item,date):
        #process item type & specia charactor
        item = self.item_initial(item)

        if not self.is_exist(item['outerid']):
            self.insert_good(item,date)
        else:
            self.update_good_date(item,date)

        self.insert_price_stock(item,date)
        return
    
    def item_initial(self,item):
        #Initial value type
        ids = ['categoryID','subCategoryID','ThirdCategoryID']
        for id in ids:
            if id in item.keys():
                if item[id]:
                    item[id] = int(item[id])
                else:
                    item[id] = 0
        item['price'] = float(item['price'])
        item['value'] = float(item['value'])
        item['vipprice'] = float(item['vipprice'])
        item['svipprice'] = float(item['svipprice'])
        if item['stock']:
            item['stock'] = int(item['stock'])
        else:
            item['stock'] = 0
        #Translate special caractor
        names = ['name','brand','categoryName','subCategoryName','ThridCategoryName','description']
        for name in names:
            if name in item.keys():
                item[name] = item[name].replace("\'","\\\'")
        return item


    #insert good
    def insert_good(self,item,date):
        #print('',item['name'],item['categoryName'])
        brand_id = self.check_brand(item['brand'])[0]
        self.check_category(item['categoryID'],item['categoryName'])
        self.check_category(item['subCategoryID'],item['subCategoryName'])
        self.check_category(item['ThirdCategoryID'],item['ThirdCategoryName'])
        if self.cur.execute('''
             insert into good(
                `good_id`,
                `good_name`,
                `brand_id`,
                `link`,
                `category_id`,
                `category_id_sub`,
                `category_id_third`,
                `image`,
                `description`,
                `date_create`,
                `date_last`
            ) values(\'%s\',\'%s\',%d,\'%s\',%d,%d,%d,\'%s\',\'%s\',\'%s\',\'%s\');''' 
            % (item['outerid'],item['name'],brand_id,item['loc'],item['categoryID'],item['subCategoryID'],item['ThirdCategoryID'],item['image'],item['description'],date,date)
        ):
            self.conn.commit()
        else:
            print 'insert good error\n'

    def update_good_date(self,item,date):
        self.cur.execute('UPDATE `app_test`.`good` SET `date_last`=\'%s\' WHERE `good_id`=\'%s\';' % (date,item['outerid']))
        self.conn.commit()
        return

    #insert price&stock
    def insert_price_stock(self,item,date):
        if self.cur.execute('''
             insert into price_stock(
                `good_id`,
                `price`,
                `price_original`,
                `price_vip`,
                `price_svip`,
                `stock`,
                `date`
            ) values(\'%s\',%f,%f,%f,%f,%d,\'%s\');''' 
            % (item['outerid'],item['price'],item['value'],item['vipprice'],item['svipprice'],item['stock'],date)
        ):
            self.conn.commit()
        else:
            print 'insert price&stock error\n'

    #Existed in good
    def is_exist(self, id):
        if self.cur.execute('select * from good where good_id = \'%s\''% id):
            return 1
        else:
            return 0


    #check is exist in brand
    def check_brand(self, brand_name):
        if not self.cur.execute('select brand_id from brand where brand_name = \'%s\';' % brand_name):
            if self.cur.execute('insert into brand(`brand_name`) values(\'%s\');' % brand_name):
                self.conn.commit()
            else:
                print 'insert brand error\n'
            self.cur.execute('select brand_id from brand where brand_name = \'%s\';' % brand_name)
        return self.cur.fetchone()
        

    #check is exist in category
    def check_category(self, category_id,category_name):
        if not self.cur.execute('select * from category where category_id = %d;' % category_id):
            if self.cur.execute('insert into category(`category_id`,`category_name`) values(%d,\'%s\');' % (category_id,category_name)):
                self.conn.commit()
            else:
                print 'insert category error\n'
        return

################################ jd processor
class CommenJdItem(object):
    def __init__(self,cur,conn):
        self.cur = cur
        self.conn = conn


    def item_insert(self,item,date):
        #process item type & specia charactor
        item = self.item_initial(item)
        self.insert_jd(item,date) 
        return
    
    def item_initial(self,item):
        #Initial value type
        item['wareId'] = int(item['wareId'])
        item['jdPrice'] = float(item['jdPrice'])
        item['wname'] = item['wname'].replace("\'","\\\'")
        return item


    #insert jd
    def insert_jd(self,item,date):
        if self.cur.execute('''
             insert into jd(
                `ware_id`,
                `wname`,
                `jd_price`,
                `date`
            ) values(%d,\'%s\',%f,\'%s\');''' 
            % (item['wareId'],item['wname'],item['jdPrice'],date)
        ):
            self.conn.commit()
        else:
            print 'insert jd error\n'



if __name__ == '__main__':
    commenItem = CommenItem()
    commenItem.process_item()
