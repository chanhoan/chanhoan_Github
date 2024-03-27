from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns
from matplotlib import gridspec
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator, IndexLocator, FuncFormatter, AutoMinorLocator

font_path = 'C:/windows/fonts/arial.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'
path_ = 'D:/연구실/1. Samsung/2021/열교환기고장진단/FDD/CondOutPred/Aug/3066/'

dataa = ['cond_in_air_temp','cond_out_air_temp','cond_in_air_velocity','cond_out_air_volume']
# cond_out_air_temp


def plot(path, datelist,unit):
    for date in datelist:
        testlist = os.listdir(path + date)
        data_ = pd.DataFrame()
        for test in testlist:
            dic = path + date + '/' + test
            print(dic)
            data = pd.DataFrame()
            for i in os.listdir(dic):
                if 'Outdoor' in i:
                    df = pd.read_csv(dic + '/' + i, index_col=0)
                    label = i.split("_")[-2]
                    if label == '40Mesh':
                        label = 'Mesh40'
                    elif label == '200Mesh':
                        label = 'Mesh200'
                    elif label == 'Nofault':
                        label = 'Base'
                    df['updated_time'] = df.index
                    data['cond_in_air_velocity'] = df['Standard Velocity (Matrix)'].apply(lambda x: -x if x < 0 else x)
                    data['cond_in_air_velocity'] = data['cond_in_air_velocity'].apply(lambda x: None if x > 10 else x)
                    # data['cond_out_air_volume'] = df['Standard Velocity (Matrix)'].apply(lambda x: x if x > 10 else None)
                    data['fan_step'] = df['fan_step'].apply(lambda x: None if x == 0 else x)
                    data = data.reset_index(drop=True)
                    data['fault_type'] = label
                    if unit == '3065':
                        data['velocity_rated'] = 0.033 * data['fan_step']
                    elif unit == '3066':
                        data['velocity_rated'] = 0.0346 * data['fan_step']
                    elif unit == '3067':
                        data['velocity_rated'] = 0.0442 * data['fan_step']
                    data['fault_level'] = abs(data['velocity_rated']-data['cond_in_air_velocity']) / data['velocity_rated']
                    data['fault_level'] = data['fault_level'].apply(lambda x: None if x < 0 else x)
            data_ = pd.concat([data_,data],axis=0)
        data_ = data_.dropna(axis=0)
        data_.to_csv(path+'fault_level/{}/cond_in_air_velocity_{}_fault_level.csv'.format(date,date))


for i in dataa:
    plt.suptitle(i, x=0.15, y=1.03, fontsize=20)
    plot(path+'3065/', ['0810','0811'],'3065')
    plot(path+'3066/', ['0728','0729','0730','0804','0805', '0810', '0811'],'3066')
    plot(path+'3067/', ['0813','0813_normal'],'3067')