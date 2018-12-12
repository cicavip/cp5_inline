import pymysql



def mappingtable_car(host, user, pw, database):

    # 数据库连接
    db = pymysql.connect(host, user, pw, database, charset='utf8')
    # 创建游标，通过连接与数据通信
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select notstandard,standard from car"
    # 执行SQL语句n
    cursor.execute(sql)
    # 获取所有记录列表
    dict_cars=dict(cursor.fetchall())
    # print(dict_cars)


    sql_stcar = "select standard from car"
    # 执行SQL语句n
    cursor.execute(sql_stcar)

    #标准车型缩写
    standard_car = []
    st_cars=list(cursor.fetchall())

    #标准车型缩写做在一个列表里面
    for st_car in st_cars:
        standard_car.append(st_car[0])

    # # 去掉重复的和排序
    standard_car=(sorted(set(standard_car)))
    # print(standard_car)

    # 关闭数据库连接
    db.close()


    return dict_cars,standard_car

def mappingtable_part (host, user, pw, database):

    # 数据库连接
    db = pymysql.connect(host, user, pw, database, charset='utf8')
    # 创建游标，通过连接与数据通信
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select notstandard,standard from part"
    # 执行SQL语句n
    cursor.execute(sql)
    # 获取所有记录列表
    dict_parts = dict(cursor.fetchall())
    # print(dict_parts)


    sql_stpart = "select standard from part"
    # 执行SQL语句n
    cursor.execute(sql_stpart)

    #标准零件缩写
    standard_part = []
    st_parts=list(cursor.fetchall())

    # 标准零件缩写做在一个列表里面
    for st_part in st_parts:
        standard_part.append(st_part[0])

    #去掉重复的和排序
    standard_part=sorted(set(standard_part))
    # print(standard_part)

    # 关闭数据库连接
    db.close()


    return dict_parts,standard_part


