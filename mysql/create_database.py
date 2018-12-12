# _*_encoding:UTF-8_*_
import pymysql



def cre_db_database(host, user, pw, database):
    try:
        # 数据库连接
        db = pymysql.connect(host, user, pw, charset='utf8')
        # 创建游标，通过连接与数据通信
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute('show databases')
        rows = cursor.fetchall()
        print(rows)
        list_rows=[]
        for row in rows:
            print(row)
            list_rows=list_rows+list(row)
        print(list_rows)

        # 判断数据库是否存在
        if database not in list_rows:
            list_rows.append(database)
            print(list_rows)
            cursor.execute('create database ' + database)
            # 提交到数据库执行
            db.commit()
        # 关闭数据库连接
        db.close()



    except pymysql.Error as e:
        error_number=e.args[0]
        error_detail=e.args[1]
        print(f'Mysql Error{error_number}:{error_detail}')
        # # 关闭数据库连接
        # db.close()



        # finally:
    #     # 关闭数据库连接
    #     db.close()

# 测试
# db_host = 'localhost'
# db_user = 'root'
# db_pw = 'mysql_qd'
# db_databases = ['TROC','X55']
# table_names = ['RO1','RO2','RO6']
# cre_db_database(db_host, db_user, db_pw,db_databases)