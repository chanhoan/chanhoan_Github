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


def plot(path, datelist, name, ax1):
    col = ['comp1', 'comp2', 'cond_out_temp1', 'suction_temp1', 'discharge_temp1',
           'outdoor_temperature', 'high_pressure', 'low_pressure', 'eev1', 'ct1', 'ct2', 'double_tube_temp',
           'hot_gas_valve1', 'hot_gas_valve2', 'evi_bypass_valve', 'comp_current_frequency1', 'comp_current_frequency2',
           'evi_eev', 'fan_step', 'comp_ipm1']
    df_plot = pd.DataFrame(columns=['fault_type', name])
    for date in datelist:
        testlist = os.listdir(path + date)
        for test in testlist:
            dic = path + date + '/' + test
            print(dic)
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
                    data = pd.DataFrame(df[col])
                    data['comp_freq_sum'] = df.filter(regex='current_frequency').sum(axis=1)
                    data['cond_in_air_temp'] = df.filter(regex='point').mean(axis=1)
                    data['cond_out_air_temp'] = df.filter(regex='condout').mean(axis=1)
                    data['cond_in_air_velocity'] = df['Standard Velocity (Matrix)'].apply(lambda x: -x if x < 0 else x)
                    data['cond_in_air_velocity'] = data['cond_in_air_velocity'].apply(lambda x: None if x > 10 else x)
                    data['cond_out_air_volume'] = df['Standard Velocity (Matrix)'].apply(lambda x: x if x > 10 else None)
                    data['cond_in_air_velocity'].fillna(method='ffill', inplace=True)
                    data = data.reset_index(drop=True)
                    data['fault_type'] = label
                    # data[name] = data[name].apply(lambda x: None if x < 0 else x)

                elif 'indoor' in i:
                    df = pd.read_csv(dic + '/' + i)

            df_plot = pd.concat([df_plot, data[['fault_type', 'comp_freq_sum', name]]], axis=0)
    df_plot = df_plot.sort_values(by=['fault_type'], ascending=[True])
    df_plot['freq'] = pd.cut(df_plot['comp_freq_sum'], np.arange(0, max(df_plot['comp_freq_sum']), step=20))
    print(df_plot['freq'])
    mean = df_plot.groupby(['fault_type','freq'], as_index=False).mean()
    freq = mean['freq'].values.tolist()

    mean_dict = {}
    for k in range(len(freq)):
        if mean['freq'][k] == freq[k]:
            mean_dict[freq[k]] = mean[(mean.freq == freq[k])]
    # print(mean_dict)

    marker_list = ['o','D','^','s','p','*']
    a = 0
    for key, value in mean_dict.items():
        try:
            ax1.plot(mean_dict[key]['fault_type'], value[name], marker=marker_list[a], markersize=10,linewidth=3, zorder=1, label='Average of '+str(key))
            a += 1
        except:
            pass

    sns.stripplot(data=df_plot, x='fault_type', y=name, hue='freq', zorder=0, ax=ax1, split=True, size=7)

    minor_locator = AutoMinorLocator(2)
    ax1.xaxis.set_minor_locator(minor_locator)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=5))
    if name == 'cond_in_air_velocity':
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=0.2))
    elif name == 'cond_out_air_volume':
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=500))
    elif name == 'cond_out_air_temp':
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=2))
    ax1.grid(linestyle=':', color='dimgray', which='minor')
    ax1.set(ylabel=None, xlabel=None)
    ax1.set(title=path[-5:-1])

    # handles, labels = ax1.get_legend_handles_labels()
    ax1.get_legend().remove()


path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'
path_ = 'D:/연구실/1. Samsung/2021/열교환기고장진단/FDD/CondOutPred/Aug/3066/'

dataa = ['cond_in_air_temp','cond_out_air_temp','cond_in_air_velocity','cond_out_air_volume']
# cond_out_air_temp

for i in dataa:
    f1, axes = plt.subplots(2, 2, sharey=True,  figsize=(15, 10))
    plt.suptitle(i, x=0.15, y=1.03, fontsize=20)
    plot(path+'3065/', ['0810','0811'], i, axes[0,0])
    plot(path+'3066/', ['0728','0729','0730','0804','0805', '0810', '0811'], i, axes[0,1])
    plot(path+'3067/', ['0813'], i, axes[1,0])
    plot(path+'3069/', ['0809','0812'], i, axes[1,1])
    handles, labels = axes[1,1].get_legend_handles_labels()
    lg = f1.legend(handles,labels,ncol=6,bbox_to_anchor=(0.99,1.04))
    plt.tight_layout()
    # plt.show()
    f1.savefig('D:/'+'{}.png'.format(i),bbox_extra_artists=(lg,),bbox_inches='tight')
    plt.clf()