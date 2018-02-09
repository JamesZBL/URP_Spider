# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 20:15
"""
# 服务器主机名
# 科大
HOST = 'jw.hebust.edu.cn'
# 科大理工
# HOST = 'lgjwxt.hebust.edu.cn'

# 服务器端口号
PORT = 80

# 登录 URL (POST)
URL_LOGIN = '/loginAction.do'

# 登出 URL (POST)
URL_LOGOUT = '/logout.do?loginType=platformLogin'

# 学籍信息 URL (GET)
URL_XJXX = '/xjInfoAction.do?oper=xjxx'

# 年级
URP_GRADE = 17

# 分隔符（非理工为'',引号中间无空格,不可省略）
# URP_SEPARATOR = 'L'
URP_SEPARATOR = ''

# 学院（部）（1-2 位数字）
URP_COLLEGE_START = 1
URP_COLLEGE_END = 11

# 专业 （1 位数字）
URP_MAJOR_START = 1
URP_MAJOR_END = 7

# 班 （1 位数字）
URP_CLASS_START = 1
URP_CLASS_END = 9

# 学号 （1-2 位数字）
URP_STU_START = 1
URP_STU_END = 50

# 数据库主机名
DB_HOST = 'localhost'

# 数据库端口号
DB_PORT = 3306

# 数据库名
DB_NAME = 'URP_ROLL_INFO'

# 用户名
DB_USER = 'root'

# 密码
DB_PWD = 'root'

# 表名
DB_TABLE_NAME = 'URP_INFO_HEBUST_17'

# 超时时间
SECOND_TIMEOUT = 0
