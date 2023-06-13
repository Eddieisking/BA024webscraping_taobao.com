# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
import re
# Pipeline for Excel
# class ExcelPipeline:
#
#     def __init__(self):
#         self.wb = openpyxl.Workbook()
#         self.ws = self.wb.active
#         self.ws.title = 'Top250'
#         self.ws.append(('标题','评分','信息', '片长', '简介'))
#
#     def open_spider(self, spider):
#         pass
#
#     def close_spider(self, spider):
#         self.wb.save('douban.xlsx')
#
#     def process_item(self, item, spider):
#         name = item.get('name', '')
#         rating = item.get('rating', '')
#         info = item.get('info', '')
#         length = item.get('length', '')
#         abstract = item.get('abstract', '')
#         self.ws.append((name, rating, info, length, abstract))
#         return item

"""
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

class DatabasePipeline:

    def __init__(self):
        self.conn = pymysql.connect(user="fqmm26", password="boston27", host="myeusql.dur.ac.uk", database="Pfqmm26_amazon")
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.sql_write()
        self.conn.close()

    def process_item(self, item, spider):
        product_name = item.get('product_name', '')
        customer_name = item.get('customer_name', '')
        customer_rating = item.get('customer_rating', '')
        # Remove unloaded chars
        customer_date_original = item.get('customer_date', '')
        customer_date = remove_unappealing_characters(customer_date_original)
        # Remove unloaded chars and cut
        customer_review_original = item.get('customer_review', '')
        customer_review = remove_unappealing_characters(' '.join(customer_review_original)[:1000])
        customer_support = item.get('customer_support', '')
        self.data.append((product_name, customer_name, customer_rating, customer_date, customer_review, customer_support))

        if len(self.data) == 10:
            self.sql_write()
            self.data.clear()

        return item

    def sql_write(self):
        self.cursor.executemany(
            "insert into customer_review (product_name, customer_name, customer_rating, customer_date, customer_review, customer_support) values(%s, %s, %s, %s, %s, %s)",
            self.data
        )
        self.conn.commit()



