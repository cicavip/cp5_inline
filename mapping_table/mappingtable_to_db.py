import xlrd,os
from mysql.create_database import cre_db_database
from mysql.create_table import cre_db_table
from mysql.into_data import into_data

host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd1'  # mysql的密码
map_database = 'MappingTable'#映射表数据据库名称
car_table='car'
part_table='part'
program_addr = os.path.split(os.path.realpath(__file__))[0]
mappingtable_excel_addr=os.path.split(program_addr)[0]+'\\'+'11_映射表'+'\\'+'映射表.xlsx'
car_sheet='car'
part_sheet='part'
table_byte='(standard CHAR(30) NOT NULL , notstandard CHAR(30) NOT NULL, primary key(standard,notstandard))'

cre_db_database(host, user, pw, map_database)
cre_db_table(host, user, pw, map_database,car_table,table_byte)
cre_db_table(host, user, pw, map_database,part_table,table_byte)

print(mappingtable_excel_addr)
workbook = xlrd.open_workbook(mappingtable_excel_addr)
car_sheet = workbook.sheet_by_name(car_sheet)
car_nrows = car_sheet.nrows
print(car_nrows)
for i in range(car_nrows):   # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    row_value=car_sheet.row_values(i)[:car_nrows]
    print(row_value)
    standard_car=row_value[1]
    notstandard_car = row_value[2]
    canshu=(map_database,car_table,standard_car,notstandard_car)

    sql = """INSERT INTO %s.%s (standard,notstandard)
                    VALUES ('%s', '%s')""" % canshu
    print(sql)
    into_data(host, user, pw, sql)

part_sheet = workbook.sheet_by_name(part_sheet)
part_nrows = part_sheet.nrows
print(part_nrows)
for i in range(part_nrows):   # 循环逐行打印
    if i == 0: # 跳过第一行
        continue
    row_value = part_sheet.row_values(i)[:part_nrows]
    print(row_value)
    standard_part = row_value[1]
    notstandard_part = row_value[2]
    canshu = (map_database, part_table, standard_part, notstandard_part)

    sql = """INSERT INTO %s.%s (standard,notstandard)
                        VALUES ('%s', '%s')""" % canshu
    print(sql)
    into_data(host, user, pw, sql)