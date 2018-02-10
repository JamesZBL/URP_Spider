# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 20:15
"""
# 服务器主机名
# 科大
SERVER_HOST = 'jw.hebust.edu.cn'
# 科大理工
# HOST = 'lgjwxt.hebust.edu.cn'

# 服务器端口号
SERVER_PORT = 80

# 登录 URL (POST)
URL_LOGIN = '/loginAction.do'

# 登出 URL (POST)
URL_LOGOUT = '/logout.do?loginType=platformLogin'

# 学籍信息 URL (GET)
URL_XJXX = '/xjInfoAction.do?oper=xjxx'

# 学籍照片 URL (GET)
URL_XJZP = '/xjInfoAction.do?oper=img'

# 年级（2位数字，对应学号的第 1-2 位）
URP_GRADE = 17

# 分隔符（非理工为'',引号中间无空格,且不可省略）
# URP_SEPARATOR = 'L'
URP_SEPARATOR = ''

# 学院（理工为学部）（1-2 位数字，对应学号的第 3-4（理工为 4-5）位）
URP_COLLEGE_START = 1
URP_COLLEGE_END = 11

# 专业 （1 位数字，对应学号的第 5-6（理工为 6-7）位）
URP_MAJOR_START = 1
URP_MAJOR_END = 7

# 班 （1 位数字，对应学号的第 7（理工为 8）位）
URP_CLASS_START = 1
URP_CLASS_END = 9

# 学号 （1-2 位数字，对应学号的最后 2 位）
URP_STU_START = 1
URP_STU_END = 50

# 数据库主机名（数据库必须为 MySQL）
DB_HOST = 'localhost'

# 端口号
DB_PORT = 3306

# 数据库名
DB_NAME = 'URP_ROLL_INFO'

# 用户名
DB_USER = 'root'

# 密码
DB_PWD = 'root'

# 表名
DB_TABLE_NAME = 'URP_INFO_HEBUST_17'

# 获取学籍信息
MOD_ROLL_INFO = False

# 获取学籍照片
MOD_ROLL_IMG = True
