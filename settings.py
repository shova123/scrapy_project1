# Scrapy settings for scrapy_australia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_australia'

SPIDER_MODULES = ['scrapy_australia.spiders']
NEWSPIDER_MODULE = 'scrapy_australia.spiders'
#Export as CSV Feed
FEED_FORMAT = "csv"
FEED_URI = "course.csv"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_australia (+http://www.yourdomain.com)'
# USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
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
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy_australia.middlewares.ScrapyAustraliaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy_australia.middlewares.ScrapyAustraliaDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {'scrapy_crawlera.CrawleraMiddleware': 610}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = 'e73669c64dbd4f6e95526d08d9782f48:'
#CRAWLERA_URL = 'http://proxy.crawlera.com:8010'
CRAWWLERA_PRESERVE_DELAY = 0
# CONCURRENT_REQUESTS = 100
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# DOWNLOAD_TIMEOUT = 20
# LOG_LEVEL = 'ERROR'
# RANDOMIZE_DOWNLOAD_DELAY = True
# DOWNLOAD_DELAY = 0
# AUTOTHROTTLE_DEBUG = False
# AUTOTHROTTLE_MAX_DELAY = 4
# AUTOTHROTTLE_START_DELAY = 0
# AUTOTHROTTLE_ENABLED = False
# COOKIES_ENABLED = False
handle_httpstatus_list = [404]
HTTPERROR_ALLOWED_CODES  =[404]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapy_australia.pipelines.ScrapyAustraliaPipeline': 300,
#}

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
