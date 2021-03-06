# -*- coding: utf-8 -*-

# Scrapy-redis Settings
# 

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
# REDIS_URL = 'redis://172.31.238.60:6379'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Don't cleanup redis queues, allows to pause/resume crawls.
#SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

# ITEM_PIPELINES = {
#     'example.pipelines.ExamplePipeline': 300,
#     'scrapy_redis.pipelines.RedisPipeline': 400,
# }

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 429, 302, 403]
# DEPTH_PRIORITY = 2
RETRY_PRIORITY_ADJUST = +1

#DOWNLOAD_DELAY = 0.5

# Normal Settings
CONCURRENT_REQUESTS = 256

BOT_NAME = 'zephyr_crawler'

SPIDER_MODULES = ['zephyr_crawler.spiders']
NEWSPIDER_MODULE = 'zephyr_crawler.spiders'

DEPTH_LIMIT = 2

REDIRECT_ENABLED = False

DOWNLOAD_TIMEOUT = 10
RETRY_ENABLED = True
RETRY_TIMES = 30

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'zephyr_crawler.middlewares.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'zephyr_crawler.HttpProxyMiddleware.HttpProxyMiddleware': None,
    'zephyr_crawler.middlewares.AbuyunProxyMiddleware': None,
    'zephyr_crawler.middlewares.ProxyMiddleware': None
}

DEFAULT_REQUEST_HEADERS = {
    'accept': 'image/webp,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
}

ITEM_PIPELINES = {
   'zephyr_crawler.pipelines.CommonPipeline': 300,
}

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zephyr_crawler.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html


# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# 
AUTOTHROTTLE_ENABLED = True
# # The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# 
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
