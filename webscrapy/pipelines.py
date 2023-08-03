# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
import re
import googletrans
from datetime import datetime
from googletrans import Translator
from pymysql import Error
from datetime import datetime, timedelta

"""
    review_id = scrapy.Field()
    product_name = scrapy.Field()
    customer_name = scrapy.Field()
    customer_rating = scrapy.Field()
    customer_date = scrapy.Field()
    customer_review = scrapy.Field()
    customer_support = scrapy.Field()
"""


# Pipeline for Excel
class ExcelPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'customer reviews'
        self.ws.append(('product_name', 'customer_name', 'customer_date', 'customer_review', 'customer_support',
                        'customer_browse'))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.wb.save('taobao.xlsx')

    def process_item(self, item, spider):
        # review_id = item.get('review_id', '')
        product_name = item.get('product_name', '')
        customer_name = item.get('customer_name', '')
        # customer_rating = item.get('customer_rating', '')
        customer_date = item.get('customer_date', '')
        customer_review = item.get('customer_review', '')
        customer_support = item.get('customer_support', '')
        # customer_disagree = item.get('customer_disagree', '')
        customer_browse = item.get('customer_browse', '')

        self.ws.append((product_name, customer_name, customer_date, customer_review, customer_support, customer_browse))
        return item


"""
    review_id = scrapy.Field()
    product_name = scrapy.Field()
    customer_name = scrapy.Field()
    customer_rating = scrapy.Field()
    customer_date = scrapy.Field()
    customer_review = scrapy.Field()
    customer_support = scrapy.Field()
"""


# Pipeline for sql
def remove_unappealing_characters(text):
    # Remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E]', '', text)

    return text

def translator(text: str, src: str):

    # print(googletrans.LANGUAGES)

    translator = Translator()
    result = translator.translate(text, src=src, dest='en')

    return result.text

def extract_date_info(string):
    date_info = string.split(' ')[0].strip()
    return date_info

def convert_to_datetime(date_info):
    current_date = datetime.now().date()  # Get current date without time
    if '年前' in date_info:
        years_ago = int(date_info.split('年前')[0])
        date = current_date - timedelta(days=years_ago * 365)
    elif '个月前' in date_info:
        months_ago = int(date_info.split('个月前')[0])
        date = current_date - timedelta(days=months_ago * 30)
    elif '天前' in date_info:
        days_ago = int(date_info.split('天前')[0])
        date = current_date - timedelta(days=days_ago)
    else:
        raise ValueError(f"Unsupported date format: {date_info}")

    return date

def extract_number(string):
    number = re.findall(r'\d+', string)
    if number:
        return int(number[0])
    else:
        return 0

class DatabasePipeline:

    def __init__(self):
        self.conn = pymysql.connect(user="fqmm26", password="boston27", host="myeusql.dur.ac.uk", database="Pfqmm26_BA024")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        # self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("SELECT 1")  # Execute a simple query to check if the connection is alive
        except Error as e:
            print(f"Error: {e}")
            self.reconnect()

        # review_id = item.get('review_id', '')
        review_id = 'N/A'
        product_name = item.get('product_name', '')
        customer_name = item.get('customer_name', '')
        # customer_rating = item.get('customer_rating', '')
        customer_rating = 'N/A'
        customer_date = convert_to_datetime(extract_date_info(item.get('customer_date', '')))

        customer_review = item.get('customer_review', '')[0:1999]
        customer_support = extract_number(item.get('customer_support', ''))
        # customer_disagree = item.get('customer_disagree', '')
        customer_disagree = 'N/A'
        product_website = item.get('product_website', '')
        product_brand = item.get('product_brand', '')
        product_model = item.get('product_model', '')
        product_type = item.get('product_type', '')
        # customer_browse = item.get('customer_browse', '')

        product_name_en = translator(product_name, src='zh-cn')
        customer_review_en = translator(customer_review, src='zh-cn')

        try:
            self.cursor.execute(
                "INSERT INTO taobao_cn (review_id, product_name, customer_name, customer_rating, customer_date, "
                "customer_review, customer_support, customer_disagree, product_name_en, customer_review_en, product_website, product_type, product_brand, product_model) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (review_id, product_name, customer_name, customer_rating, customer_date, customer_review,
                 customer_support, customer_disagree, product_name_en, customer_review_en, product_website,
                 product_type, product_brand, product_model)
            )
            self.conn.commit()
        except Error as e:
            print(f"Error inserting item into database: {e}")
        return item

    def reconnect(self):
        try:
            self.conn.ping(reconnect=True)  # Ping the server to reconnect
            print("Reconnected to the database.")
        except Error as e:
            print(f"Error reconnecting to the database: {e}")