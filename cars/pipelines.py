# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime

import pyes
from transliterate import translit

import settings


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        print 'json: got item'
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


def flatten(item):
    if type(item) == list:
        return ";".join(item)
    else:
        return item


class ESWriterPipeline(object):
    def __init__(self):
        self.es = pyes.ES(settings.ES)
        self.index_name = 'parts_%s' % datetime.date.today().strftime("%Y%m%d")
        self.item_type = settings.ITEM_TYPE
        self.mapping = settings.CAR_MAPPING

        if not self.es.indices.exists_index(self.index_name):
            self.es.indices.create_index(self.index_name)
            self.es.indices.put_mapping(self.item_type, self.mapping, self.index_name)

    def process_item(self, item, spider):
        print 'es: got item'
        get_field = lambda x: flatten(item.get(x))
        model = get_field('model')
        brand = get_field('brand')
        if not brand:
            brand = settings.BRAND  # for debugging from cmd

        mark_model_en = u'%s %s' % (brand, model)
        mark_model_rus = translit(mark_model_en, 'ru')

        part_name = get_field('car_part')
        info = get_field('info')

        es_item = {'part_name': part_name,
                   'info': info,
                   'shop_name': get_field('shop_name'),
                   'shop_link': get_field('shop_url'),
                   'ext_link': get_field('ext_link'),
                   'price': get_field('price'),
                   'city': get_field('shop_city'),
                   'mark_model_en': mark_model_en,
                   'mark_model_rus': mark_model_rus
                   }

        try:
            self.es.index(es_item, self.index_name, settings.ITEM_TYPE)
        except pyes.exceptions.ElasticSearchException as e:
            print repr(e)
            print "On %s" % es_item

    def close_spider(self, spider):
        self.es.indices.refresh()
