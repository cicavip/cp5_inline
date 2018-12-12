import datetime,os,shutil,traceback,time
import pandas as pd
import numpy as np
import win32com.client as win32
from cp5_inline.mysql.select_data import select_data
from cp5_inline.mysql.read_MappingTable import mappingtable_part
from cp5_inline.mail_address_list.select_mail_address import select_mail_addrs
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid')

host = 'localhost'  # mysql的ip或者本地的地址
user = 'root'  # mydql的用户
pw = 'mysql-qd1'  # mysql的密码
map_database = 'MappingTable'#映射表数据据库名称
car_map_dict = {'Bora_MQB': 'Bora_MQB', }
pro_addr = os.path.split(os.path.realpath(__file__))[0]
excel_question_addr =os.path.split(pro_addr)[0]+ r'\02_alert_sheet\问题单模板\在线测量预警问题单模板.xlsx'
share_folder_addr = r'\\msnasst-qd1-00\P-Q-QD-MT\01_数据管理组\在线测量预警\04_预警问题单'

part_list = []
standard_parts = mappingtable_part(host, user, pw, map_database)[0]  # 映射表标准零件缩写的列表
for standard_part in standard_parts.values():
    part_list.append(standard_part)
part_list = list(set(part_list))  # 去重复的零件缩写


def gen_question_sheet(warning_point_name,bao_jing_datetime,car,part):

    """
    :param warning_point_name: 预警的点名
    :param bao_jing_datetime: 预警的时间
    :param car: 对应车型
    :param part: 零件
    :return: 问题单的存放和问题单，预警的点的名称
    """

    #把时间转化为字符串格式
    occur_datatime = datetime.datetime.strptime(bao_jing_datetime, "%Y-%m-%d %H:%M:%S")
    print('gggggggggggggggg',occur_datatime)
    #建时间转化为周表示
    nzx_tuple = occur_datatime.isocalendar()
    #读取周的格式
    zhou_ci = str(nzx_tuple[0])[-2:] + 'KW' + ('0' + str(nzx_tuple[1]))[-2:] + '-' + str(nzx_tuple[2])

    basic_table='inline_base_'+part   #mysqll对应的基础数据库的列表名称
    canshu=(car,basic_table,warning_point_name)
    sql = "select * from %s.%s  where PointName = '%s' " % canshu

    #读取预警的点的基础信息
    base_info_df=list(zip(*select_data(host, user, pw, sql)))
    print(base_info_df)
    car_type = car_map_dict[car]

    #将点的各个信息赋给各个变量
    point_description=base_info_df[17][0]#点的描述
    point_feature=base_info_df[16][0]#点的特征
    point_grade=base_info_df[18][0]#点的等级程度
    point_standard_up_tol=base_info_df[9][0]#标准上公差
    point_standard_down_tol = base_info_df[8][0]#标准下公差
    point_3grade_up_tol=base_info_df[15][0]#3级上公差
    point_3grade_down_tol=base_info_df[14][0]#3级下公差

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True
    excel.DisplayAlerts = False
    con = win32.constants
    wb = excel.Workbooks.Open(excel_question_addr)
    wb.Worksheets('点名').Name = warning_point_name
    sheet = wb.Worksheets(warning_point_name)

    #将点的各个信息写入对应excel的表格
    sheet.Cells(4, 3).Value = car_type
    sheet.Cells(5, 3).Value = part
    sheet.Cells(6, 3).Value = warning_point_name
    sheet.Cells(7, 2).Value = point_description
    sheet.Cells(10, 2).Value = point_feature
    sheet.Cells(10, 4).Value = str(point_grade)
    sheet.Cells(12, 2).Value = point_standard_down_tol
    sheet.Cells(12, 4).Value = point_standard_up_tol
    sheet.Cells(14, 2).Value = point_3grade_down_tol
    sheet.Cells(14, 4).Value = point_3grade_up_tol
    print('ffffffffffffff',occur_datatime,type(occur_datatime))
    sheet.Cells(2, 7).Value = str(occur_datatime)
    sheet.Cells(2, 'M').Value = zhou_ci

    database=car
    dve_table='inline_dev_'+part

    #读取之前的80个测量值
    canshu = (database, dve_table, warning_point_name, occur_datatime)
    sql = "select Messwert from %s.%s where PointName = '%s' and EndDateTime <= '%s' order by EndDateTime desc limit 0,80" % canshu
    p_vals_1 = pd.DataFrame(list(select_data(host, user, pw, sql))[::-1])
    # print(p_vals_1)

    # 读取之后的20个测量值
    canshu = (database, dve_table,  warning_point_name, occur_datatime)
    sql = "select Messwert from %s.%s where PointName = '%s' and EndDateTime > '%s' order by EndDateTime limit 0,20" % canshu
    p_vals_2 = pd.DataFrame(list(select_data(host, user, pw, sql)))
    # print(p_vals_2)

    #把两个读出来的测量值合并在一起
    p_vals_hebing = pd.concat([p_vals_1, p_vals_2], ignore_index=True)
    p_vals = p_vals_hebing
    print(p_vals)

    # 读取之前的80个测量结束时间
    paramt_x = (database, dve_table, warning_point_name, occur_datatime)
    sql_x = "select EndDateTime from %s.%s where PointName = '%s' and EndDateTime <= '%s' order by EndDateTime desc limit 0,80" % paramt_x
    temp = list(select_data(host, user, pw, sql_x))[::-1]
    print(temp)

    # 读取之后的20个测量结束时间
    sql_x1 = "select EndDateTime from %s.%s where PointName = '%s' and EndDateTime > '%s' order by EndDateTime limit 0,20" % paramt_x
    temp1 = list(select_data(host, user, pw, sql_x1))
    print(temp1)

    #把开始和结束时间赋给变量
    start_time = temp[0][0]
    end_time = temp[-1][0]
    start_time = datetime.datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strftime(end_time, "%Y-%m-%d %H:%M:%S")
    sheet.Cells(3, 'J').Value = str(start_time)
    sheet.Cells(3, 'N').Value = str(end_time)


    p_vals_list = p_vals[0].values.tolist()
    p_vals_mean = p_vals[0].mean()#计算平均值
    p_vals_std = p_vals[0].std()#计算标准差
    up_control = 3 * p_vals_std + p_vals_mean#上控制线
    down_control = -3 * p_vals_std + p_vals_mean#下控制线

    list_len = len(temp)
    for k in range(0, list_len, 10):
        list_10 = p_vals_list[k:k + 10]
        max_val = np.max(list_10)
        min_val = np.min(list_10)
        max_index = list_10.index(max_val)
        min_index = list_10.index(min_val)
        max_excel_column = max_index + k + 2
        min_excel_column = min_index + k + 2

        sheet.Cells(71, max_excel_column).Value = max_val
        sheet.Cells(71, min_excel_column).Value = min_val

    for i in range(list_len):
        val = p_vals.at[i, 0]
        mess_time = temp[i]
        sheet.Cells(64, i + 2).Value = mess_time
        sheet.Cells(65, i + 2).Value = val
        sheet.Cells(66, i + 2).Value = p_vals_mean
        sheet.Cells(67, i + 2).Value = up_control
        sheet.Cells(68, i + 2).Value = down_control
        sheet.Cells(69, i + 2).Value = point_standard_up_tol
        sheet.Cells(70, i + 2).Value = point_standard_down_tol

    max_column = i + 2

    # 插入图片

    picture_addr = os.path.split(pro_addr)[0] + '\\10_Inline_photo\\' + car + '\\' + part + '\\' + warning_point_name + '.JPG'
    print(picture_addr)
    picture_left = sheet.Cells(17, 'A').Left
    picture_top = sheet.Cells(17, 'A').Top
    picture_width = sheet.Cells(17, 'A').Width * 4
    picture_height = sheet.Cells(17, 'A').Height * 11

    try:
        sheet.Shapes.AddPicture(picture_addr, 1, 1, picture_left, picture_top, picture_width, picture_height)
    except:
        print('图片库里没有' + car + ' ' + part + ' ' + warning_point_name + '图片')

    # 插入图表
    chartObjectLeft = sheet.Cells(5, 'E').Left
    chartObjectTop = sheet.Cells(5, 'E').Top
    chartObjectWidth = sheet.Cells(5, 'E').Width * 12
    chartObjectHeight = sheet.Cells(5, 'E').Height * 11
    chartObject = sheet.ChartObjects().Add(chartObjectLeft, chartObjectTop, chartObjectWidth, chartObjectHeight)
    chart = chartObject.Chart

    chartObject.Name = '时间序列'
    chart.ChartType = con.xlLine
    chart.ApplyLayout(1)
    chart.ChartTitle.Delete()
    chart.Axes(con.xlCategory).Delete()
    chart.Legend.Delete()
    chart.Axes(con.xlValue, con.xlPrimary).AxisTitle.Text = "mm"
    chart.Axes(con.xlValue).MajorGridlines.Format.Line.Visible = 0

    series1 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(1).MarkerStyle = con.xlMarkerStyleCircle
    series1.Values = sheet.Range(sheet.Cells(65, 'B'), sheet.Cells(65, max_column))

    series2 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(2).MarkerStyle = con.xlMarkerStyleNone
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    chart.SeriesCollection(2).Format.Line.ForeColor.RGB = 50
    chart.SeriesCollection(2).Format.Line.Weight = 0.25
    series2.Values = sheet.Range(sheet.Cells(66, 'B'), sheet.Cells(66, max_column))

    series3 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(3).MarkerStyle = con.xlMarkerStyleNone
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    chart.SeriesCollection(3).Format.Line.ForeColor.RGB = 255
    chart.SeriesCollection(3).Format.Line.Weight = 0.25
    series3.Values = sheet.Range(sheet.Cells(67, 'B'), sheet.Cells(67, max_column))

    series4 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(4).MarkerStyle = con.xlMarkerStyleNone
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    chart.SeriesCollection(4).Format.Line.ForeColor.RGB = 255
    chart.SeriesCollection(4).Format.Line.Weight = 0.25
    series4.Values = sheet.Range(sheet.Cells(68, 'B'), sheet.Cells(68, max_column))

    series5 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(5).MarkerStyle = con.xlMarkerStyleNone
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    chart.SeriesCollection(5).Format.Line.ForeColor.RGB = 180
    chart.SeriesCollection(5).Format.Line.Weight = 0.25
    chart.SeriesCollection(5).Format.Line.DashStyle = 2
    series5.Values = sheet.Range(sheet.Cells(69, 'B'), sheet.Cells(69, max_column))

    series6 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(6).MarkerStyle = con.xlMarkerStyleNone
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    chart.SeriesCollection(6).Format.Line.ForeColor.RGB = 180
    chart.SeriesCollection(6).Format.Line.Weight = 0.25
    chart.SeriesCollection(6).Format.Line.DashStyle = 2
    series6.Values = sheet.Range(sheet.Cells(70, 'B'), sheet.Cells(70, max_column))

    series7 = chart.SeriesCollection().NewSeries()
    chart.SeriesCollection(7).Format.Line.ForeColor.RGB = 230
    chart.SeriesCollection(7).MarkerStyle = con.xlMarkerStyleNone
    chart.SeriesCollection(7).ApplyDataLabels()
    chart.SeriesCollection(7).DataLabels().Position = 0
    chart.SeriesCollection(7).Format.Line.Visible = 0
    # chart.SeriesCollection(2).Format.Line.ForeColor.ObjectThemeColor = 6
    series7.Values = sheet.Range(sheet.Cells(71, 'B'), sheet.Cells(71, max_column))

    # n = 0
    row = 82
    sheet.Cells(16, 'N').Value = str(occur_datatime.date())
    none_Messwert = 0#用于控制之前有很多天没有测测量值而导致不停循环关闭的条件之一
    while True:
        day_datetime_strat = str(occur_datatime.date()) + ' ' + '08:30:00'
        night_datetime_strat = str(occur_datatime.date()) + ' ' + '19:30:00'
        night_date_end = occur_datatime.date() + datetime.timedelta(days=1)
        night_datetime_end = str(night_date_end) + ' ' + '08:30:00'

        canshu = (database, dve_table, warning_point_name, day_datetime_strat, night_datetime_strat)
        day_sql = "select Messwert from %s.%s where PointName = '%s' and EndDateTime between '%s' and '%s'" % canshu
        day_data =select_data(host, user, pw, day_sql)
        print(day_data)

        if day_data != ():
            day_df = pd.DataFrame(list(day_data))
            kai_pan = day_df[0].quantile(0.25)
            pan_gao = day_df[0].quantile(1)
            pan_di = day_df[0].quantile(0)
            shou_pan = day_df[0].quantile(0.75)

            sheet.Cells(row, 5).Value = str(occur_datatime.date()) + '白'
            sheet.Cells(row, 6).Value = round(kai_pan,2)
            sheet.Cells(row, 7).Value = round(pan_gao,2)
            sheet.Cells(row, 8).Value = round(pan_di,2)
            sheet.Cells(row, 9).Value = round(shou_pan,2)

            row = row - 1

        canshu = (database, dve_table, warning_point_name, night_datetime_strat, night_datetime_end)
        night_sql = "select Messwert from %s.%s where PointName = '%s' and EndDateTime between '%s' and '%s'" % canshu
        night_data = select_data(host, user, pw, night_sql)
        print(night_data)

        if night_data != ():
            night_df = pd.DataFrame(list(night_data))
            kai_pan = night_df[0].quantile(0.25)
            pan_gao = night_df[0].quantile(1)
            pan_di = night_df[0].quantile(0)
            shou_pan = night_df[0].quantile(0.75)

            sheet.Cells(row, 5).Value = str(occur_datatime.date()) + '夜'
            sheet.Cells(row, 6).Value = kai_pan
            sheet.Cells(row, 7).Value = pan_gao
            sheet.Cells(row, 8).Value = pan_di
            sheet.Cells(row, 9).Value = shou_pan

            row = row - 1


        if  day_data == () and night_data == ():
            none_Messwert = none_Messwert+1

        if row < 73 or none_Messwert > 20: break#判断是否跳出循环：行数小于73（因为盒型图的数据在82~73行和连续20天没有测量值）
        occur_datatime = occur_datatime - datetime.timedelta(days=1)
    sheet.Cells(16, 'J').Value = str(occur_datatime.date())

    excel_question_save_addr = os.path.split(pro_addr)[0]+r'\02_alert_sheet' + '\\' + car + '_' + part + '_' + warning_point_name + '_' + '在线测量预警问题单.xlsx'
    wb.SaveAs(excel_question_save_addr)
    excel.DisplayAlerts = True
    # wb.Close()
    excel.Quit()

    return excel_question_save_addr,warning_point_name


def sendmail(receiver,info,time,reason,check,pho_addr,excel_question_save_share_addr):

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = receiver
    # mail.Cc = receivers
    mail.Subject = '在线测量预警'
    body = '测量信息：'+info+'\n'+\
           '测量时间：'+time+'\n'+'报警原因：'+reason
    # mail.Body = body
    if check == 1:
        # mail.Attachments.Add(excel_question_save_addr)
        mail.Attachments.Add(pho_addr)
        mail.HTMLBody = '<html>' \
                        "<p> 各位同事好： </p>" \
                        "<p> 本邮件是智能测量系统【在线测量】，尺寸自动预警  </p>" \
                        "<p> 若有疑问请联系：测量技术科，数据管理组，xiaobin.qiu@faw-vw.com，也可以联系haibin.qiu.qd，+86-532-55536598</p>" \
                        "<p>   </p>" \
                        "<p>邮件为自动发送请勿回复，谢谢</p>" \
                        "<p>提示：1.预警邮件过多时，邮箱请手动设定存档规则</p>" \
                        "<p>提示：2.如果《问题单》没有访问权限，请联系数据管理组。</p>" \
                        "<p>   </p>" \
                        "<p>预警信息简略版如下:</p>" \
                        "<p>   </p>" \
                        "<p><a href="+'"'+excel_question_save_share_addr+'"'+">问题单</a></p>" \
                        '<p>'+body+"</p><p>趋势：" \
                        "</p><img src='cid:image.png' height=432 width=864>"
    mail.Send()


rule = '该点出现断崖式变化'
tipdir = pro_addr+'\\sendmail不要删除.txt'
with open(tipdir,'w') as f : pass

# describe_info = "\n各位同事好：\n\t本邮件是焊装在线测量【尺寸自动预警】\n\t若有疑问请联系：测量技术科，数据管理组，HongLin.Chen@faw-vw.com，也可以联系bin.zhang.cp4，63930454\n\n\t\t谢谢\n\n\t预警信息简略版如下:\n\n"
remove_point = ['MLRWS0021iODDG','MRLDL1001','QLLVI1001iUAZZ.Y']
mail_point_txt_folder_addr = os.path.split(pro_addr)[0]+'\\09_mail_point_txt'




# receiver = '''
#                 risheng.li@faw-vw.com;
#             '''



fdir = os.path.split(pro_addr)[0]+'\\03_Gen_txt'
flist = os.listdir(fdir)
dic = {}

for f in flist:
    faddr = fdir+'\\'+f
    ctime = os.stat(faddr).st_ctime
    dic[f] = ctime

sort_list = sorted(dic.items(),key=lambda item:item[1],reverse=False)
print(sort_list)

try:
    for f in sort_list:
        fname = f[0]
        info = fname.split('.txt')[0]
        car = info.split('-')[0]
        part = info.split('-')[1]
        # ganghao = info.split('-')[2]

        receiver = select_mail_addrs(host, user, pw, car, part)#读取对应车型和零件的发邮件的名单
        print(receiver)
        if part not in part_list:
            os.remove(fdir + '\\' + fname)
            continue

        point_name = info.split('-')[3]
        print(point_name)

        check_remove = 0
        for p in remove_point:
            if p in point_name:
                check_remove = 1
                break
        if check_remove == 1:
            os.remove(fdir + '\\' + fname)
            continue

        with open(fdir+'\\'+fname,'r') as file:
            time = file.readline().replace('\n','')
            print('54545454')
            print(time)
            reason = file.readline().replace('\n','')

        check = 0
        print(rule)
        print(reason)
        if reason == rule:
            check = 1
            dve_table = 'inline_dev_' + part
            sql1 = "select Messwert from %s.%s where PointName='%s' and EndDateTime<='%s' order by EndDateTime desc limit 0,20" %(car,dve_table,point_name,time)
            sql2 = "select EndDateTime from %s.%s where PointName='%s' and EndDateTime<='%s' order by EndDateTime desc limit 0,20" %(car,dve_table,point_name,time)

            val6_df = pd.DataFrame(list(select_data(host, user, pw, sql1)))[::-1]

            print(val6_df)
            val6_series = val6_df[0].abs()
            val6_series_smaller1_len = len(val6_series[val6_series < 1])
            val6_series_max = val6_series.max()
            if val6_series_smaller1_len>=13 and val6_series_max>3:
                os.remove(fdir + '\\' + fname)
                continue

            val6_series_bigger3_len = len(val6_series[val6_series > 3])
            if val6_series_bigger3_len >= 14:
                os.remove(fdir + '\\' + fname)
                continue

            sub_df_1 = val6_df[[0]][:-1].reset_index(drop=True)
            sub_df_2 = val6_df[[0]][1:].reset_index(drop=True)
            ret_df = sub_df_1.sub(sub_df_2,axis=0)
            ret_series = ret_df[0].abs()
            ret_series_bigger3_len = len(ret_series[ret_series>=3])
            if ret_series_bigger3_len>3:
                os.remove(fdir + '\\' + fname)
                print('有3个以上差值大于3')
                continue

            ret_series_bigger4_len = len(ret_series[ret_series > 4])
            ret_series_smaller2_len = len(ret_series[ret_series < 1.5])
            if ret_series_bigger4_len == 1 and ret_series_smaller2_len>15:
                os.remove(fdir + '\\' + fname)
                print('只有一个差值大于4')
                continue

            ret_series_bigger2_len = len(ret_series[ret_series > 2])
            if ret_series_bigger2_len > 11:
                os.remove(fdir + '\\' + fname)
                print('差值大于2的数量大于11')
                continue

            val6_time_df = pd.DataFrame(list(select_data(host, user, pw,sql2)))
            val6_time_df[[0]] = val6_time_df[[0]].astype(str)
            val6_df[[0]] = val6_df[[0]].astype(float)
            val6_df.plot()

            plt.gcf().set_size_inches(10,5)
            for i in range(len(val6_df)):
                val = val6_df.iloc[i, 0]
                plt.text(19-i, val, str(val), family='serif', style='italic', ha='center', wrap=True, alpha=0.5, size=10)#标注
            plt.xticks(range(20), np.array(val6_time_df), rotation=30, fontsize=7)  # 自定义横坐标值
            plt.legend(['InlineDev'])  # 图例名称
            plt.subplots_adjust(left=0.06, right=0.95, bottom=0.2, top=0.99)  # 调整图形边距

            pho_addr = pro_addr + '\\image.png'
            plt.savefig(pho_addr)

        mail_point_txt_addr = mail_point_txt_folder_addr + '\\' + car + '-' + part + '-' + point_name + '.txt'
        check_mail_point = os.path.exists(mail_point_txt_addr)

        os.remove(fdir + '\\' + fname)

        #同一问题30分钟内不重复发送
        if check_mail_point:

            with open(mail_point_txt_addr, 'r') as file:
                last_datetime = file.readline().replace('\n', '')
                last_datetime = datetime.datetime.strptime(last_datetime, "%Y-%m-%d %H:%M:%S")
            now_datetime = datetime.datetime.now()
            interval_minute = (now_datetime - last_datetime).total_seconds() / 60

            if abs(interval_minute) < 45:
                continue
            else:
                print('kkkkkkkk',time)
                excel_question_save_addr = gen_question_sheet(point_name, time, car, part)
                if excel_question_save_addr != '':
                    point_name_i = excel_question_save_addr[1]
                    # sendmail(receiver, info, time, reason, check, pho_addr,excel_question_save_share_addr)
                    with open(mail_point_txt_addr, 'w') as f:
                        now_datetime = datetime.datetime.now()
                        now_datetime = datetime.datetime.strftime(now_datetime, "%Y-%m-%d %H:%M:%S")
                        f.write(now_datetime + '\n')

                    date_str = str(datetime.datetime.now().date())
                    nian = date_str.split('-')[0]
                    yue = date_str.split('-')[1]
                    nian_yue = nian + '-' + yue
                    year_folder = share_folder_addr + '\\' + nian + '\\' + nian_yue + '\\' + date_str
                    if not os.path.exists(year_folder):
                        os.makedirs(year_folder)
                    riqi = date_str.replace('-', '')
                    shijian = str(datetime.datetime.now().time()).split('.')[0].replace(':', '')
                    excel_datetime = riqi + shijian
                    excel_question_save_share_addr = year_folder + '\\' + car + '_' + part + '_' + point_name_i + '_' + excel_datetime + '_在线测量预警问题单.xlsx'
                    shutil.copyfile(excel_question_save_addr[0],excel_question_save_share_addr)
                    sendmail(receiver, info, time, reason, check, pho_addr, excel_question_save_share_addr)

        else:
            print('kkkkkkkk', time)
            excel_question_save_addr = gen_question_sheet(point_name, time, car, part)
            if excel_question_save_addr != '':
                point_name_i = excel_question_save_addr[1]
                # sendmail(receiver, info, time, reason, check, pho_addr,excel_question_save_share_addr)
                with open(mail_point_txt_addr, 'w') as f:
                    now_datetime = datetime.datetime.now()
                    now_datetime = datetime.datetime.strftime(now_datetime, "%Y-%m-%d %H:%M:%S")
                    f.write(now_datetime + '\n')

                date_str = str(datetime.datetime.now().date())
                nian = date_str.split('-')[0]
                yue = date_str.split('-')[1]
                nian_yue = nian+'-'+yue
                year_folder = share_folder_addr + '\\' + nian + '\\' + nian_yue+'\\'+date_str
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                riqi = date_str.replace('-', '')
                shijian = str(datetime.datetime.now().time()).split('.')[0].replace(':', '')
                excel_datetime = riqi + shijian
                excel_question_save_share_addr = year_folder + '\\' + car + '_' + part + '_' + point_name_i + '_' + excel_datetime + '_在线测量预警问题单.xlsx'
                print(excel_question_save_share_addr)
                shutil.copyfile(excel_question_save_addr[0], excel_question_save_share_addr)
                sendmail(receiver, info, time, reason, check, pho_addr, excel_question_save_share_addr)

        if check == 1:
            # pass
            try:
                os.remove(pro_addr + '\\image.png')
            except:pass
except:
    now_datetime = str(datetime.datetime.now())
    print(now_datetime)
    txt_name = now_datetime.split('.')[0].replace('-', '').replace(' ', '').replace(':', '')
    traceback.print_exc(file=open('error_info'+'\\'+txt_name+'_发送邮件发生错误.txt','w'))

finally:
    os.remove(tipdir)
