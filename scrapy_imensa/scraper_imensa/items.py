# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperImensaItem(scrapy.Item):
    mensa_name = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    meal_category = scrapy.Field()
    meal_name = scrapy.Field()
    price = scrapy.Field()
    price_per = scrapy.Field()
    last_time = scrapy.Field()
    meal_attributes = scrapy.Field()
    date_meal = scrapy.Field()
    day_meal = scrapy.Field()
    stars_average = scrapy.Field()
    ratings_count = scrapy.Field()
    number_5_star_ratings = scrapy.Field()
    number_4_star_ratings = scrapy.Field()
    number_3_star_ratings = scrapy.Field()
    number_2_star_ratings = scrapy.Field()
    number_1_star_ratings = scrapy.Field()
    street_and_nr = scrapy.Field()
    plz_and_city = scrapy.Field()
    unique_key = scrapy.Field()
    operator = scrapy.Field()
    list_mensas_close = scrapy.Field()
    day_minute_scraped = scrapy.Field()