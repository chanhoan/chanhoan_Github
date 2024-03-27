import pandas as pd
import os

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)

indoor_3065 = [3071,3072,3074,3081,3084,3091,3092,3094,3095,3099,3100,3105,3106,3109,3112,3123,3124,3125,3131,3133]
indoor_3066 = [3085,3086,3107,3108,3121,3128]
indoor_3067 = [3075,3079,3080,3088,3094,3101,3111,3114,3115,3119,3120,3122,3130]
indoor_3069 = [3077,3082,3083,3089,3090,3096,3102,3104,3110,3116,3117,3129,3134]

month = '08'
date = '10'
unit = '3065'
experiment_count = 2
layer = ['Nofault']
start_time = ['2021-{}-{} 12:47:00'.format(month,date), '2021-{}-{} 16:21:00'.format(month,date), '2021-{}-{} 14:38:00'.format(month,date)]
finish_time = ['2021-{}-{} 14:01:00'.format(month,date),'2021-{}-{} 17:33:00'.format(month,date), '2021-{}-{} 16:05:00'.format(month,date)]
directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Compressor map data\2021-11-23\{}\{}-{}'.format(unit,month,date)

indoor_list = []
if unit == '3065':
    indoor_list = indoor_3065
elif unit == '3066':
    indoor_list = indoor_3066
elif unit == '3067':
    indoor_list = indoor_3067
elif unit == '3069':
    indoor_list = indoor_3069

for i in range(len(indoor_list)):
    indoor = pd.read_csv(directory+'\{}{}_indoor_{}.csv'.format(month,date,indoor_list[i])).set_index('updated_time').drop('Unnamed: 0',axis=1)
    # print(indoor.index)

    iot_start = 0
    iot_finish = 0

    for j in range(experiment_count):
        for k in range(len(indoor)):
            if start_time[j] == str(indoor.index[k]):
                iot_start = k
            elif finish_time[j] == str(indoor.index[k]):
                iot_finish = k
        indoor_ = indoor.iloc[iot_start:iot_finish, :]
        print(j)
        save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Dataset2\{}\{}{}\experiment {}'.format(unit, month, date, j+1, )
        create_folder(save)
        indoor_.to_csv(save+'\{}{}_indoor_{}_{}.csv'.format(month, date, indoor_list[i], j+1))
