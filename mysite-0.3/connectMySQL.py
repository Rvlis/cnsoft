#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project      ：mysite
@File         : connectMySQL.py
@Time         : 2021/9/1 22:51
@Author       : lgl
@PRODUCT_NAME : PyCharm
"""
import pymysql
from pymysql.converters import escape_string
#7enai/w2fbUU
#打开数据库连接
#注意：这里已经假定存在数据库testdb，db指定了连接的数据库，当然这个参数也可以没有
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='rvli', db='newsdatabase', charset='utf8')

#使用cursor方法创建一个游标
cursor = db.cursor()

#查询数据表所有数据
def selectOneData(sql):
    # sql = "select * from employee"
    # sql = "select * from " + table # forecastdata # trainingdata
    cursor.execute(sql)
    data = cursor.fetchone()
    # print(data)
    return data
# selectData('forecastdata')

#向数据表中插入数据
def insertData(sql):
    '''
    :param table: 数据表
    :return:
    '''
    # sql = "insert into forecastdata values ('1','2',20.0)"
    cursor.execute(sql)
    db.commit()
# print('''abcd'1'"2"e'g''',"""abcd'1'"2"eg""","a''''''b")
# insertData("insert into forecastdata values (2,'1','1','//初始化反作弊 组织青年飞行员开展现地教学活动 “常香玉老前辈，我们是人民空军飞行员。今天来这里参学习，特意带来了一架歼-20战斗机模型，',20.0)")
#指定sql查询数据表数据
def selectAllData(sql):
    # sql = " select * from employee where income > '%d' " % (1000)
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

#关闭数据库连接
def closeConncet():
    db.close()

#更新数据库
def updateDB(sql):
    # sql = " update employee set age = age+1 where sex = '%c' " % ('W')
    cursor.execute(sql)
    db.commit()

# 为有效避免因为错误导致的后果，使用以下方式来执行数据库的操作
def tryfunc(sql):
    try:
      # 执行 SQL 语句
      cursor.execute(sql)
      # 提交修改
      db.commit()
    except:
      # 发生错误时回滚
      db.rollback()

#删除数据
def deleteData(sql):
    # sql = " delete from employee where age > '%d' " % (30)
    cursor.execute(sql)
    db.commit()

#查询数据库版本
def versionDB():
    cursor.execute("select version()")
    data = cursor.fetchone()
    print(" Database Version:%s" % data)

#创建数据库表
def addTable(sql):
    cursor.execute("drop table if exists employee")  #如果数据表已经存在，那么删除后重新创建
    # sql = """
    # CREATE TABLE EMPLOYEE (
    # FIRST_NAME CHAR(20) NOT NULL,
    # LAST_NAME CHAR(20),
    # AGE INT,
    # SEX CHAR(1),
    # INCOME FLOAT )
    # """
    cursor.execute(sql)



# sql = "select * from forecastdata"
# itemData = selectAllData(sql)
# print(itemData)
# columns_name = (('编号', 'channelName', 'title', 'content', '预测时长(秒)'),)
# print(columns_name)
def forecastdataLen():
    sql = "select * from forecastdata"
    # forecastdataLen = selectAllData(sql)
    # print(forecastdataLen)
    itemData = selectAllData(sql)
    forecastdataLen = len(itemData)
    return forecastdataLen