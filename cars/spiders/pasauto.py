# -*- coding: utf-8 -*-
import scrapy


class PasautoSpider(scrapy.Spider):
    name = "pasauto"
    allowed_domains = ["pasauto.ru"]
    start_urls = (
        'http://pasauto.ru/',
    )

    def parse(self, response):
        brands = response.css('')

#
# PASAUTO:
#
# brands: css('div.cars table a')
# models: 'div.cars div#vmMainPage table a' -- ford example
# cats: 'div.cars div#vmMainPage table a' -- mazda example
# parts: 'div.cars div#vmMainPage table a' -- kia example
# items: add &limitstart=0&limit=50 to show all items

# Example:
#for i in response.css('div#vmMainPage table tr').xpath('//tr[re:test(@class, "\d$")]'):
#    print i.css('td span.productPrice::text').extract()[0]  # print price

# ----
# NB: it's multiple ext_links in each row here; TBD: select first. Can css
# selector do it?

# PAGE: http://pasauto.ru/zapchasti-b-u.html?category_id=687&page=shop.browse&limitstart=0&limit=50


#
# Bibit.ru
#
# brands: 'div.middle div.row table a'
# models: 'div.middle div.col-xs-6 ul a'
# cats:   'div.middle div.col-xs-6 ul a'
# parts: 'div.middle div.col-xs-6 ul a'
# items:
#for i in response.css('div.middle div#col-slave div.block h3 a'):
    # getting name, url
#    print i.css('a::text').extract(), i.css('a::attr(href)').extract()

#
# info
#
#for i in response.css('div.middle div#col-slave div.block div.col-xs-7'):
#    print ";".join(i.css('::text').extract())

#TBD: For all spiders:
# - flatten every data !!!
# - save to appropriate format. current redirecting stdin works not really
# good
