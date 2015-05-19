# -*- coding: utf-8 -*-

# Scrapy settings for cars project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os

BOT_NAME = 'cars'

SPIDER_MODULES = ['cars.spiders']
NEWSPIDER_MODULE = 'cars.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cars (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'cars.pipelines.JsonWriterPipeline': 300,
    'cars.pipelines.ESWriterPipeline': 500,
}

ES = 'http://localhost:9202'
ITEM_TYPE = 'car_part_item'
CAR_MAPPING = {
                "properties": {
                    "mark_model_en" : {"type": "string", "analyzer": "russian"},
                    "mark_model_ru" : {"type": "string", "analyzer": "russian"},
                    "part_name" : {"type": "string", "analyzer": "russian"},
                    "info" : {"type": "string", "analyzer": "russian"},
                    "shop_name" : {"type": "string", "index": "not_analyzed"},
                    "shop_link" : {"type": "string", "index": "not_analyzed"},
                    "ext_link" : {"type": "string", "index": "not_analyzed"},
                    "price" : {"type": "integer"},
                    "city" : {"type" : "string", "index" : "not_analyzed"}
                }
            }
BRAND='Ford'

DOWNLOAD_DELAY = 0.05

DOWNLOADER_MIDDLEWARES = {
        'cars.tools.RandomUserAgentMiddleware': 100,
}

USER_AGENT_FILE = os.path.join(os.path.dirname(__file__), '..', 'ua_list')
