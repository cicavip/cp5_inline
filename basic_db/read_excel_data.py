import xlrd,os,shutil,csv,pymysql
import pandas as pd
from basic_db.creat_basic_db import creat_basic_db
from mysql.create_database import cre_db_database


car='Bora_MQB'
parts=['RO2']
# parts=['RO1','RO2','RO5','STIL','STIR']

host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd1'  # mysql的密码
map_database = 'MappingTable'  # 映射表数据据库名称


program_addr = os.path.split(os.path.realpath(__file__))[0]
csv_data_addr=os.path.split(program_addr )[0]+r'\12_csv_data'
piweb_data_addr=os.path.split(program_addr )[0]+r'\13_piweb_data'

for part in  parts:
    db_table='inline_base_'+part
    database=car
    cre_db_database(host, user, pw, database)
    creat_basic_db(host, user, pw, database, db_table)
    csv_file_name_addr=csv_data_addr+'\\'+part
    csv_names = os.listdir(csv_file_name_addr)
    point_name_tol = {}
    names = []
    for csv_name in csv_names:
        filename=csv_file_name_addr+'\\'+csv_name
        print(filename)
        with open(filename) as namexyztol:
            reader = csv.reader(namexyztol)
            all_row_data=list(reader)
            row_datas=all_row_data.copy()
            row_datas_tol = all_row_data.copy()
            for row_data in all_row_data:
                # print(row_data)
                if '' not in row_data and 'Measurand' not in row_data :
                    name=row_data[0]+'.'+row_data[1]
                    names.append(name)
                    # print(names)
                    xyztol=[]
                    for xyz_data in row_datas:

                        if row_data[0]==xyz_data[0]:
                            xyztol.append(xyz_data[2])
                            if len(xyztol)==3:
                                for tol in row_datas_tol:
                                    if row_data[0] == tol[0] and row_data[1]==tol[1]:
                                        tol_data=tol[-6:]
                                        for tol123 in tol_data:
                                            xyztol.append(tol123)
                                            # print(xyztol)
                                            if len(xyztol)==9:

                                                group = filename.split('.')[0][-1]
                                                xyztol.append(group)
                                                # print(xyztol)
                                                point_name_tol[name] = xyztol
    print(point_name_tol)

    piweb_filename=piweb_data_addr+'\\'+part+'\\'+part+'.xlsx'
    print(piweb_filename)
    for point_fulname in point_name_tol.keys():
        print(point_fulname)

        table='Tabelle1'

        # print(piweb_filename)
        piweb_workbook = xlrd.open_workbook(piweb_filename)
        piweb_sheet = piweb_workbook.sheet_by_name(table)
        piweb_nrows = piweb_sheet.nrows
        for row_num in  range(piweb_nrows) :

            # print(point_name_tol[point_fulname])
            # print(row_num)


            row_data = piweb_sheet.row_values(row_num)[:piweb_nrows]
            if point_fulname in row_data:
                print('=============================================')
                print(row_data)

                X_Richtung=piweb_sheet.row_values(row_num+11)[2]
                Y_Richtung = piweb_sheet.row_values(row_num +12)[2]
                Z_Richtung = piweb_sheet.row_values(row_num +13)[2]

                print(X_Richtung,Y_Richtung,Z_Richtung)

                Point_Group =point_name_tol[point_fulname][9]  # 点的组别
                PointName = point_fulname  # 点名
                X_Position = point_name_tol[point_fulname][0]  # 点的X方向位置
                Y_Position = point_name_tol[point_fulname][1]  # 点的Y方向位置
                Z_Position = point_name_tol[point_fulname][2]  # 点的Z方向位置
                if X_Richtung =='Messdatum':
                    i_Richtung = '0'  # 点的X方向
                    j_Richtung = '0'  # 点的Y方向
                    k_Richtung = '1'  # 点的Z方向
                else:
                    i_Richtung = X_Richtung  # 点的X方向
                    j_Richtung = Y_Richtung  # 点的Y方向
                    k_Richtung = Z_Richtung  # 点的Z方向

                UntererTol = point_name_tol[point_fulname][5]  # 标准下公差
                ObererTol = point_name_tol[point_fulname][6]  # 标准上公差
                UntererTol_I = point_name_tol[point_fulname][3]  # 1级下公差
                ObererTol_I = point_name_tol[point_fulname][4]  # 1级上公差
                UntererTol_II = point_name_tol[point_fulname][5]  # 2级下公差
                ObererTol_II = point_name_tol[point_fulname][6]  # 2级上公差
                UntererTol_III = point_name_tol[point_fulname][7]  # 3级下公差
                ObererTol_III = point_name_tol[point_fulname][8]  # 3级上公差

                # 点的测量原则
                if PointName[-4:][:2].isalpha():
                    Characteristic = PointName[-4:][:2]
                else:
                    Characteristic = 'none'

                # 点的描述
                Description = PointName[2:5]
                # 点的等级
                Point_Grade = '1'
                # 是否一致性监控
                Consistency = 'Yes'
                # 是否功能尺寸点
                FM_POINT = 'No'
                # 是否进行CS统计
                CS_Statistics = 'Yes'

                canshu = (db_table, Point_Group, PointName, X_Position, Y_Position, Z_Position, i_Richtung, j_Richtung,
                          k_Richtung, UntererTol, ObererTol, UntererTol_I, ObererTol_I, UntererTol_II, ObererTol_II,
                          UntererTol_III,
                          ObererTol_III, Characteristic, Description, Point_Grade, Consistency, FM_POINT, CS_Statistics)
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
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                except:
                    print('基础数据库已有该点信息')
                # 提交到数据库执行
                db.commit()

                break












