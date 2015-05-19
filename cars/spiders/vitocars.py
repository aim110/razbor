# -*- coding: utf-8 -*-
import re
import string
import time
from urlparse import urljoin

import scrapy
from scrapy import log  # use: log.msg('')
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

from cars.items import CarPart
from cars import settings

class ExampleSpider(scrapy.Spider):
    name = 'vito'
    allowed_domains = ['vitocars.net']
    start_urls = ['https://vitocars.net/']
    main_url = 'https://vitocars.net'

    def errback(self, failure):
        print failure

    def __init__(self):
        self.parse = self.parse_main_page
        # TBD: for testing
        #self.start_urls = ['https://vitocars.net/car-parts/bra-bmw/mod-1-series-e82e88/cat-optika']
        #self.parse = self.parse_dbg

    def parse_dbg(self, response):
        response.meta['brand'] = 'bmw'
        response.meta['model'] = 'e82'
        response.meta['category'] = 'optika'
        return self.parse_category(response)

    def parse_main_page(self, response):
        """
        initial parse method for start_urls@.

        response@ - scrapy.http.Response instance
        """
        brands = response.css('ul.brands').css('a')
        for b in brands:
            brand_name, url = self.get_name_url(b)
            request = scrapy.Request(self.main_url + url, callback=self.parse_brand, errback=self.errback)
            request.meta['brand'] = brand_name
            yield request

    def get_name_url(self, href_selector):
        name = href_selector.css('a::text').extract()
        url = href_selector.css('a::attr(href)').extract()[0]
        return name, url

    def parse_link_table(self, response, callback, meta_name):
        table_links = response.css('tr td a')

        for link in table_links:
            name, url = self.get_name_url(link)
            # TBD: is that ok to create here a new dict object?
            new_meta = {i: v for i, v in response.meta.iteritems()}
            new_meta[meta_name] = name
            yield scrapy.Request(self.main_url + url, callback=callback, errback=self.errback, meta=new_meta)

    def parse_brand(self, response):
        """ brand -> models """
        return self.parse_link_table(response, self.parse_model, 'model')

    def parse_model(self, response):
        """ model -> cat parts categories """
        return self.parse_link_table(response, self.parse_category, 'category')

    def parse_category(self, response):
        """
        category -> car part name
            e.g.: https://vitocars.net/car-parts/bra-bmw/mod-3-series-e46/cat-optika

        Category can contain car parts for sale, not subgroupped car part names.
            e.g.: https://vitocars.net/car-parts/bra-bmw/mod-1-series-e82e88/cat-optika

        """
        if len(response.css('div.content > table.parts')) > 0:
            return self.parse_parts2(response)
        else:
            return self.parse_link_table(response, self.parse_parts2, 'car_part')

    def parse_parts2(self, response):
        log.msg("\tparse_parts time: %s" % int(time.time()), level=log.DEBUG)
        ua = response.request.headers['User-Agent']
        log.msg("\tua: %s" % ua, level=log.DEBUG)

        for part in response.css('table.parts > tbody > tr'):
            il = ItemLoader(item=CarPart(), selector=part)
            il.add_xpath('shop_city', "td[@class='shop']/a/text()")
            il.add_xpath('shop_name', "td[@class='shop']/a/strong/text()")

            shop_url = il.get_xpath("td[@class='shop']/a/@href", TakeFirst())
            photo_url = il.get_xpath("td[@class='photo']/a/@href", TakeFirst())
            il.add_value('shop_url', urljoin(self.main_url, shop_url))
            il.add_value('ext_link', urljoin(self.main_url, photo_url))

            il.add_xpath('info', "td[@class='info']//text()")
            il.add_xpath('price', "td[@class='price']//text()")

            il.add_value('brand', response.meta.get('brand'))
            il.add_value('model', response.meta.get('model'))
            il.add_value('car_part', response.meta.get('car_part'))
            il.add_value('category', response.meta.get('category'))

            item = il.load_item()
            if item.is_valid():
                yield item
