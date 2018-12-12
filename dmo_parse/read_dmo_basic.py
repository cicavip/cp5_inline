import codecs

def read_dmo_basic(dmo_addr,basic_information):

    """
      读取DMO入口函数
      :param addr: DMO地址
             列表 basic_information: DMO的基础信息，零件钢号，车型，零件，测量开始时间，测量结束时间如：
                        ['82541277', 'T-Roc', 'FK', '2018/10/12', '09:12:22', '2018/10/12', '09:13:30']
             字典 point_value_information：点对应的测量测量值如：
                        {'NRFKA0004_O_AA.X': ' 1.277', 'NRFKA0004_O_AA.Y': ' -0.412'}
      """

    fil = codecs.open(dmo_addr, 'r')
    lines = [line.strip() for line in fil]
    fil.close()
    row_num = len(lines)

    i = 0
    while i < row_num:
        line = lines[i]
        line = line.replace("Dir1", "N")

        if len(line) > 2:  # 去除空行
            if "，" in line:
                line = line.replace("，", ",")

            if line[-1] == r'$':  # 合并不同行
                i += 1
                line_next = lines[i]
                line = line + line_next  # 去除末尾$

                j = 0
                while j < 10:  # 最多允许10个续行
                    if line_next[-1] == r'$':
                        i += 1
                        line_next = lines[i]
                        line = line + line_next
                    else:
                        break
                    j += 1

                line = line.replace("$", "")  # 去除续行符

        current_row = i

        dmo_basic_information(line, basic_information)

        i += 1
    return basic_information



def dmo_basic_information(line,basic_information):
    """
    获取DMO的基本信息：车型，零件，测量开始时间，测量结束时间，零件钢号，
    :return:
    """

    if line[:9] == 'PN(PART1)':
        basic_information.append(line.split("'")[1])# 获取零件钢号
    elif line[:7] == 'MD(SNR)':
        car=line.split("'")[1]

        if car is '':
            car='Bora_MQB'

        basic_information.append(car)# 获取车   型名称缩写
    elif line[:7] == 'DI(YD1)':
        basic_information.append(line.split("'")[1])  # 获取零件名称缩写
    elif line[:4] == 'DATE':
        basic_information.append(line.split(" = ")[-1])
    elif line[:4] == 'TIME':
        basic_information.append(line.split(" = ")[-1])
    else:
        pass
    # print(basic_information)



# dmo_addr=r'C:\Users\xiaobin.qiu\Desktop\1844210188_20181101013322.dmo'
# point_value = {}  # 点的偏差值字典，点名为键值为偏差
# basic_information = []  # 列表基本信息：车型，零件，零件钢号，测量开始时间，测量结束时间
# read_dmo_basic(dmo_addr,basic_information)
# print(point_value)
# print(basic_information)