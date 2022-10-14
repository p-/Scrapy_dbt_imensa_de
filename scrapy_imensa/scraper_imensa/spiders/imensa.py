import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scraper_imensa.items import ScraperImensaItem
from datetime import date, datetime, timedelta
import time

class ImensaSpider(CrawlSpider):
    name ="imensa"
    allowed_domains = ['www.imensa.de']
    start_urls = ['https://www.imensa.de']

    rules = (
        Rule(LinkExtractor(deny='.*(?:\/.*){5}')),
        Rule(LinkExtractor(), callback='parse_item')
    )

    def parse_item(self,response):
        self.ts = time.time()
        self.day_minute_scraped = (datetime.fromtimestamp(self.ts)).strftime('%Y-%m-%d %H:%M:%S')
        self.day_scraped = (datetime.fromtimestamp(self.ts)).strftime('%Y-%m-%d')
        # self.not_valid_meal_names = [
        item = ScraperImensaItem()
        operator_raw = response.css('div.aw-title-header-content div.row div:nth-child(1)::text').get()
        for meal_category in response.css('div.aw-meal-category'):
            item['mensa_name'] = response.css('h1.aw-title-header-title::text').get()
            item['state'] = response.css('a.internal span::text').getall()[1]
            item['meal_category'] = meal_category.css('h3.aw-meal-category-name::text').get()
            item['meal_name'] = ' '.join(meal_category.css('p.aw-meal-description::text').getall())
            item['price'] = meal_category.css('div.aw-meal-price::text').get()
            item['price_per'] = meal_category.css('div.aw-meal-price span.aw-meal-price-per::text').get()
            item['date_meal'] = self.convert_date(response.css('a.list-group-item.active small.pull-right::text').get())
            item['day_minute_scraped'] = self.day_minute_scraped
            item['last_time'] = self.convert_date_last_time(meal_category.css('div.aw-meal-last::text').get(), item['date_meal'])
            item['meal_attributes'] = meal_category.css('p.aw-meal-attributes span::text').get()
            item['day_meal'] = response.css('a.list-group-item.active::text').get()
            item['stars_average'] = response.css('div.aw-ratings-average::text').get()
            item['ratings_count'] = response.css('div.aw-ratings-count::text').get()
            try:
                item['number_5_star_ratings'] = response.css('div.aw-ratings-chart.barchart span.barchart-value::text').getall()[0]
                item['number_4_star_ratings'] = response.css('div.aw-ratings-chart.barchart span.barchart-value::text').getall()[1]
                item['number_3_star_ratings'] = response.css('div.aw-ratings-chart.barchart span.barchart-value::text').getall()[2]
                item['number_2_star_ratings'] = response.css('div.aw-ratings-chart.barchart span.barchart-value::text').getall()[3]
                item['number_1_star_ratings'] = response.css('div.aw-ratings-chart.barchart span.barchart-value::text').getall()[4]
            except:
                item['number_5_star_ratings'] = None
                item['number_4_star_ratings'] = None
                item['number_3_star_ratings'] = None
                item['number_2_star_ratings'] = None
                item['number_1_star_ratings'] = None
            item['street_and_nr'] = response.css('a.panel-body::text').getall()[0]
            item['plz_and_city'] = response.css('a.panel-body::text').getall()[1]
            item['unique_key'] =  self.day_scraped \
                + self.xstr(item['meal_name']) \
                + self.xstr(item['mensa_name']) \
                + self.xstr(item['meal_category']) \
                + self.xstr(item['day_meal']) \
                + self.xstr(item['street_and_nr'])
            try:
                item['operator'] = re.search('wird vom(.*) betrieben', operator_raw).group(1)
            except:
                item['operator'] = ""
            list_mensas_close_names = response.css('div.panel.panel-default.hidden-xs.hidden-sm:nth-of-type(2) a.list-group-item::text').getall()
            list_mensas_close_distances = response.css('div.panel.panel-default.hidden-xs.hidden-sm:nth-of-type(2) a.list-group-item small::text').getall()
            dict_mensas_close = dict(zip(list_mensas_close_names, list_mensas_close_distances))
            item['list_mensas_close'] = dict_mensas_close

            yield item

        for link_day in response.css('a.list-group-item::attr(href)').getall():
            yield response.follow(link_day, callback=self.parse_item)

    def convert_date(self, value):
        if value == 'morgen':
            return (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
        if value == 'heute':
            return (date.today()).strftime("%d.%m.%Y")
        else:
            return value

    def xstr(self,s):
        if s is None:
            return ''
        return str(s)

    def convert_date_last_time(self,value,context_date):
        # problem of no date value in item['date']
        if value =='gestern':
            context_day = int(context_date.split('.')[0])
            context_month = int(context_date.split('.')[1])
            context_year = int(context_date.split('.')[2])
            return (date(context_year, context_month, context_day) + timedelta(days=-1)).strftime("%d.%m,%Y")
        if value =='vorgestern':
            context_day = int(context_date.split('.')[0])
            context_month = int(context_date.split('.')[1])
            context_year = int(context_date.split('.')[2])
            return (date(context_year, context_month, context_day) + timedelta(days=-2)).strftime("%d.%m,%Y")
        else:
            return value