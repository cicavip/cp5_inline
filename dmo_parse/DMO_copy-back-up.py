import os,shutil,datetime

from mysql.read_MappingTable import mappingtable_car,mappingtable_part
from dmo_parse.read_dmo_basic import read_dmo_basic




host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd'  # mysql的密码
map_database = 'MappingTable'  # 映射表数据据库名称

program_addr = os.path.split(os.path.realpath(__file__))[0]
lacol_dmo_file=os.path.split(program_addr)[0]+'\\'+'DMO'
print(lacol_dmo_file)

tipdir = program_addr + '\\DMO复制不要删除.txt'
with open(tipdir, 'w') as f:pass


dict_cars=mappingtable_car(host, user, pw, map_database)[0]#映射表车型的字典
dict_parts=mappingtable_part (host, user, pw, map_database)[0]#映射表零件的字典


# addr=r'\\10.236.64.30\dmo_mt\在离线.DMO\在线测量DMO'
addr=r'\\10.236.64.30\dmo_mt\Inline_Offline_DMO\Inline_DMO'

dmo_file_addr=addr+'\\'+'DMO'
dmo_names=os.listdir(dmo_file_addr)
while True:
    try:
        for dmo_name in dmo_names:
            dmo_addr = dmo_file_addr + '\\' + dmo_name
            lacol_dmo_addr = lacol_dmo_file + '\\' + dmo_name
            print(dmo_addr)
            basic_information=[]
            basic_information=read_dmo_basic(dmo_addr, basic_information)
            dmo_car=basic_information[2]
            dmo_part=basic_information[0]
            dmo_start=basic_information[3]
            day_time_q=basic_information[3].replace('/','-')+' '+basic_information[4]
            print(day_time_q)
            day_date=datetime.datetime.strptime(day_time_q,'%Y-%m-%d %H:%M:%S').date()

            if basic_information[4] > '08:30:00':
                print(day_date)
                dmo_file_name=str(day_date)
                backup_dmo_file = addr + '\\' + dict_cars[dmo_car] + '\\' + dict_parts[dmo_part] + '\\' + dmo_file_name
                backup_dmo_file_addr = backup_dmo_file+'\\'+dmo_name

                if os.path.exists(backup_dmo_file) == False:
                    os.makedirs(backup_dmo_file)
                shutil.copyfile(dmo_addr, backup_dmo_file_addr)
                shutil.copyfile(dmo_addr, lacol_dmo_addr)
                os.remove(dmo_addr)  # 删除原DMO



            else:
                print(day_date + datetime.timedelta(days=-1))
                dmo_file_name = str(day_date + datetime.timedelta(days=-1))
                backup_dmo_file = addr + '\\' + dict_cars[dmo_car] + '\\' + dict_parts[dmo_part] + '\\' + dmo_file_name
                backup_dmo_file_addr = addr + '\\' + dict_cars[dmo_car] + '\\' + dict_parts[
                    dmo_part] + '\\' + dmo_file_name + '\\' + dmo_name

                if os.path.exists(backup_dmo_file) == False:
                    os.makedirs(backup_dmo_file)
                shutil.copyfile(dmo_addr, backup_dmo_file_addr)
                shutil.copyfile(dmo_addr, lacol_dmo_addr)
                os.remove(dmo_addr)  # 删除原DMO
    except:
        print("复制时发生错误")

    finally:
        os.remove(tipdir)