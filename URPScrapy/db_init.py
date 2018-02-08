# -*- coding:utf-8 -*-
""" 
@author:James
Created on:18-2-7 16:50
"""
import pymysql

TABLE_COLUMNS = [
	'STUID', 'NAME',
	'NAME_PY', 'NAME_EN',
	'NAME_OLD', 'ICID',
	'GENDER', 'STU_CATEGORY',
	'SPECIAL_CATEGORY', 'SCHOOL_ROLL_STATUS',
	'FEE_CATEGORY', 'NATION',
	'BIRTH_PLACE', 'BIRTH_DATE',
	'POLITICS_STATUS', 'EXAM_REGION',
	'GRADUATE_SCHOOL', 'GK_SCORE',
	'MATRICULATE_ID', 'GK_ID',
	'GK_LANGUAGE', 'CONTACT_ADDRESS',
	'POSTCODE', 'PATRIARCH_INFO',
	'ENROLLMENT_DATE', 'DEPARTMENT',
	'MAJOR', 'MAJOR_DIRECTION',
	'GRADE', 'CLASS',
	'HAS_ROLL', 'HAS_NATIONAL_ROLL',
	'SCHOOL_PART', 'TRANSACTION',
	'FOREIGN_LANGUAGE', 'DORM_ADDRESS',
	'YCSJ', 'TRAIN_LEVEL',
	'TRAIN_PATTERN', 'SHUNT_DIRECTION',
	'LEAVE_SCHOOL', 'COMMENT',
	'COMMENT1', 'COMMENT2',
	'COMMENT3'
]


def connect_db():
	return pymysql.connect(
		host='localhost',
		port=3306,
		user='root',
		password='root',
		database='urp_roll_info',
		charset='utf8'
	)


def main():
	conn = connect_db()
	sql_str = 'create table URP_INFO_HEBUST_LG ('
	for c in TABLE_COLUMNS:
		sql_str += c + ' ' + 'varchar(50)' + ','
	sql_str = sql_str[0:sql_str.__len__() - 1]
	sql_str += ');'
	print(sql_str)
	conn.cursor().execute(sql_str)
	conn.close()


if __name__ == '__main__':
	main()
