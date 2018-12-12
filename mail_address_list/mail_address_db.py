
from mysql.create_table import cre_db_table
from mysql.read_MappingTable import mappingtable_part,mappingtable_car

host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd'  # mysql的密码
map_database = 'MappingTable'#映射表数据据库名称
cars=['Bora_MQB']

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

print(standard_parts)
print(parts_list)
print(cars_list)

def  creat_db(car):
    database=car
    table='mail_address'
    # table_byte = '(ID INT NOT NULL auto_increment primary key,' \
    #                       'Part CHAR(50) NOT NULL ,' \
    #                       'Address  CHAR(50) NOT NULL' \
    #              ')'
    table_byte = '(Part CHAR(50) NOT NULL ,' \
                 'Address  CHAR(50) NOT NULL,' \
                 'primary key(Part,Address)'\
                 ')'
    cre_db_table(host, user, pw, database, table, table_byte)
for car in cars:
 creat_db(car)