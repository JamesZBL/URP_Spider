# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-8 20:15
"""

# 登录 (GET)
URL_LOGIN = 'http://lgjwxt.hebust.edu.cn/loginAction.do'
# 登出 (POST only)
URL_LOGOUT = 'http://lgjwxt.hebust.edu.cn/logout.do?loginType=platformLogin'
# 学籍信息 (GET)
URL_XJXX = 'http://lgjwxt.hebust.edu.cn/xjInfoAction.do?oper=xjxx'
# 年级
URP_GRADE = 14
# 分隔符（非理工为'',引号中间无空格)
URP_SEPARATOR = 'L'
# 学院（部）
URP_COLLEGE_START = 1
URP_COLLEGE_END = 7
# 专业
URP_MAJOR_START = 51
URP_MAJOR_END = 52
# 班
URP_CLASS_START = 1
URP_CLASS_END = 2
# 学号
URP_STU_START = 0
URP_STU_END = 99

DB_TABLE_NAME = 'URP_INFO_HEBUST_LG_14'
