import pymysql

def point_value_to_db (host, user, pw,car,part,point_value_information,basic_information):
    """
    :param point_value_information: 单个点对应的测量测量值
    :param basic_information: 单个DMO的基础信息，零件钢号，车型，零件，测量开始时间，测量结束时间
    将每一个dmo的测量点的测量值读入数据库。
    :return:
    """
    #目标数据库
    db_database=car
    #目标表格
    db_table = part
    #对应的钢号
    Identnummer = basic_information[1]
    #对应DMO的开始时间
    StartDateTime= basic_information[3].replace("/", "-") + ' ' + basic_information[4]
    # StartDateTime = datetime.datetime.strptime(sStartDateTime, "%Y-%m-%d %H:%M:%S")
    #对应DMO的结束时间
    EndDateTime = basic_information[5].replace("/", "-") + ' ' + basic_information[6]
    # EndDateTime = datetime.datetime.strptime(EndDateTime, "%Y-%m-%d %H:%M:%S")

    # 数据库连接
    db = pymysql.connect(host, user, pw, db_database, charset='utf8')
    # 创建游标，通过连接与数据通信
    cursor = db.cursor()

    for PointName, Messwert in point_value_information.items():

        canshu=(db_table,PointName,Messwert,Identnummer,StartDateTime,EndDateTime)
        print(canshu)

        # SQL 插入语句
        sql = """INSERT INTO %s (PointName, Messwert, Identnummer, StartDateTime, EndDateTime)
                 VALUES ('%s', '%s', '%s', '%s', '%s')"""%canshu
        print(sql)
        # 执行sql语句
        cursor.execute(sql)

    # 提交到数据库执行
    db.commit()

    # 关闭数据库连接
    db.close()