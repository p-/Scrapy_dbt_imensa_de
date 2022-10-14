# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class ScraperImensaPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
        dbname="imensa",
        host="localhost",
        port="5432",
        user="postgres",
        password="postgres"
        )
        self.cur = self.conn.cursor()
        self.create_table()

    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()

    def create_table(self):
        self.cur.execute(
            """
            DROP TABLE IF EXISTS
                items_raw
            CASCADE
            """
            )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS items_raw (
            id SERIAL PRIMARY KEY,
            mensa_name TEXT,
            state TEXT,
            meal_category TEXT,
            meal_name TEXT,
            price TEXT,
            price_per TEXT,
            last_time TEXT,
            meal_attributes TEXT,
            day_meal TEXT,
            date_meal TEXT,
            stars_average TEXT,
            ratings_count TEXT,
            number_5_star_ratings TEXT,
            number_4_star_ratings TEXT,
            number_3_star_ratings TEXT,
            number_2_star_ratings TEXT,
            number_1_star_ratings TEXT,
            street_and_nr TEXT,
            plz_and_city TEXT,
            unique_key TEXT UNIQUE NOT NULL,
            operator TEXT,
            list_mensas_close TEXT,
            day_minute_scraped TEXT
            )"""
            )

    def process_item(self, item, spider):
        self.cur.execute("""INSERT INTO items_raw (
                            mensa_name,
                            state,
                            meal_category,
                            meal_name,
                            price,
                            price_per,
                            last_time,
                            meal_attributes,
                            day_meal,
                            date_meal,
                            stars_average,
                            ratings_count,
                            number_5_star_ratings,
                            number_4_star_ratings,
                            number_3_star_ratings,
                            number_2_star_ratings,
                            number_1_star_ratings,
                            street_and_nr,
                            plz_and_city,
                            unique_key,
                            operator,
                            list_mensas_close,
                            day_minute_scraped) VALUES
                            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON CONFLICT (unique_key)
                            DO NOTHING;
                        """,
                        (
                            item['mensa_name'],
                            item['state'],
                            item['meal_category'],
                            item['meal_name'],
                            item['price'],
                            item['price_per'],
                            item['last_time'],
                            item['meal_attributes'],
                            item['day_meal'],
                            item['date_meal'],
                            item['stars_average'],
                            item['ratings_count'],
                            item['number_5_star_ratings'],
                            item['number_4_star_ratings'],
                            item['number_3_star_ratings'],
                            item['number_2_star_ratings'],
                            item['number_1_star_ratings'],
                            item['street_and_nr'],
                            item['plz_and_city'],
                            item['unique_key'],
                            item['operator'],
                            str(item['list_mensas_close']),
                            item['day_minute_scraped']
                            )
                        )
        self.conn.commit()
        return item
