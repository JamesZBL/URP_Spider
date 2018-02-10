# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-10 16:06
"""

from URPInfoSpider import settings

header = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Cache-Control': 'max-age=0',
	'Connection': 'Keep-alive',
	'Host': settings.SERVER_HOST,
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
}
