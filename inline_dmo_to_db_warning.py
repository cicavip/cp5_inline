import os,shutil,time
from mysql.read_MappingTable import mappingtable_car,mappingtable_part
from mysql.create_database import cre_db_database
from mysql.create_table import cre_db_table
from mysql.select_data import select_data
from dmo_parse.read_dmo_basic import read_dmo_basic
from dmo_parse.read_dmo_value import read_dmo_value
from dmo_parse.point_value_to_db import point_value_to_db
from inline_early_warning.warning_condition import inline_warining_condition


host = 'localhost'#mysql的ip或者本地的地址
user = 'root'#mydql的用户
pw = 'mysql-qd1'#mysql的密码
map_database = 'MappingTable'#映射表数据据库名称

program_addr = os.path.split(os.path.realpath(__file__))[0]

#dmo存放的绝对地址
dmo_file = program_addr+r'\DMO'
#读取dmo出现错误是的接收文件夹
dmo_error_file = program_addr+ r'\DMO_Error'
#有预警是这个文件夹会生成一个txt文件
gentxtfolder_addr= program_addr+r'\03_Gen_txt'#出现

dict_cars=mappingtable_car(host, user, pw, map_database)[0]#映射表车型的字典
# standard_cars=mappingtable_car(host, user, pw, map_database)[1]#映射表标准车型缩写的列表
dict_parts=mappingtable_part (host, user, pw, map_database)[0]#映射表零件的字典
# standard_parts=mappingtable_part (host, user, pw, map_database)[0]#映射表标准零件缩写的列表

tipdir = program_addr + '\\循环读取DMO不要删除.txt'
with open(tipdir, 'w') as f:pass


dmo_list = os.listdir(dmo_file)  # 获取dmo的名称列表
print(dmo_list)
#循环读取每个dmo把信息写入数据库
try:
    for dmo_name in dmo_list:

        # dmo的路径
        dmo_addr = dmo_file + '\\' + dmo_name
        print(dmo_addr)



        #在循环内定义一个共的点偏差字典和基本信息列表是为了每一个dmo都会刷新一下，这个每一都不会叠加。
        point_value_information = {}  # 点的偏差值字典，点名为键值为偏差
        basic_information = []  #列表基本信息：车型，零件，零件钢号，测量开始时间，测量结束时间

        # 点的偏差值字典，点名为键值为偏差
        point_value_information = read_dmo_value(dmo_addr,point_value_information)
        # 列表基本信息：车型，零件，零件钢号，测量开始时间，测量结束时间
        basic_information =read_dmo_basic(dmo_addr, basic_information)

        print(basic_information)
        print(point_value_information)

        car = dict_cars[basic_information[2]]#以dmo里面的 车型 缩写找到标准的 车型 缩写
        print(car)
        part = dict_parts[basic_information[0]]#以dmo里面的 零件 缩写找到标准的 零件 缩写

        #以标准的车型缩写创建对应的数据路
        cre_db_database(host, user, pw, car)

        dve_table= 'inline'+ '_' +'dev'+'_'+ part
        print(dve_table)
        dve_table_byte = '(ID INT NOT NULL auto_increment primary key,' \
                     'PointName CHAR(30) NOT NULL,' \
                     'Messwert FLOAT, ' \
                     'Identnummer  CHAR(30),' \
                     'StartDateTime  DATETIME ,' \
                     'EndDateTime  DATETIME ' \
                     ')'

        # 以标准的零件缩写创建对应的零件数据列表
        cre_db_table(host, user, pw, car, dve_table, dve_table_byte)
        print('2121212121')

        #将dmo的数据写入到数据库
        point_value_to_db(host, user, pw, car, dve_table, point_value_information, basic_information)

        dmo_point_names = []
        for point_name in point_value_information.keys():
            dmo_point_names.append(point_name)


        # #预警部分++++++++++++++++++++++++++++++++++++++++++++++++

        #提取基础数据库的点的名
        database=car#数据库名称
        base_table = 'inline_base_' + part#数据库的列表名称
        base_point_name_canshu=(database,base_table)
        basa_db_point_name_sql= "select PointName from %s.%s " % base_point_name_canshu


        #使用已编的函数读取，同时把点名转换为列表
        basa_db_point_names=list(list(zip(*select_data(host, user, pw,basa_db_point_name_sql)))[0])
        Intersection_point_name_list = list((set(dmo_point_names).union(set(basa_db_point_names))) ^ (set(dmo_point_names) ^ set(basa_db_point_names)))
        print(Intersection_point_name_list)
        print(basic_information)
        Identnummer=basic_information[1]
        EndDateTime=basic_information[5].replace("/", "-") + ' ' + basic_information[6]
        cal_n = 10
        WarningType = '未标记'
        inline_warining_condition(host, user, pw, car, part, Intersection_point_name_list,
                        Identnummer, cal_n, WarningType,gentxtfolder_addr,EndDateTime)

        #删除已写数据库的dmo
        os.remove(dmo_addr)

except :

    #读取错误的dmo
    error_dmo_addr= dmo_error_file + '\\' + dmo_name
    print(f'{dmo_name} 读取错误，dmo已移到<DMO_ERROR>文件夹')

    #将读取错误的dmo移动到对应的待处理文件夹
    shutil.move(dmo_addr,error_dmo_addr)

finally:
    os.remove(tipdir)


