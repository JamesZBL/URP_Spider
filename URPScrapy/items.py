# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class URPStuItem(scrapy.Item):
	# 学号
	stuId = scrapy.Field()
	# 学生姓名
	stuName = scrapy.Field()
	# 身份证号
	icNum = scrapy.Field()
