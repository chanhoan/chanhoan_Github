import pymysql
import pandas as pd
import datetime
import os

today = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
folder_name = today[0:10]

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

create_folder(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\{}'.format(folder_name))

# indoor_data = "indoor_power, evain_temp, evaout_temp, indoor_set_temp, current_room_temp, eev, indoor_fan_speed, relative_capa_code"
indoor_data = "indoor_power, indoor_set_temp, current_room_temp, eev, relative_capa_code"
outdoor_data = "total_indoor_capa, comp1, comp2, cond_out_temp1, cond_out_temp2, suction_temp1, suction_temp2, " \
               "discharge_temp1, discharge_temp2, discharge_temp3, outdoor_temperature, high_pressure, low_pressure, eev, ct, meter"

meter_id = [1040, 1046, 1551, 1041, 1045, 1552, 1553, 1549, 1042, 1047, 1043, 1550, 1548, 1044]
outdoor_id = [908, 907, 909, 910, 921, 920, 919, 917, 918, 911, 915, 913, 914, 916]
indoor_id = [922, 924, 925, 926, 928, 929, 930, 931, 933, 934, 935, 936, 937, 938, 939, 940,
             941, 942, 943, 944, 947, 948, 950, 951, 953, 954, 955, 956, 957, 958, 959, 960,
             961, 962, 963, 964, 966, 967, 968, 970, 971, 972, 974, 975, 976, 977, 978, 979, 980,
             981, 983, 984, 985, 986, 988, 990, 991, 992, 993, 994, 996, 997, 998, 999, 1000,
             1002, 1004, 1005, 1006, 1007, 1008, 1009, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1019, 1020,
             1021, 1022, 1023, 1024, 1025]

nong = [636,620,615,651,640,596,610,602,564,611,595,573]

db_conn = pymysql.connect(host="192.168.0.33", user='bsmart', password='bsmartlab419', database='biot', autocommit=True)
cursor = db_conn.cursor()

def get_indoor(month1,date1,month,date, unit):
    for i in dido[unit]:
        sql1 = "SELECT * FROM indoor_{} WHERE updated_time >= '2022-{}-{} {}:00:00' and updated_time <= '2022-{}-{} {}:59:00' AND time(updated_time) BETWEEN '00:00:00' AND '23:59:00'".format(i,month1,date1,'00',month,date,23)
        # cursor.execute(sql1)
        # rows = cursor.fetchall()
        # print(rows)
        df1 = pd.read_sql(sql1, db_conn)
        save = r"C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\{}\{}\{}{}".format(folder_name,unit,month,date)
        create_folder(save)
        df1.to_csv(save+'\{}{}_indoor_{}.csv'.format(month,date, i))
    # len(df1)
    db_conn.close()

def get_outdoor(dev, start, end, occ):
    if occ == True:
        hour1 = '00'
        hour2 = '23'
    elif occ == False:
        hour1 = '00'
        hour2 = '23'

    if start== end:
        period=start
    elif start != end:
        period=start+end


    for i in dev:
        sql = "SELECT * FROM outdoor_{} WHERE updated_time >= '2022-{}-{} {}:00:00' and updated_time <= '2022-{}-{} {}:59:00' AND time(updated_time) BETWEEN '00:00:00' AND '23:59:00'".format(
            i, start[:2], start[2:], hour1, end[:2], end[2:], hour2)
        df = pd.read_sql(sql, db_conn)
        df.to_csv(r"C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\{}\outdoor_{}.csv".format(folder_name, i))
        # df.to_csv("C:/Users/user/OneDrive - Chonnam National University/2020_Samsung/InitialTest/2020.10.06/database/mysql_outdoor_{}.csv".format(i))
    db_conn.close()


dido_out = [3065,3066,3067,3069]

dido = {
    3065:[3109, 3100, 3095, 3112, 3133, 3074, 3092, 3105, 3091, 3124, 3071, 3072, 3123, 3125, 3106, 3099, 3081, 3131, 3094, 3084],
    3069:[3077, 3082, 3083, 3089, 3096, 3104, 3110, 3117, 3134, 3102, 3116, 3129, 3090],
    3066:[3085, 3086, 3107, 3128, 3108, 3121],
    3067:[3075, 3079, 3080, 3088, 3094, 3101, 3111, 3114, 3115, 3119, 3120, 3122, 3130]}


today = datetime.datetime.now()
start_month = '02'
start_date = '14'
end_month = '02'
end_date = '14'
indoor_start_month = '02'
indoor_start_date = '14'
indoor_month = '02'
indoor_date = '14'

# get_indoor(indoor_start_month,indoor_start_date,indoor_month,indoor_date, 3065)
# get_indoor(indoor_start_month,indoor_start_date,indoor_month,indoor_date, 3066)
# get_indoor(indoor_start_month,indoor_start_date,indoor_month,indoor_date, 3067)
# get_indoor(indoor_start_month,indoor_start_date,indoor_month,indoor_date, 3069)
#
get_outdoor(dido_out, start_month+start_date, end_month+end_date, False)