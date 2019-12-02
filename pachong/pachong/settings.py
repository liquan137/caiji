# -*- coding: utf-8 -*-

# Scrapy settings for pachong project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from django.core.wsgi import get_wsgi_application

PROXIES = [{"IP": "223.156.198.52", "Port": 19069}, {"IP": "1.57.193.66", "Port": 23180},
           {"IP": "182.98.37.142", "Port": 32810}, {"IP": "27.191.74.226", "Port": 41013},
           {"IP": "117.26.228.220", "Port": 37584}, {"IP": "223.240.229.190", "Port": 39148},
           {"IP": "180.155.159.44", "Port": 26110}, {"IP": "175.150.110.33", "Port": 41641},
           {"IP": "113.143.59.48", "Port": 36598}, {"IP": "113.237.228.81", "Port": 35195},
           {"IP": "117.92.131.157", "Port": 30204}, {"IP": "123.163.147.49", "Port": 14583},
           {"IP": "182.202.223.127", "Port": 42493}, {"IP": "121.237.148.245", "Port": 26752},
           {"IP": "113.237.187.251", "Port": 23685}, {"IP": "222.132.140.28", "Port": 15913},
           {"IP": "101.26.53.29", "Port": 37332}, {"IP": "39.72.51.115", "Port": 15158},
           {"IP": "121.205.177.81", "Port": 16854}, {"IP": "58.253.6.72", "Port": 41914},
           {"IP": "112.83.139.166", "Port": 42035}, {"IP": "123.190.136.102", "Port": 23759},
           {"IP": "115.223.166.137", "Port": 21149}, {"IP": "117.67.41.88", "Port": 33133},
           {"IP": "122.194.249.134", "Port": 38062}, {"IP": "125.123.66.4", "Port": 40154},
           {"IP": "219.136.190.89", "Port": 28231}, {"IP": "60.187.160.177", "Port": 0},
           {"IP": "121.61.182.81", "Port": 24757}, {"IP": "101.31.59.174", "Port": 30635},
           {"IP": "223.215.10.45", "Port": 17535}, {"IP": "183.141.34.19", "Port": 38145},
           {"IP": "153.35.227.32", "Port": 38215}, {"IP": "183.166.37.239", "Port": 30079},
           {"IP": "106.125.238.162", "Port": 13290}, {"IP": "117.44.24.245", "Port": 36627},
           {"IP": "27.156.142.28", "Port": 12368}, {"IP": "175.44.186.18", "Port": 36686},
           {"IP": "113.121.23.236", "Port": 37916}, {"IP": "122.194.249.242", "Port": 41254},
           {"IP": "110.248.90.125", "Port": 40911}, {"IP": "119.140.163.200", "Port": 12745},
           {"IP": "117.42.202.43", "Port": 15099}, {"IP": "27.191.77.37", "Port": 16814},
           {"IP": "101.22.194.229", "Port": 29286}, {"IP": "119.249.45.38", "Port": 37381},
           {"IP": "113.76.239.240", "Port": 52208}, {"IP": "119.184.155.182", "Port": 12783},
           {"IP": "27.43.109.231", "Port": 38655}, {"IP": "219.145.164.163", "Port": 17546},
           {"IP": "125.78.13.71", "Port": 40851}, {"IP": "58.253.14.171", "Port": 23974},
           {"IP": "114.106.151.86", "Port": 12020}, {"IP": "125.126.202.188", "Port": 13742},
           {"IP": "120.41.153.71", "Port": 21681}, {"IP": "60.17.200.87", "Port": 13469},
           {"IP": "113.103.53.8", "Port": 31911}, {"IP": "14.118.234.62", "Port": 12996},
           {"IP": "113.76.139.158", "Port": 31657}, {"IP": "117.95.40.193", "Port": 19725},
           {"IP": "125.86.166.193", "Port": 34641}, {"IP": "180.160.61.209", "Port": 32142},
           {"IP": "120.87.32.32", "Port": 14482}, {"IP": "117.88.5.229", "Port": 35446},
           {"IP": "119.138.195.150", "Port": 35954}, {"IP": "113.121.177.248", "Port": 27976},
           {"IP": "223.156.198.143", "Port": 18859}, {"IP": "125.94.165.114", "Port": 39171},
           {"IP": "124.94.187.132", "Port": 35668}, {"IP": "112.85.45.223", "Port": 23627},
           {"IP": "171.13.19.149", "Port": 20527}, {"IP": "125.86.166.254", "Port": 37941},
           {"IP": "113.124.94.167", "Port": 29082}, {"IP": "125.106.185.83", "Port": 42691},
           {"IP": "183.150.158.149", "Port": 27617}, {"IP": "163.204.216.232", "Port": 35571},
           {"IP": "114.104.129.11", "Port": 11718}, {"IP": "182.34.26.247", "Port": 26873},
           {"IP": "125.87.105.35", "Port": 25628}, {"IP": "220.186.175.136", "Port": 34867},
           {"IP": "42.7.117.230", "Port": 35221}, {"IP": "113.137.111.175", "Port": 10668},
           {"IP": "121.225.187.24", "Port": 32650}, {"IP": "221.203.172.154", "Port": 39613},
           {"IP": "117.92.212.3", "Port": 10088}, {"IP": "119.5.179.6", "Port": 38235},
           {"IP": "119.132.117.46", "Port": 14377}, {"IP": "49.86.181.212", "Port": 13624},
           {"IP": "140.255.151.124", "Port": 28934}, {"IP": "175.165.162.119", "Port": 36333},
           {"IP": "101.30.147.129", "Port": 13703}, {"IP": "121.8.28.9", "Port": 24519},
           {"IP": "114.98.161.218", "Port": 10909}, {"IP": "61.186.65.64", "Port": 14505},
           {"IP": "36.57.87.16", "Port": 35941}, {"IP": "114.237.89.113", "Port": 10263},
           {"IP": "115.209.73.203", "Port": 40082}, {"IP": "110.247.108.79", "Port": 41199},
           {"IP": "113.143.59.135", "Port": 42335}, {"IP": "119.249.43.18", "Port": 15155},
           {"IP": "175.150.103.129", "Port": 38926}, {"IP": "117.95.214.13", "Port": 36829},
           {"IP": "110.18.154.107", "Port": 12349}, {"IP": "101.26.54.13", "Port": 21579},
           {"IP": "59.53.144.152", "Port": 29052}, {"IP": "113.143.56.196", "Port": 41743},
           {"IP": "60.17.205.24", "Port": 41124}, {"IP": "120.6.169.88", "Port": 15961},
           {"IP": "223.156.196.183", "Port": 21382}, {"IP": "106.36.160.39", "Port": 12170},
           {"IP": "223.215.222.180", "Port": 33949}, {"IP": "117.65.150.168", "Port": 37401},
           {"IP": "61.186.66.39", "Port": 16148}, {"IP": "114.237.60.220", "Port": 28700},
           {"IP": "171.211.7.102", "Port": 14694}, {"IP": "112.194.94.162", "Port": 14968},
           {"IP": "61.52.87.167", "Port": 10475}, {"IP": "106.111.9.151", "Port": 41721},
           {"IP": "106.40.243.141", "Port": 15641}, {"IP": "113.100.89.101", "Port": 15739},
           {"IP": "119.186.72.9", "Port": 14273}, {"IP": "125.94.181.104", "Port": 18033},
           {"IP": "114.238.169.47", "Port": 17934}, {"IP": "115.207.63.94", "Port": 20258},
           {"IP": "180.155.155.187", "Port": 26808}, {"IP": "123.188.197.151", "Port": 38862},
           {"IP": "14.118.233.161", "Port": 10748}, {"IP": "59.32.46.89", "Port": 10826},
           {"IP": "42.87.70.225", "Port": 10975}, {"IP": "14.157.101.147", "Port": 27742},
           {"IP": "123.169.39.155", "Port": 33297}, {"IP": "14.134.187.143", "Port": 14655},
           {"IP": "183.47.136.39", "Port": 28574}, {"IP": "219.131.191.179", "Port": 37287},
           {"IP": "114.107.149.103", "Port": 12402}, {"IP": "122.188.58.103", "Port": 14313},
           {"IP": "14.134.190.181", "Port": 37083}, {"IP": "113.121.42.182", "Port": 19847},
           {"IP": "117.26.220.53", "Port": 10452}, {"IP": "106.40.242.32", "Port": 37522},
           {"IP": "113.117.30.220", "Port": 12493}, {"IP": "114.225.220.16", "Port": 14771},
           {"IP": "220.177.158.37", "Port": 11373}, {"IP": "113.124.86.162", "Port": 13382},
           {"IP": "125.94.178.88", "Port": 12914}, {"IP": "114.97.214.83", "Port": 16352},
           {"IP": "122.191.147.154", "Port": 34024}, {"IP": "116.131.200.120", "Port": 26280},
           {"IP": "114.101.23.215", "Port": 26412}, {"IP": "113.138.210.205", "Port": 33796},
           {"IP": "171.13.48.11", "Port": 14556}, {"IP": "58.62.40.25", "Port": 33404},
           {"IP": "42.203.38.225", "Port": 25407}, {"IP": "123.160.121.217", "Port": 18746},
           {"IP": "111.76.143.16", "Port": 41473}, {"IP": "120.4.230.128", "Port": 34677},
           {"IP": "125.126.205.85", "Port": 39602}, {"IP": "223.156.199.186", "Port": 20028},
           {"IP": "220.170.240.170", "Port": 32705}, {"IP": "113.237.247.196", "Port": 36787},
           {"IP": "125.120.8.72", "Port": 39981}, {"IP": "115.225.233.124", "Port": 0},
           {"IP": "124.94.205.208", "Port": 11732}, {"IP": "120.40.214.28", "Port": 41214},
           {"IP": "122.7.220.26", "Port": 27692}, {"IP": "1.180.165.233", "Port": 41144},
           {"IP": "119.5.176.253", "Port": 18953}, {"IP": "113.128.30.180", "Port": 27185},
           {"IP": "182.202.222.12", "Port": 38710}, {"IP": "120.80.43.139", "Port": 32300},
           {"IP": "116.208.93.73", "Port": 27388}, {"IP": "115.151.6.42", "Port": 23039},
           {"IP": "1.180.165.122", "Port": 14870}, {"IP": "101.72.134.248", "Port": 27774},
           {"IP": "125.94.178.14", "Port": 41101}, {"IP": "1.198.147.190", "Port": 27467},
           {"IP": "27.150.192.208", "Port": 35938}, {"IP": "116.22.201.12", "Port": 51950},
           {"IP": "144.0.100.41", "Port": 20215}, {"IP": "116.208.99.224", "Port": 29241},
           {"IP": "110.18.2.147", "Port": 40298}, {"IP": "36.47.81.93", "Port": 41888},
           {"IP": "60.185.201.201", "Port": 31181}, {"IP": "60.7.69.97", "Port": 15893},
           {"IP": "110.247.242.47", "Port": 26703}, {"IP": "27.29.158.44", "Port": 10423},
           {"IP": "171.211.6.43", "Port": 29119}, {"IP": "115.148.40.25", "Port": 32719},
           {"IP": "27.159.142.114", "Port": 37974}, {"IP": "106.92.102.28", "Port": 31371},
           {"IP": "112.194.178.6", "Port": 37578}, {"IP": "120.14.81.23", "Port": 10955},
           {"IP": "175.167.238.123", "Port": 11635}, {"IP": "60.182.231.179", "Port": 27674},
           {"IP": "116.131.233.32", "Port": 13048}, {"IP": "110.86.175.150", "Port": 10596},
           {"IP": "101.74.5.2", "Port": 37006}, {"IP": "113.128.120.152", "Port": 10659},
           {"IP": "121.205.177.69", "Port": 41709}, {"IP": "116.22.31.48", "Port": 15264}]

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

BOT_NAME = 'pachong'

SPIDER_MODULES = ['pachong.spiders']
NEWSPIDER_MODULE = 'pachong.spiders'

DOWNLOAD_HANDLERS = {'s3': None}
DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 100



CONCURRENT_REQUESTS_PER_IP = 1

ITEM_PIPELINES = {
    'pachong.pipelines.PachongPipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pachong (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'pachong.middlewares.PachongSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'pachong.middlewares.ProxyMiddleware': 543,
    'pachong.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'pachong.middlewares.AreaSpiderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     # 'pachong.pipelines.PachongPipeline': 300,
#     'scrapy.pipelines.images.ImagesPipeline': 1
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'ITEM_PIPELINES
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FILES_STORE = './img'
# IMAGES_STORE = 'h:/img'
# IMAGES_URL_FIELD = 'image_urls'
