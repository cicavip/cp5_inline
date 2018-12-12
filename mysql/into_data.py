#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
fetchall():接收全部的返回结果行.
rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
'''

import pymysql

def into_data(host, user, pw,sql):

    """
    :param host: 数据库IP地址
    :param user: 用户
    :param pw: 密码
    :param sql: 搜索的执行语句,这个语句里面需要写数据库和表的名称
    :return:
    """

    # 数据库连接
    db = pymysql.connect(host, user, pw,charset='utf8')
    # 创建游标，通过连接与数据通信
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # 关闭数据库连接
    db.close()


