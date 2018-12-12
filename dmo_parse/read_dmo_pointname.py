# -*- coding:utf-8 -*-


import codecs
import win32api
import win32con

def read_dmo_value(dmo_addr,point_value):

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

        point_information(line, current_row, lines, point_value)

        i += 1
    return point_value

def point_information (line, current_row, lines,point_value_information):
    """
       获取测量点的偏差值字典
    """
    if line[:3] == 'TA(' \
            and '_abs' not in line \
            and 'Aignment' not in line \
            and 'Aig' not in line \
            and 'Alignment' not in line:  # 点信息

        point_name = get_point_name(line, current_row, lines)
        point_direction = get_point_direction_general(line)
        point_value = get_point_error(line, point_name, point_direction)
        full_point_name = point_name + "." + point_direction
        point_value_information[full_point_name] = point_value
        # print(point_value_information)

def get_point_name(line, current_row, lines):
    """
    获取点名
    """
    ta_point_name = line.split("(")[1].split(")")[0]
    # fa_point_name = ""

    for i in range(current_row, 0, -1):
        row_up = lines[i]
        key_1 = "FA("
        # key_2 = "FA("
        if row_up[:3] == key_1:
            fa_point_name = row_up.split("(")[1].split(")")[0]
            point_name = fa_point_name

            break
    return point_name


def get_point_direction_general(line):
    """
    获取评价方向
    :param line:
    :return:
    """
    if "XAXIS" in line:
        direction = "X"
    elif "YAXIS" in line:
        direction = "Y"
    elif "ZAXIS" in line:
        direction = "Z"
    elif "PROFP" in line:
        direction = "N"
    elif "PROFS" in line:
        direction = "N"
    elif "NAXIS" in line:
        direction = "N"
    elif "WIDTH" in line and "LONG" in line:
        direction = "L"
    elif "WIDTH" in line and "SHORT" in line:
        direction = "B"
    elif "DIAM" in line:
        direction = "D"
    elif "TOL/POS" in line:  # 位置度偏差
        direction = "P"
    else:
        win32api.MessageBox(0, "存在未识别的类型,该语句为：\n" + line, "错误", win32con.MB_OK)  # 弹窗报错
    return direction

def get_point_error (line,point_name,direction):
    point_name_direction = point_name + direction
    ta_point_name = line.split("(")[1].split(")")[0]
    if point_name_direction == ta_point_name :
        point_error = line.split(",")[-2]

    else:
        win32api.MessageBox(0, "该点未找到偏差：\n" + point_name, "错误", win32con.MB_OK)  # 弹窗报错

    return point_error

#
# dmo_addr=r'D:\Python\Python_Project\cp4_2_inline\basic_dmo\RO1\C4201840453828_20181016065410.dmo'
# point_value = {}  # 点的偏差值字典，点名为键值为偏差
# basic_information = []  # 列表基本信息：车型，零件，零件钢号，测量开始时间，测量结束时间
# read_dmo_value(dmo_addr,point_value)
# print(point_value)
# print(basic_information)
# point_names=[]
# for point_name in point_value.keys():
#     point_names.append(point_name)
#
# print(point_names)