
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

        gentxt_addr = gentxtfolder_addr + '\\' + car + '-' + part + '-' + Identnummer + '-' + point_name + '.txt'

        mess_vals = mess_vals_df.ix[[point_name], [1]].head(50)
        mess_vals_len = len(mess_vals)


        base_table = 'inline_base_' + part
        base_canshu = (database, base_table,point_name)
        base_info_sql = "select UntererTol,ObererTol from %s.%s where PointName = '%s'" % base_canshu
        # print(base_info_sql)
        base_info = list(select_data(host, user, pw, base_info_sql))

        if base_info == []: continue

        uptol = float(base_info[0][1])
        downtol = float(base_info[0][0])

        print(mess_vals_len)
        if mess_vals_len > 25:
            # print(mess_vals[1])
            point_std = mess_vals[1].std()#标准偏差
            # print(point_std)

            if point_std != 0:
                point_cp = (uptol - downtol) / (6 * point_std)  # 计算出这个点的cp值
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

            point_mean = mess_vals[1].mean()#平均数

            alarm_description = '该点出现断崖式变化'
            # print(mess_vals[:cal_n])
            last20_vals = mess_vals[:cal_n].reset_index(drop=True)#取出前20件的values
            # print(last20_vals)

            last20_vals_std = last20_vals[1].std()
            if last20_vals_std == 0: last20_vals_std = 0.001
            last20_vals_mean = last20_vals[1].mean()
            last20_index = last20_vals.index.tolist()

            index_list = []
            for i in last20_index:
                # z-score 标准化(zero-mean normalization)也叫标准差标准化，经过处理的数据符合标准正态分布
                # '''
                # 这种方法基于原始数据的均值（mean）和标准差（standard deviation）进行数据的标准化。将A的原始值x使用z-score标准化到x’。
                # z-score标准化方法适用于属性A的最大值和最小值未知的情况，或有超出取值范围的离群数据的情况。
                # spss默认的标准化方法就是z-score标准化。
                # 用Excel进行z-score标准化的方法：在Excel中没有现成的函数，需要自己分步计算，其实标准化的公式很简单。
                # 步骤如下：
                # 1.求出各变量（指标）的算术平均值（数学期望）xi和标准差si ；
                # 2.进行标准化处理：
                # zij=（xij－xi）/si
                # 其中：zij为标准化后的变量值；xij为实际变量值。
                # 3.将逆指标前的正负号对调。
                # 标准化后的变量值围绕0上下波动，大于0说明高于平均水平，小于0说明低于平均水平。
                # '''
                dui_bi_num = abs(float((last20_vals[1][i]) - last20_vals_mean) / last20_vals_std)
                # print(dui_bi_num)
                if dui_bi_num > 3:
                    index_list.append(i)

            new_last20_vals = last20_vals[1].drop(index_list)
            # print(new_last20_vals)
            # print(last20_vals[1])
            qian_mean = new_last20_vals[:10].mean()
            hou_mean = new_last20_vals[10:].mean()
            if abs(qian_mean) > 100 and abs(hou_mean) > 100:
                continue
            cha_zhi = abs(qian_mean - hou_mean)
            print(cha_zhi)

            if cha_zhi >1:
                # print(car,part,point_name)
                # print(last20_vals)
                # print(last20_index)
                # print(index_list)
                # print(qian_mean, hou_mean, cha_zhi)
                #抛出预警点文件
                with open(gentxt_addr, 'w') as f:
                    f.write(EndDateTime + '\n')
                    f.write(alarm_description)

                warning_table='inline_warning_'+part
                warning_record_table_byte = '(ID INT NOT NULL auto_increment primary key,' \
                                            'PointName CHAR(30) NOT NULL,' \
                                            'DifferenceValue  FLOAT, ' \
                                            'EndDateTime  DATETIME, ' \
                                            'Identnummer  CHAR(50),' \
                                            'WarningDescribe CHAR(200), ' \
                                            'Amount INT ,' \
                                            'WarningType  CHAR(100) ' \
                                            ')'

                cre_db_table(host, user, pw, database, warning_table, warning_record_table_byte)

                # print()
                canshu = (database, warning_table, point_name,cha_zhi, EndDateTime, Identnummer, alarm_description, cal_n,WarningType)
                record_sql = "insert into %s.%s(PointName,DifferenceValue,EndDateTime,Identnummer,WarningDescribe,Amount,WarningType) values('%s','%s','%s','%s','%s',%d,'%s')" % canshu
                print(record_sql)
                into_data(host, user, pw, record_sql)
                print('预警数据写入数据库')
                continue
# #
# # ###测试
# host = 'localhost'#mysql的ip或者本地的地址
# user = 'root'#mydql的用户
# pw = 'mysql-qd1'#mysql的密码
# car='Bora_MQB'
# part='RO1'
# point_name_list=['MLESB1201_HDLE.X','NLSHI0009_U_AA.Z','MRRWH0032_HEBA.X','NLRVO0005_R_DG.Y','NRRVO0001_U_CA.X']
# Identnummer= '58745545'
# cal_n=20
# WarningType='WEIBIAOZHI'
# #有预警是这个文件夹会生成一个txt文件
# gentxtfolder_addr=r'D:\01_MProject\cp5_inline\09_mail_point_txt'#出现
# EndDateTime='2018-10-31 10:12:22'
# while True:
#     inline_warining_condition(host, user, pw,car,part,point_name_list,Identnummer,cal_n,WarningType,gentxtfolder_addr,EndDateTime)