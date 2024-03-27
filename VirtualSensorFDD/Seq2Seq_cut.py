import pandas as pd
import os
import datetime

file = {'3065/': ['0810','0811'],
        '3066/': ['0728','0729','0730','0804','0805', '0810', '0811'],
        '3067/': ['0813']}

for key, datelist in file.items():
    unit = key[:-1]
    for day in datelist:
        month = day[:2]
        date = day[2:]
        experiment_count = 3
        layer = ['Nofault']
        # start_time = ['2021-{}-{} 10:39:00'.format(month,date), '2021-{}-{} 12:50:00'.format(month,date), '2021-{}-{} 14:38:00'.format(month,date)]
        # finish_time = ['2021-{}-{} 12:29:00'.format(month,date),'2021-{}-{} 14:16:00'.format(month,date), '2021-{}-{} 16:05:00'.format(month,date)]
        directory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Performance degradation\Seq2Seq\{}\ODU{}_Test_2021_{}_{}.csv'.format(unit,unit,month,date)

        data = pd.read_csv(directory)

        date_range = pd.date_range('2021-{}-{} 00:00:00'.format(month,date),'2021-{}-{} 23:55:00'.format(month,date),freq=datetime.timedelta(minutes=5))

        data.index = date_range

        dic = r'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Performance degradation/EPM/{}/{}{}/'.format(unit,month,date)

        for test in os.listdir(dic):
            cut_to_data = pd.read_csv(dic+test + '/EPM.csv').set_index('Unnamed: 0')
            # print(cut_to_data)
            start = cut_to_data.index[0]
            end = cut_to_data.index[-1]
            start_index = 0
            end_index = 0
            for j in range(len(data)):
                if str(data.index[j]) == str(start):
                    start_index = j
                elif str(data.index[j]) == str(end):
                    end_index = j

            Seq2Seq = data.loc[start:end,]
            Seq2Seq.to_csv(dic+test+'/Seq2Seq.csv')