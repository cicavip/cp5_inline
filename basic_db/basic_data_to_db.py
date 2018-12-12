import pymysql

def basic_data_to_db(host,user, pw,database,table, Point_Group,PointName,X_Position,Y_Position,Z_Position,i_Richtung,j_Richtung,k_Richtung,UntererTol,
                          ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,
                          Description, Point_Grade,Consistency,FM_POINT,CS_Statistics):
    try:
        canshu = (table, Point_Group, PointName, X_Position, Y_Position, Z_Position, i_Richtung, j_Richtung, k_Richtung,
                  UntererTol,
                  ObererTol, UntererTol_I, ObererTol_I, UntererTol_II, ObererTol_II, UntererTol_III, ObererTol_III,
                  Characteristic,
                  Description, Point_Grade, Consistency, FM_POINT, CS_Statistics)
        print(canshu)
        print(type(PointName))
        # SQL 插入语句
        sql = """INSERT INTO %s (Point_Group,PointName,X_Position,Y_Position,Z_Position,i_Richtung,j_Richtung,k_Richtung,UntererTol,
                  ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,
                  Description, Point_Grade,Consistency,FM_POINT,CS_Statistics)
                            VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                    %s,%s,%s,%s,'%s','%s',%s,'%s','%s','%s')""" % canshu
        print(sql)
        # 打开数据库连接
        db = pymysql.connect(host, user, pw, database, charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute(sql)
    except:
        canshu = (table, Point_Group, PointName, X_Position, Y_Position, Z_Position, i_Richtung, j_Richtung, k_Richtung,
                  UntererTol,
                  ObererTol, UntererTol_I, ObererTol_I, UntererTol_II, ObererTol_II, UntererTol_III, ObererTol_III,
                  Characteristic,
                  Description, Point_Grade, Consistency, FM_POINT, CS_Statistics)
        print(canshu)
        print(type(PointName))
        # SQL 插入语句
        sql = """INSERT INTO %s (Point_Group,PointName,X_Position,Y_Position,Z_Position,i_Richtung,j_Richtung,k_Richtung,UntererTol,
                          ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,
                          Description, Point_Grade,Consistency,FM_POINT,CS_Statistics)
                                    VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                            %s,%s,%s,%s,'%s','%s',%s,'%s','%s','%s')""" % canshu
        print(sql)
        # 打开数据库连接
        db = pymysql.connect(host, user, pw, database, charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行sql语句
        # cursor.execute(sql)
        try:
            cursor.execute(sql)
        except:
            print('点名有重复')


    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()