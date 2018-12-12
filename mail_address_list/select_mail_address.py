from mysql.select_data import select_data

def select_mail_addrs(host,user,pw,car,part):

    if 'PAD'in part:
        part=part[:3]
        print(part)

    table = 'mail_address'
    canshu = (car, table, part)
    sql = "select Address from %s.%s where Part='%s' " % canshu
    print(sql)
    mail_addrs=select_data(host, user, pw, sql)
    mail_addrs=list(list(zip(*mail_addrs))[0])
    print(mail_addrs)
    str_mail_addrs = ''
    for i in mail_addrs:
        str_mail_addrs = str_mail_addrs + i + ';'
    # print(str_mail_addrs)
    return str_mail_addrs
# host = 'localhost'  # mysql的ip或者本地的地址
# user = 'root'  # mydql的用户
# pw = 'mysql-qd'  # mysql的密码
# map_database = 'MappingTable'#映射表数据据库名称
# car='Bora_MQB'
# part='ub2'
# print(select_mail_addrs(host,user,pw,car,part))
