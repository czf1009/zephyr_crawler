# coding : utf8
import os
import random
import requests
from user_agents import agents
from lxml import etree
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
from twisted.web._newclient import ResponseNeverReceived
import math
import threading
import time
import logging

from connect_mysql import connect_mysql

logger = logging.getLogger(__name__)

class UserAgentMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class ProxyMiddleware(object):
    # change a new proxy when this error occu
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError,
                         ResponseNeverReceived, ConnectError, ValueError)

    def __init__(self):
        # the minium proxy number when restart fetch proxy
        self.proxys_min = 10
        # request.meta["dont_redirect"] = True  # sometimes proxy will redirect
        # to a strange url
        self.test_thread_num = 30
        # currently used proxy's index
        self.proxys_index = -1
        # connect Mysql
        self.conn, self.cur = connect_mysql()
        # if last update time is update_time/min ago then update proxy
        self.update_time = 30
        # last update time
        self.last_update_time = self.get_last_update_time()

    # get a root node for a url
    def get_url_xpath(self, url):
        r = requests.get(url)
        return etree.HTML(r.content)

    # crawl proxy from https://www.us-proxy.org
    def crawl_proxy_usproxy(self):
        root = self.get_url_xpath('https://www.us-proxy.org/')
        proxys = root.xpath('//table[@id="proxylisttable"]/tbody/tr')
        for proxy_cel in proxys:
            list_proxy = proxy_cel.xpath('td/text()')
            dict_proxy = {}
            dict_proxy['ip'] = list_proxy[0]
            dict_proxy['port'] = list_proxy[1]
            if list_proxy[6] == 'yes':
                dict_proxy['https'] = 1
            else:
                dict_proxy['https'] = 0
            self.add_proxy(dict_proxy)

    # crawl proxy from http://www.kxdaili.com
    def crawl_proxy_kxdaili(self):
        for i in range(1, 11):
            root = self.get_url_xpath(
                'http://www.kxdaili.com/ipList/%d.html#ip' % i)
            proxys = root.xpath('//table[@class="ui table segment"]/tbody/tr')
            for proxy_cel in proxys:
                list_proxy = proxy_cel.xpath('td/text()')
                list_proxy = proxy_cel.xpath('td/text()')
                dict_proxy = {}
                dict_proxy['ip'] = list_proxy[0]
                dict_proxy['port'] = list_proxy[1]
                # initial https
                dict_proxy['https'] = 0
                if 'HTTPS' in list_proxy[3]:
                    # is https
                    dict_proxy['https'] = 1
                    if 'HTTP' in list_proxy[3]:
                        # is http & https
                        dict_proxy['https'] = 2

                self.add_proxy(dict_proxy)

    # crawl proxy from url
    def crawl_proxy(self):
        self.crawl_proxy_usproxy()
        self.crawl_proxy_kxdaili()
        # print '\ncrawl proxy complete, now has %d active proxy.\n' %
        # self.count_active_proxy()

    # check is this ip in mysql
    def is_exist(self, ip):
        if self.cur.execute('select * from proxy where ip = \'%s\';' % ip):
            return True
        else:
            return False

    # check is need update proxy
    def is_need_update(self):
        if (time.time() - self.last_update_time) / 60 > self.update_time:
            print '\nlast_update is %d mins ago.\n' % ((time.time()-self.last_update_time)/60)
            return True
        else:
            return False

    # get last update time and set self.last_update_time
    def get_last_update_time(self):
        # get when is the last update time
        if self.cur.execute(
            '''SELECT last_update 
              FROM app_test.proxy where is_active=1 
              order by last_update DESC limit 1; '''):
            t = self.cur.fetchone()[0]
            # transfer datetime to time
            t = time.mktime(t.timetuple())
            return t
        else:
            print '\nGet update time error!\n'

    # add proxy into mysql which from crawl_proxy
    def add_proxy(self, proxy):
        if self.is_exist(proxy['ip']):
            self.update_proxy(proxy)
        else:
            self.insert_proxy(proxy)

    # update proxy
    def update_proxy(self, proxy):
        if self.cur.execute(
                '''UPDATE `app_test`.`proxy` 
                SET `port`=\'%s\',`https`=%d , `is_active`=1
                WHERE `ip`=\'%s\';''' % (proxy['port'], proxy['https'], proxy['ip'])):
            self.conn.commit()

    # insert proxy into mysql
    def insert_proxy(self, proxy):
        if self.cur.execute(
                '''INSERT INTO `app_test`.`proxy` (`ip`, `port`, `https`) 
                VALUES (\'%s\', \'%s\', %d);'''
                % (proxy['ip'], proxy['port'], proxy['https'])):
            self.conn.commit()
        else:
            print '\ninert proxy error.\n'

    # inactive proxy in mysql
    def inactive_proxy(self, ip):
        if self.cur.executemany('UPDATE `app_test`.`proxy` SET `is_active`=\'0\' WHERE `ip`=%s;', ip):
            self.conn.commit()
            print 'ip inactive: %s\n' % ip
        else:
            print '\ninactive_proxy faild.\nip:\n', ip, '\n'

    # get a proxy from mysql, is none return false
    # like:  https://xxx.xx.xxx.x:xxxx
    def get_proxy(self):
        proxy_num = self.count_active_proxy()
        # has proxy
        if proxy_num:
            # proxy_index + 1
            self.proxys_index = (self.proxys_index+1) % proxy_num
            if self.cur.execute('select ip,port,https from proxy where is_active = 1 limit %d,1;' % self.proxys_index):
                proxy_raw = self.cur.fetchone()
                proxy = '%s:%s' % (proxy_raw[0], proxy_raw[1])
                # is https
                if proxy[2]:
                    proxy = 'https://' + proxy
                else:
                    proxy = 'http://' + proxy
                return proxy
            else:
                print '\nget_proxy faild.\n'
                return False
        else:
            return False

    # get all active proxy from mysql, is none return false
    def get_all_proxy(self):
        if self.cur.execute('select ip,port,https from proxy where is_active = 1;'):
            proxys_raw = self.cur.fetchall()
            proxys = []
            for proxy_raw in proxys_raw:
                proxy = {}
                proxy['ip'] = proxy_raw[0]
                proxy['port'] = proxy_raw[1]
                proxy['https'] = proxy_raw[2]
                proxys.append(proxy)
            return proxys
        else:
            print '\nget_all_proxy faild.\n'
            return False

    # count active proxy
    def count_active_proxy(self):
        if self.cur.execute('select count(*) from proxy where is_active = 1;'):
            return self.cur.fetchone()[0]
        else:
            print '\nget count of active proxy failed.\n'

    # test is proxy can be used
    def test_proxy(self):
        threads = []
        # get all proxy
        proxys = self.get_all_proxy()
        part_num = int(math.ceil(len(proxys)) / self.test_thread_num)
        for i in range(self.test_thread_num):
            proxys_part = proxys[i*part_num: (i+1) * part_num]
            t = threading.Thread(
                target=self.test_proxy_thread, args=(proxys_part))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print '\nAfter test remain %d proxy active.\n' % self.count_active_proxy()

    def test_proxy_thread(self, *proxys_part):
        url_test = 'http://www.baidu.com/js/bdsug.js?v=1.0.3.0'
        inactive_ips = []
        for proxy in proxys_part:
            # set proxy
            ip_port = '%s:%s' % (proxy['ip'], proxy['port'])

            # not https
            if proxy['https'] != 1:
                proxies = {'http': ip_port}
            # not http
            if proxy['https'] != 0:
                proxies = {'https': ip_port}

            try:
                r = requests.get(url_test, proxies=proxies, timeout=5)
            except Exception as e:
                # print 'test fail: %s\n' % e
                inactive_ips.append([proxy['ip']])
        self.inactive_proxy(inactive_ips)

    def process_request(self, request, spider):
        '''
        #not need change proxy,then return
        if 'change_proxy' not in request.meta.keys():
            return

        request.meta['proxy'] = 'https://86.27.56.138:8080'
        return
        '''

        # not enough proxy or time out then crawl proxy
        if self.count_active_proxy() < self.proxys_min or self.is_need_update():
            self.last_update_time = time.time()
            self.crawl_proxy()
            self.test_proxy()

        '''
        # remove invalid proxy
        if 'proxy' in request.meta.keys():
            self.inactive_proxy(request.meta['proxy'])
            del request.meta['proxy']
        '''

        # set proxy
        proxy = self.get_proxy()
        if proxy:
            request.meta['proxy'] = proxy
        else:
            # reset index
            self.proxys_index = -1

        # del request.meta['change_proxy']

        if 'proxy' in request.meta.keys():
            logger.info('use proxy:%s\n' % request.meta['proxy'])

    def process_response(self, request, response, spider):
        print '\nprocess_reaponse\nresponse.status: %d\n' % response.status
        # check response.status
        if response.status != 200 \
            and (not hasattr(spider, 'website_possible_httpstatus_list')
                 or response.status not in spider.website_possible_httpstatus_list):
            ip = request.meta['proxy'].split(':')[1]
            ip = ip.replace('//', '')
            self.inactive_proxy([[ip]])
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        print '\nprocess_exception\n'
        if isinstance(exception, self.DONT_RETRY_ERRORS):
            ip = request.meta['proxy'].split(':')[1]
            ip = ip.replace('//', '')
            self.inactive_proxy([[ip]])
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request


if __name__ == '__main__':
    print '============================='
    proxyMiddleware = ProxyMiddleware()
    proxyMiddleware.crawl_proxy()
    # proxyMiddleware.test_proxy()
    # proxyMiddleware.inactive_proxy([['104.168.151.65']])
    # print proxyMiddleware.is_need_update()
