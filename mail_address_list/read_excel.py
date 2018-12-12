# -*- coding: utf-8 -*-
import xlrd,os
from mysql.read_MappingTable import mappingtable_part,mappingtable_car
from mysql.into_data import into_data
host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd1'  # mysql的密码
map_database = 'MappingTable'#映射表数据据库名称


parts_list=[]
standard_parts = mappingtable_part(host, user, pw, map_database)[0]  # 映射表标准零件缩写的列表
for standard_part in standard_parts.values():
    parts_list.append(standard_part)
parts_list=list(sorted(set(parts_list)))#去重复的零件缩写

cars_list=[]
standard_cars = mappingtable_car(host, user, pw, map_database)[0]  # 映射表标准零件缩写的列表
for standard_car in standard_cars.values():
    cars_list.append(standard_car)
cars_list=list(sorted(set(cars_list)))#去重复的零件缩写

pro_addr = os.path.split(os.path.realpath(__file__))[0]
pro_addr=os.path.split(pro_addr)[0]+r'\05_在线测量预警名单确认'
excel_names=os.listdir(pro_addr)



for excel_name in excel_names:

    excel_addr=pro_addr+'\\'+excel_name
    sheet_name='收件人'
    workbook = xlrd.open_workbook(excel_addr)
    sheet = workbook.sheet_by_name(sheet_name)
    nrows=sheet.nrows

    for i in range(2, nrows, 1):
        rows = sheet.row_values(i)
        car = rows[1]
        part = rows[2]
        key_mail_addrs=car+'_'+part
        excel_mail_addrs = rows[4:]
        excel_mail_addrs = list(set(excel_mail_addrs))
        excel_mail_addrs.remove('')

        for mail_addr in excel_mail_addrs:

            if '@' not in mail_addr  :
                new_mail_addr= mail_addr
                mail_addr_name=new_mail_addr.split('.')[1]
                mail_addr_familyname=new_mail_addr.split('.')[0]
                mail_addr=mail_addr_name+'.'+mail_addr_familyname+'@faw-vw.com'

            print(mail_addr)
            print(standard_cars,standard_parts)
            st_car=standard_cars[car]
            st_part=standard_parts[part]
            table = 'mail_address'
            canshu=(st_car,table,st_part,mail_addr)
            # SQL 插入语句
            sql = """INSERT INTO %s.%s (Part, Address)
                             VALUES ('%s', '%s')""" % canshu
            print(sql)
            try:
                into_data(host, user, pw, sql)
            except:
                print('可能是重复了')