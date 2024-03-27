from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns
from matplotlib import gridspec
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator, IndexLocator, FuncFormatter, AutoMinorLocator


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def plot(path, datelist,name,ax1,unit):
    col = ['comp1', 'comp2', 'cond_out_temp1', 'suction_temp1', 'discharge_temp1',
           'outdoor_temperature', 'high_pressure', 'low_pressure', 'eev1', 'ct1', 'ct2', 'double_tube_temp',
           'hot_gas_valve1', 'hot_gas_valve2', 'evi_bypass_valve', 'comp_current_frequency1', 'comp_current_frequency2',
           'evi_eev', 'fan_step', 'comp_ipm1']
    df_plot = pd.DataFrame(columns=['fault_type', name])
    for date in datelist:
        testlist = os.listdir(path + date)
        for test in testlist:
            dic = path + date + '/' + test
            for i in os.listdir(dic):
                if 'Outdoor' in i:
                    try:
                        df = pd.read_csv(dic + '/' + i, index_col=0).reset_index()
                    except:
                        df = pd.read_csv(dic + '/' + i, index_col=0)
                    label = i.split("_")[-2]
                    if label == '40Mesh':
                        label = 'Mesh40'
                    elif label == '200Mesh':
                        label = 'Mesh200'
                    elif label == 'Nofault':
                        label = 'Base'
                    df = df.drop(len(df)-1,axis=0)

                    data = pd.DataFrame(df[col])
                    if unit == 3065:
                        data['cond_in_ref'] = df['discharge_temp1']
                    else:
                        data['cond_in_ref'] = (df['discharge_temp1'] + df['discharge_temp2']) / 2
                    data['cond_out_ref'] = df['cond_out_temp1']
                    # data['cond_in_air'] = df.filter(regex='point').mean(axis=1)
                    data['cond_in_air'] = df.filter(regex='point').min(axis=1)
                    data['cond_out_air'] = df.filter(regex='condout').max(axis=1)
                    data['fan_step'] = df['fan_step']
                    data['outdoor_air_temperature'] = df['outdoor_temperature']
                    data['fault_type'] = label

                    data['Condenser effectiveness 1'] = abs(data['cond_in_ref'] - data['cond_out_ref']) / abs(data['cond_in_ref'] - data['cond_in_air'])
                    data['Condenser effectiveness 2'] = abs(data['cond_in_air'] - data['cond_out_air']) / abs(data['cond_in_ref'] - data['cond_in_air'])

                    data['Condenser effectiveness 1'] = data['Condenser effectiveness 1'].apply(lambda x: 1 if x > 1 else x)
                    data['Condenser effectiveness 2'] = data['Condenser effectiveness 2'].apply(lambda x: 1 if x > 1 else x)

                    create_folder('D:/{}/{}/{}'.format(unit, date, test))
                    data.to_csv(r'D:/{}/{}/{}/effectiveness.csv'.format(unit, date, test))

            df_plot = pd.concat([df_plot, data[['fault_type', 'fan_step', name]]], axis=0)
    df_plot = df_plot.sort_values(by=['fan_step'], ascending=[True])
    df_plot['fan_step'] = pd.cut(df_plot['fan_step'], np.arange(0, max(df_plot['fan_step']), step=5))

    print(df_plot)
    # mean = df_plot.groupby(['fault_type','fan_step'], as_index=False).mean()
    # oat = mean['fan_step'].values.tolist()
    # mean_dict = {}
    # for k in range(len(oat)):
    #     if mean['fan_step'][k] == oat[k]:
    #         mean_dict[oat[k]] = mean[(mean.fan_step == oat[k])]
    #
    # marker_list = ['o', 'D', '^', 's', 'p', '*']
    # a = 0
    # for key, value in mean_dict.items():
    #     try:
    #         ax1.plot(mean_dict[key]['fault_type'], value[name], marker=marker_list[a], markersize=10, linewidth=3,zorder=1, label='Average of ' + str(key))
    #         a += 1
    #     except:
    #         pass

    sns.stripplot(data=df_plot, x='fault_type', y=name, hue='fan_step', zorder=0, ax=ax1, split=True, size=7)

    minor_locator = AutoMinorLocator(2)
    ax1.xaxis.set_minor_locator(minor_locator)
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
    ax1.grid(linestyle=':', color='dimgray', which='minor')
    ax1.set(ylabel=None, xlabel=None)
    ax1.set(title=path[-5:-1])

    ax1.get_legend().remove()


path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/'

dataa = ['Condenser effectiveness 1','Condenser effectiveness 2']

for i in dataa:
    f1, axes = plt.subplots(2, 2, sharey=True,  figsize=(15, 10))
    plt.suptitle(i, x=0.15, y=1.03, fontsize=20)
    plot(path + '3065/', ['0810', '0811'], i, axes[0, 0],3065)
    plot(path + '3066/', ['0728', '0729', '0730', '0804', '0805', '0810', '0811'], i, axes[0,1],3066)
    plot(path + '3067/', ['0813'], i, axes[1, 0],3067)
    plot(path + '3069/', ['0809', '0812'], i, axes[1, 1],3069)
    handles, labels = axes[1,1].get_legend_handles_labels()
    lg = f1.legend(handles, labels, ncol=6, bbox_to_anchor=(0.99, 1.04))
    plt.tight_layout()
    # plt.show()
    f1.savefig('D:/' + '{}.png'.format(i), bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.clf()