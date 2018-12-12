# _*_encoding:UTF-8_*_
import pymysql


def cre_db_table(host, user, pw, database,table,table_byte):

    try:

         # 数据库连接
        db = pymysql.connect(host, user, pw, database, charset='utf8')
        # 创建游标，通过连接与数据通信
        cursor = db.cursor()
        # 读取对应数据库的所有表
        cursor.execute('show tables')
        rows = cursor.fetchall()
        list_rows = []
        for row in rows:
            list_rows = list_rows + list(row)
        # print(list_rows)

        if table not in list_rows:
            print('create table' + table + table_byte)
            cursor.execute('create table ' + table + table_byte)
            db.commit()
        # 关闭数据库连接
        db.close()



    except pymysql.Error as e:
            #错误说明
            error_number=e.args[0]
            error_detail=e.args[1]
            print(f'Mysql Error{error_number}:{error_detail}')
            # 关闭数据库连接
            db.close()


            #
    # finally:
    #     # 关闭数据库连接
    #     db.close()


