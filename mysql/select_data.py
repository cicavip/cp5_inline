#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
fetchall():接收全部的返回结果行.
rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
'''

import pymysql

def select_data(host, user, pw,sql):

    """
    :param host: 数据库IP地址
    :param user: 用户
    :param pw: 密码
    :param database: 数据库名称
    :param table: 列表名称
    :param sql: 搜索的执行语句
    :return:
    """

    # 数据库连接
    db = pymysql.connect(host, user, pw,charset='utf8')
    # 创建游标，通过连接与数据通信
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()

    return results
