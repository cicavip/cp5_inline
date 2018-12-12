
import pandas as pd
# from inline_cp4.programs.OperationMysql.select_data import select_data
# from inline_cp4.programs.OperationMysql.create_table import create_db_table
# from inline_cp4.programs.OperationMysql.into_data import into_data


import pandas as pd
from mysql.select_data import select_data
from mysql.create_table import cre_db_table
from mysql.into_data import into_data

def inline_warining_condition(host, user, pw,car,part,point_name_list,Identnummer,cal_n,WarningType,gentxtfolder_addr,EndDateTime):
    print('开始进入预警判断')
    database=car
    table='inline_dev_'+part
    canshu=(database,table)
    sql = "select PointName,Messwert from %s.%s order by EndDateTime desc limit 0,40000" %canshu
    mess_vals = list(select_data(host, user, pw, sql))
    mess_vals_df = pd.DataFrame(mess_vals).set_index(0)

    for point_name in point_name_list:
        # print(point_name)
        gentxt_addr = gentxtfolder_addr + '\\' + car + '-' + part + '-' + Identnummer + '-' + point_name + '.txt'

        mess_vals = mess_vals_df.ix[[point_name], [1]].head(50)
        mess_vals_len = len(mess_vals)
        # print(mess_vals_len)

        base_table = 'inline_base_' + part
        base_canshu = (database, base_table,point_name)
        base_info_sql = "select UntererTol,ObererTol from %s.%s where PointName = '%s'" % base_canshu
        # print(base_info_sql)
        base_info = list(select_data(host, user, pw, base_info_sql))
        # print(base_info)

        if base_info == []: continue

        uptol = float(base_info[0][1])
        downtol = float(base_info[0][0])

        max_warning_value = 50
        min_warning_value=abs(uptol-downtol)*0.75
        # print('min_warning_value', min_warning_value)

        if min_warning_value < 1 :
            min_warning_value=1
        elif min_warning_value > 2.5:
            min_warning_value = 2.5

        if mess_vals_len > 25:
            point_std = mess_vals[1].std()
            # print('1212121',point_std)

            if point_std != 0:
                point_cp = (uptol - downtol) / (6 * point_std)  # 计算出这个点的cp值
                # print(point_cp)
                # if point_cp < 0.1:
                #     print(point_name+'该点CP值小于0.1'+str(point_val))
                #     with open(gentxt_addr,'w') as f:
                #         f.write(nyr+'\n')
                #         f.write('该点CP值小于0.1')
            else:
                pass
                # print(point_name+'计算出的西格玛为0')
        else:
            pass
            # print('测量次数少于3次，不计算cp值')



        if mess_vals_len >= 50:

            point_mean = mess_vals[1].mean()

            alarm_description = '该点出现断崖式变化'
            last20_vals = mess_vals[:cal_n].reset_index(drop=True)
            # print(last20_vals)

            last20_vals_std = last20_vals[1].std()#计算标准差
            if last20_vals_std == 0: last20_vals_std = 0.001
            last20_vals_mean = last20_vals[1].mean()
            last20_index = last20_vals.index.tolist()
            # print(last20_index)

            index_list = []
            for i in last20_index:

                dui_bi_num = abs(float((last20_vals[1][i]) - last20_vals_mean) / last20_vals_std)
                # print(dui_bi_num)
                if dui_bi_num > 2.5:
                    index_list.append(i)

            new_last20_vals = last20_vals[1].drop(index_list)
            print(new_last20_vals)
            qian_mean = new_last20_vals[:5].mean()
            hou_mean = new_last20_vals[5:].mean()
            if abs(qian_mean) > 100 and abs(hou_mean) > 100:
                continue
            cha_zhi = abs(qian_mean - hou_mean)
            print('cha_zhi',cha_zhi)

            # if 0.12 > cha_zhi and cha_zhi > 0.1:
            if max_warning_value > cha_zhi and cha_zhi > min_warning_value:
                # print(car,part,point_name)
                # print(last20_vals)
                # print(last20_index)
                # print(index_list)
                # print(qian_mean, hou_mean, cha_zhi)

                with open(gentxt_addr, 'w') as f:
                    f.write(EndDateTime + '\n')
                    f.write(alarm_description)

                WarningID=car+'_'+part+'_'+point_name.replace('.','')+'_'+EndDateTime.replace('-','').replace(' ','').replace(':','')
                # print(WarningID)
                warning_table='inline_warning_'+part
                warning_record_table_byte = '(WarningID CHAR(100) NOT NULL,' \
                                            'PointName CHAR(100) NOT NULL,' \
                                            'DifferenceValue  FLOAT, ' \
                                            'EndDateTime  DATETIME, ' \
                                            'Identnummer  CHAR(50),' \
                                            'WarningDescribe CHAR(50), ' \
                                            'Amount INT ,' \
                                            'WarningType  CHAR(200), ' \
                                            'WarningReason  CHAR(250), ' \
                                            'AdjustReason  CHAR(250), ' \
                                            'Principal  CHAR(50), ' \
                                            'Departments  CHAR(80), ' \
                                            'Solution  CHAR(250), ' \
                                            'TimeNode  CHAR(250) ' \
                                            ')'

                cre_db_table(host, user, pw, database, warning_table, warning_record_table_byte)

                # print()
                canshu = (database,warning_table,WarningID, point_name,cha_zhi, EndDateTime, Identnummer, alarm_description, cal_n,WarningType)
                record_sql = "insert into %s.%s(WarningID,PointName,DifferenceValue,EndDateTime,Identnummer,WarningDescribe,Amount,WarningType) " \
                             "values('%s','%s','%s','%s','%s','%s','%s','%s')" % canshu
                print(record_sql)
                into_data(host, user, pw, record_sql)
                print('预警数据写入数据库')
                continue


# ###测试
# host = 'localhost'#mysql的ip或者本地的地址
# user = 'root'#mydql的用户
# pw = 'LISON23354!'#mysql的密码
# car='TROC'
# part='RO1PAD'
# point_name_list=['MLFAV1201_ODCA.X','MLFAV1201_ODCA.Y','MLFAV1201_ODCA.Z','MRFAV1201_ODCA.X','MRFAV1201_ODCA.Y']
# Identnummer= '58745545'
# cal_n=20
# WarningType='WEIBIAOZHI'
# #有预警是这个文件夹会生成一个txt文件
# gentxtfolder_addr=r'D:\Python\Python_Project\cp4_2_inline\03_Gen_txt'#出现
# EndDateTime='2018-10-20 10:12:22'
# inline_warining_condition(host, user, pw,car,part,point_name_list,Identnummer,cal_n,WarningType,gentxtfolder_addr,EndDateTime)