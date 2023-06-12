# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql


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


# class DatabasePipeline:
#
#     def __init__(self):
#         self.conn = pymysql.connect(user="fqmm26", password="boston27", host="myeusql.dur.ac.uk", database="Pfqmm26_douban")
#         self.cursor = self.conn.cursor()
#         self.data = []
#
#     def close_spider(self, spider):
#         if len(self.data) > 0:
#             self.sql_write()
#         self.conn.close()
#
#     def process_item(self, item, spider):
#         name = item.get('name', '')
#         rating = item.get('rating', '')
#         info = item.get('info', '')
#         length = item.get('length', '')
#         abstract = item.get('abstract', '')
#
#         self.data.append((name, rating, info, length, abstract))
#         print(self.data)
#         if len(self.data) == 25:
#             self.sql_write()
#             self.data.clear()
#
#         return item
#
#     def sql_write(self):
#         self.cursor.executemany(
#             "insert into top250 (Name, Rating, Info, Length, Abstract) values(%s, %s, %s, %s, %s)",
#             self.data
#         )
#         self.conn.commit()
