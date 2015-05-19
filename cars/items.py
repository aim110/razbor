# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def filter_price(value):
    res = re.findall('(\d+)', value)
    return res if res else None

def join(values):
    return ' '.join(values)


class PriceField(scrapy.Field):
    def __init__(self):
        self['input_processor'] = MapCompose(filter_price, remove_tags)
        self['output_processor'] = Join(separator=u',')


class TextField(scrapy.Field):
    def __init__(self):
        self['input_processor'] = MapCompose(remove_tags)
        self['output_processor'] = Join()


class CarPart(scrapy.Item):
    price = PriceField()

    info = TextField()
    shop_name = TextField()
    shop_city = TextField()
    brand = TextField()
    model = TextField()
    car_part = TextField()
    category = TextField()

    shop_url = TextField()
    ext_link = TextField()

    def is_valid(self):
        must_list = 'info shop_url shop_name'.split()
        for item in must_list:
            if not self.has_key(item):
                return False
        return True


from scrapy.contrib.loader import ItemLoader
def testing():
    il = ItemLoader(item=CarPart())
    il.add_value('price', [u'1800 р.'])#, re='(\d+)')

    url = il.get_value(['/qqq/www'], TakeFirst())
    base_url = 'http://host.ru'
    fin_url = '/'.join([base_url, url])
    print 'fin: ', fin_url
    il.add_value('shop_url', fin_url)
    il.add_value('info', 'some_info')

    item = il.load_item()
    print type(item), dir(item)
    print item.has_key('brand')

if __name__ == '__main__':
    testing()
