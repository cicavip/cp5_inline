
from mysql.create_table import cre_db_table

def creat_basic_db(host,user,pw,database,map_database):

    base_table_byte = '(Point_Group INT, ' \
                      'PointName CHAR(50) NOT NULL primary key,' \
                      'X_Position FLOAT, ' \
                      'Y_Position FLOAT, ' \
                      'Z_Position FLOAT, ' \
                      'i_Richtung FLOAT, ' \
                      'j_Richtung FLOAT, ' \
                      'k_Richtung FLOAT, ' \
                      'UntererTol FLOAT, ' \
                      'ObererTol FLOAT, ' \
                      'UntererTol_I FLOAT, ' \
                      'ObererTol_I FLOAT, ' \
                      'UntererTol_II FLOAT, ' \
                      'ObererTol_II FLOAT, ' \
                      'UntererTol_III FLOAT, ' \
                      'ObererTol_III FLOAT, ' \
                      'Characteristic  CHAR(50),' \
                      'Description  CHAR(50),' \
                      'Point_Grade  CHAR(50),' \
                      'Consistency  CHAR(50),' \
                      'FM_POINT  CHAR(50),' \
                      'CS_Statistics  CHAR(50)' \
                      ')'

    # 创建基础数据库
    cre_db_table(host, user, pw, database, map_database, base_table_byte)
