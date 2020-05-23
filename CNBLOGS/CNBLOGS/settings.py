# -*- coding: utf-8 -*-

# Scrapy settings for CNBLOGS project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'CNBLOGS'

SPIDER_MODULES = ['CNBLOGS.spiders']
NEWSPIDER_MODULE = 'CNBLOGS.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CNBLOGS (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
#     'referer': 'https://www.cnblogs.com/',
#     'Connection':'keep-alive',
#     'Cookie':'_ga=GA1.2.1582462423.1556498661; __gads=ID=7732b127e565176e:T=1556498649:S=ALNI_MZY2IxhXft_C8b2XCUy8Sz1UknXlw; _gid=GA1.2.1160015034.1568777657; _gat=1',
#     'Host' :'Host: www.cnblogs.com',
# }
DEFAULT_REQUEST_HEADERS ={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    #'referer': 'https://www.cnblogs.com/',
    'cookie': '_ga=GA1.2.293546808.1533785613; __gads=ID=56449782d311309e:T=1539047323:S=ALNI_MacmTqGVvA4eL7YiqL8_nwXghoUyw; Hm_lvt_d8d668bc92ee885787caab7ba4aa77ec=1541382326; Hm_lvt_856199a1621b66a38171774e55106e2d=1542965148; Hm_lvt_8875c662941dbf07e39c556c8d97615f=1545385679; UM_distinctid=16cd5cd1e1f2fa-0a996c3f8efc11-5701732-1fa400-16cd5cd1e2110db; CNZZDATA3347352=cnzz_eid%3D1581263208-1566952032-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1566952032; CNZZDATA1278017250=922124043-1568183087-https%253A%252F%252Fwww.baidu.com%252F%7C1568183087; _gid=GA1.2.428786528.1568599799; CNZZDATA1262561745=1938244999-1568680000-https%253A%252F%252Fwww.baidu.com%252F%7C1568680000; CNZZDATA1255738818=804621395-1567645041-%7C1568684659; CNZZDATA1269983936=1027557775-1568767763-https%253A%252F%252Fwww.baidu.com%252F%7C1568767763; CNZZDATA5244184=cnzz_eid%3D1292640379-1568774055-https%253A%252F%252Fwww.cnblogs.com%252F%26ntime%3D1568774055; CNZZDATA1000071539=1888270853-1568771976-https%253A%252F%252Fwww.cnblogs.com%252F%7C1568771976; _gat=1',
}
HTTPERROR_ALLOWED_CODES = [405]
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'CNBLOGS.middlewares.CnblogsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'CNBLOGS.middlewares.CnblogsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'CNBLOGS.pipelines.CnblogsPipeline': 300,
}
DOWNLOAD_TIMEOUT = 600
DOWNLOAD_DELAY = 0.2
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
