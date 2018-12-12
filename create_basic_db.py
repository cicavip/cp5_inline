import os,sqlite3,pymysql
from cp5_inline.mysql.read_MappingTable import mappingtable_car, mappingtable_part
from cp5_inline.mysql.create_table import cre_db_table


host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'LISON23354!'  # mysql的密码
map_database = 'MappingTable'  # 映射表数据据库名称

# dmo存放的绝对地址
# dmo_error_file = r'D:\Python\Python_Project\cp4_2_inline\DMO_Error'
base_data_addr = r'D:\02_Python_Project\cp4_2_inline\01_Base_data'

dict_cars = mappingtable_car(host, user, pw, map_database)[0]  # 映射表车型的字典
dict_parts = mappingtable_part(host, user, pw, map_database)[0]  # 映射表零件的字典

#读取sql3数据库的名称列表
sql3_db_list = os.listdir(base_data_addr)
print(sql3_db_list)

def sql3_basic_to_mysql(sql3_db_list):

    for sql3_db in sql3_db_list:
        sql3_db_car=sql3_db.split('_')[2]#提取sql3数据库的名称的车型缩写
        print(sql3_db_car)
        sql3_db_part = sql3_db.split('_')[3].split('.')[0]#提取sql3数据库的名称的零件缩写
        print(sql3_db_part)

        #创建对应的基础数据库列表
        database=dict_cars[sql3_db_car]#mysqll里面的车型数据库
        table='inline_base_'+dict_parts[sql3_db_part]#mysqll对应的基础数据库的列表名称
        print(table)

        #基础数据可的列表字段
        base_table_byte = '(Point_Group INT, ' \
                          'PointName CHAR(50) NOT NULL primary key,' \
                          'X_Position FLOAT, ' \
                          'Y_Position FLOAT, ' \
                          'Z_Position FLOAT, ' \
                          'i_Richtung FLOAT, ' \
                          'j_Richtung FLOAT, ' \
                          'k_Richtung FLOAT, ' \
                          'UntererTol FLOAT, ' \
                          'ObererTol FLOAT, ' \
                          'UntererTol_I FLOAT, ' \
                          'ObererTol_I FLOAT, ' \
                          'UntererTol_II FLOAT, ' \
                          'ObererTol_II FLOAT, ' \
                          'UntererTol_III FLOAT, ' \
                          'ObererTol_III FLOAT, ' \
                          'Characteristic  CHAR(50),' \
                          'Description  CHAR(50),' \
                          'Point_Grade  INT,' \
                          'Consistency  CHAR(50),' \
                          'FM_POINT  CHAR(50),' \
                          'CS_Statistics  CHAR(50)' \
                          ')'

        #创建基础数据库
        cre_db_table(host, user, pw, database, table, base_table_byte)

       #sql3的数据库绝对路径
        base_db_lu_ling = base_data_addr + '\\' + 'Inline_base_' + sql3_db_car + '_' + sql3_db_part + '.db'
        # print(base_db_lu_ling)
        #连接sql3
        conn_base = sqlite3.connect(base_db_lu_ling)
        cur_base = conn_base.cursor()
        #执行语句
        data_mei_tian = "SELECT * FROM dmo_data "
        cur_base.execute(data_mei_tian)
        #sql3的所有数据
        point_base = cur_base.fetchall()
        #关闭数据库
        conn_base.close()

        print(point_base)
        for point in point_base:
            Point_Group='1'#点的组别
            PointName=point[0]#点名
            X_Position=point[1]#点的X方向位置
            Y_Position = point[2]#点的Y方向位置
            Z_Position = point[3]#点的Z方向位置
            i_Richtung = point[4]#点的X方向
            j_Richtung = point[5]#点的Y方向
            k_Richtung = point[6]#点的Z方向
            UntererTol = float(point[7])#标准下公差
            ObererTol = float(point[8])#标准上公差
            UntererTol_I=float(UntererTol)*0.75#1级下公差
            ObererTol_I=float(ObererTol)*0.75#1级上公差
            UntererTol_II = float(UntererTol)#2级下公差
            ObererTol_II = float(ObererTol)#2级上公差
            UntererTol_III = float(UntererTol) - 1.5#3级下公差
            ObererTol_III = float(ObererTol) + 1.5#3级上公差

            #点的测量原则
            if PointName[-4:][:2].isalpha():
                Characteristic=PointName[-4:][:2]
            else:
                Characteristic='none'

            # 点的描述
            Description= PointName[2:5]
            # 点的等级
            Point_Grade='1'
            #是否一致性监控
            Consistency='Yes'
            #是否功能尺寸点
            FM_POINT='No'
            #是否进行CS统计
            CS_Statistics='Yes'

            try:
                canshu = (table, Point_Group,PointName,X_Position,Y_Position,Z_Position,i_Richtung,j_Richtung,k_Richtung,UntererTol,
                          ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,
                          Description, Point_Grade,Consistency,FM_POINT,CS_Statistics)
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
                canshu = (table, Point_Group, PointName,UntererTol,ObererTol, UntererTol_I, ObererTol_I,
                          UntererTol_II, ObererTol_II, UntererTol_III, ObererTol_III,Characteristic,Description,
                          Point_Grade, Consistency, FM_POINT, CS_Statistics)
                print(canshu)
                print(type(PointName))
                # SQL 插入语句
                sql = """INSERT INTO %s (Point_Group,PointName,UntererTol,ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,
                                          ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,Description, Point_Grade,
                                          Consistency,FM_POINT,CS_Statistics)
                                                VALUES (%s,'%s',%s,%s,%s,%s,
                                                        %s,%s,%s,%s,'%s','%s',%s,'%s','%s','%s')""" % canshu
                print(sql)
                # 打开数据库连接
                db = pymysql.connect(host, user, pw, database, charset='utf8')
                # 使用cursor()方法获取操作游标
                cursor = db.cursor()
                # 执行sql语句
                print(sql)
                # cursor.execute(sql)
                try:
                    cursor.execute(sql)
                except:
                    print('点名有重复')

            # 提交到数据库执行
            db.commit()
    # 关闭数据库连接
    db.close()
    os.remove(base_db_lu_ling)

sql3_basic_to_mysql(sql3_db_list)
