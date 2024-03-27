import mpld3
from mpld3 import plugins
import pymysql
import pandas as pd
import datetime as dt
import ast
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import warnings


warnings.filterwarnings(action='ignore')

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return None

###############################################################################################################################################

def member_connect(host, port, database, username, password):
    conn = pymysql.connect(host=host, user=username, passwd=password, db=database, port=port, use_unicode=True,
                           charset='utf8')
    cursor = conn.cursor()
    user_query = "SELECT * FROM Member"
    cursor.execute(user_query)
    conn.commit()
    user_result = cursor.fetchall()

    un_list = []
    for data in user_result:
        username = data[2].decode('utf-8')
        un_list.append(username)

    return un_list

def member_list(path):
    member_data = pd.read_csv(path,encoding='utf-8')

    member_list = member_data['username'].tolist()

    return member_list

###############################################################################################################################################

def DIA_logs_server(column, user_list, host, username, password, database, port, day, overfitting, window, dia_column_count):
    conn = pymysql.connect(host=host, user=username, passwd=password, db=database, port=port, use_unicode=True,
                           charset='utf8')
    cursor = conn.cursor()
    for name in user_list:
        pd_logs_dia = pd.DataFrame(columns=column)

        dia_query = "SELECT * FROM logs_DIA WHERE log_identifer = '{}'".format(name)
        cursor.execute(dia_query)
        conn.commit()
        dia_result = cursor.fetchall()

        for i, data in enumerate(dia_result):
            date = dt.datetime.date(data[2])
            time = dt.datetime.time(data[2])

            if date == day:
                pd_logs_dia.loc[i, 'UserID'] = data[1]
                pd_logs_dia.loc[i, 'Date'] = date
                pd_logs_dia.loc[i, 'Time'] = time
                pd_logs_dia.loc[i, 'DataDetail'] = data[-1]

                pd_logs_dia.loc[i, 'UserID'] = pd_logs_dia.loc[i, 'UserID'].decode('utf-8')
                pd_logs_dia.loc[i, 'DataDetail'] = pd_logs_dia.loc[i, 'DataDetail'].decode('utf-8')

                pd_logs_dia = pd_logs_dia.reset_index(drop=True)

        concat_pd = pd.DataFrame(columns=['UserID', 'Date', 'Time', 'reason', 'get_amount', 'use_amount', 'remain'])

        for j in pd_logs_dia.index:
            str_data = pd_logs_dia.loc[j, 'DataDetail']
            str_data = str_data.replace('\n', '')
            str_data = str_data.replace('{', '{"')
            str_data = str_data.replace('}', '"}')
            str_data = str_data.replace(':', '" : "')
            str_data = str_data.replace('" ', '"')
            str_data = str_data.replace(',', '", "')

            dict_data = ast.literal_eval(str_data)
            dict_data.update({'UserID': str(pd_logs_dia.loc[j, 'UserID']), 'Date': str(pd_logs_dia.loc[j, 'Date']),
                              'Time': str(pd_logs_dia.loc[j, 'Time'])})
            concat_pd = pd.concat([concat_pd, pd.DataFrame([dict_data])], axis=0)

        concat_pd = concat_pd.reset_index(drop=True).fillna(0).astype({'get_amount': int, 'use_amount': int, 'remain': int, })

        if len(concat_pd) == 0 or len(concat_pd) == 1:
            continue

        rolling_pd = pd.DataFrame()
        rolling_pd['get_amount'] = concat_pd['get_amount'].rolling(window=window).mean()
        rolling_pd['use_amount'] = concat_pd['use_amount'].rolling(window=window).mean()
        rolling_pd['get_amount+'] = rolling_pd['get_amount'] * (1 + overfitting)
        rolling_pd['use_amount+'] = rolling_pd['use_amount'] * (1 + overfitting)
        rolling_pd['get_amount-'] = rolling_pd['get_amount'] * (1 - overfitting)
        rolling_pd['use_amount-'] = rolling_pd['use_amount'] * (1 - overfitting)

        rolling_pd = rolling_pd.fillna(method='bfill')

        for p in range(1, len(concat_pd)):
            if concat_pd.loc[p,'get_amount'] != 0:
                rolling_pd.loc[p, 'remain_vs_get'] = concat_pd.loc[p, 'remain'] - concat_pd.loc[p-1, 'remain']
            elif concat_pd.loc[p,'get_amount'] == 0:
                rolling_pd.loc[p, 'remain_vs_get'] = 0
        for p in range(1, len(concat_pd)):
            if concat_pd.loc[p, 'use_amount'] != 0:
                rolling_pd.loc[p, 'remain_vs_use'] = concat_pd.loc[p-1, 'remain'] - concat_pd.loc[p, 'remain']
            elif concat_pd.loc[p, 'use_amount'] == 0:
                rolling_pd.loc[p, 'remain_vs_use'] = 0

        concat_pd_save_path = './DIA_log/{}/RawData'.format(day)
        rolling_pd_save_path = './DIA_log/{}/RollingData'.format(day)

        create_path(concat_pd_save_path)
        create_path(rolling_pd_save_path)

        concat_pd.to_csv(concat_pd_save_path+'/{}.csv'.format(name),encoding='utf-8-sig')
        rolling_pd.to_csv(rolling_pd_save_path+'/{}.csv'.format(name),encoding='utf-8-sig')

        Dia_graph(concat_pd, rolling_pd, name, day, dia_column_count)

    return None

def TICKET_logs_server(column, user_list, host, username, password, database, port, day, overfitting, window, ticket_column_count):
    conn = pymysql.connect(host=host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
    cursor = conn.cursor()
    for name in user_list:
        pd_logs = pd.DataFrame(columns=column)

        ticket_query = "SELECT * FROM logs_TICKET WHERE log_identifer = '{}'".format(name)
        cursor.execute(ticket_query)
        conn.commit()
        dia_result = cursor.fetchall()

        for i, data in enumerate(dia_result):
            date = dt.datetime.date(data[2])
            time = dt.datetime.time(data[2])

            if date == day:
                pd_logs.loc[i, 'UserID'] = data[1]
                pd_logs.loc[i, 'Date'] = date
                pd_logs.loc[i, 'Time'] = time
                pd_logs.loc[i, 'DataDetail'] = data[-1]

                pd_logs.loc[i, 'UserID'] = pd_logs.loc[i, 'UserID'].decode('utf-8')
                pd_logs.loc[i, 'DataDetail'] = pd_logs.loc[i, 'DataDetail'].decode('utf-8')

                pd_logs = pd_logs.reset_index(drop=True)

        concat_pd = pd.DataFrame(columns=['UserID', 'Date', 'Time', 'reason', 'bossticket', 'moneyticket',
                                          'skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                                          'weaponticket', 'accessoryticket', 'clothticket', 'skillticket',
                                          'jangsuticket', 'supportticket', 'edutimeone', 'edutimetwo',
                                          'edutimefour', 'edutimefull', 'abilstone', 'weaponss', 'weaponsss',
                                          'jangsupiece', 'gotchapiece'])

        for j in pd_logs.index:
            str_data = pd_logs.loc[j, 'DataDetail']
            str_data = str_data.replace('\n', '')
            str_data = str_data.replace('{', '{"')
            str_data = str_data.replace('}', '"}')
            str_data = str_data.replace(':', '" : "')
            str_data = str_data.replace('" ', '"')
            str_data = str_data.replace(',', '", "')

            if 'DailyShop'in str_data or 'Member' in str_data or 'StatData' in str_data:
                continue

            dict_data = ast.literal_eval(str_data)

            dict_data.update({'UserID': str(pd_logs.loc[j, 'UserID']), 'Date': str(pd_logs.loc[j, 'Date']),
                              'Time': str(pd_logs.loc[j, 'Time'])})
            concat_pd = pd.concat([concat_pd, pd.DataFrame([dict_data])], axis=0)

        concat_pd = concat_pd.reset_index(drop=True).fillna(0)

        concat_pd['reason'] = concat_pd['reason'].astype(str)


        for i in range(len(concat_pd)):
            if 'use' in concat_pd.loc[i,'reason']:
                for col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                    concat_pd.loc[i, col] = -int(concat_pd.loc[i, col])
            else:
                for col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                    concat_pd.loc[i, col] = int(concat_pd.loc[i, col])

        for col in concat_pd.columns:
            if col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                concat_pd[col+' remain'] = concat_pd[col].cumsum()

        if len(concat_pd) == 0:
            continue
        concat_pd_save_path = './TICKET_log/{}/RawData'.format(day)

        create_path(concat_pd_save_path)

        concat_pd.to_csv(concat_pd_save_path+'/{}.csv'.format(name))

        Ticket_graph(concat_pd, name, day)

###############################################################################################################################################

def DIA_logs_csv(dia_csv_path, column, user_list, day, overfitting, window, dia_column_count):

    dia_result = pd.read_csv(dia_csv_path,encoding='utf-8')

    dia_result = dia_result[pd.to_datetime(dia_result['log_date']).dt.date == day].reset_index(drop=True)

    dia_result['date'] = pd.to_datetime(dia_result['log_date']).dt.date
    dia_result['time'] = pd.to_datetime(dia_result['log_date']).dt.time

    for name in user_list:
        pd_logs_dia = pd.DataFrame(columns=column)
        user_data = dia_result[dia_result['log_identifer'] == name].copy()

        pd_logs_dia["UserID"] = user_data['log_identifer']
        pd_logs_dia["Date"] = user_data['date']
        pd_logs_dia["Time"] = user_data['time']
        pd_logs_dia["DataDetail"] =  user_data['log_details']
        pd_logs_dia = pd_logs_dia.reset_index(drop=True)

        concat_pd = pd.DataFrame(columns=['UserID', 'Date', 'Time', 'reason', 'get_amount', 'use_amount', 'remain'])

        if len(pd_logs_dia) == 0 or len(pd_logs_dia) == 1:
            continue

        for j in pd_logs_dia.index:
            str_data = pd_logs_dia.loc[j, 'DataDetail']
            str_data = str_data.replace('\n', '')
            str_data = str_data.replace('{', '{"')
            str_data = str_data.replace('}', '"}')
            str_data = str_data.replace(':', '" : "')
            str_data = str_data.replace('" ', '"')
            str_data = str_data.replace(',', '", "')

            dict_data = ast.literal_eval(str_data)
            dict_data.update({'UserID': str(pd_logs_dia.loc[j, 'UserID']), 'Date': str(pd_logs_dia.loc[j, 'Date']),
                              'Time': str(pd_logs_dia.loc[j, 'Time'])})
            concat_pd = pd.concat([concat_pd, pd.DataFrame([dict_data])], axis=0)

        concat_pd = concat_pd.reset_index(drop=True).fillna(0).astype({'get_amount': int, 'use_amount': int, 'remain': int, })

        rolling_pd = pd.DataFrame()
        rolling_pd['get_amount'] = concat_pd['get_amount'].rolling(window=window).mean()
        rolling_pd['use_amount'] = concat_pd['use_amount'].rolling(window=window).mean()
        rolling_pd['get_amount+'] = rolling_pd['get_amount'] * (1 + overfitting)
        rolling_pd['use_amount+'] = rolling_pd['use_amount'] * (1 + overfitting)
        rolling_pd['get_amount-'] = rolling_pd['get_amount'] * (1 - overfitting)
        rolling_pd['use_amount-'] = rolling_pd['use_amount'] * (1 - overfitting)

        rolling_pd = rolling_pd.fillna(method='bfill')

        for p in range(1, len(concat_pd)):
            if concat_pd.loc[p,'get_amount'] != 0:
                rolling_pd.loc[p, 'remain_vs_get'] = concat_pd.loc[p, 'remain'] - concat_pd.loc[p-1, 'remain']
            elif concat_pd.loc[p,'get_amount'] == 0:
                rolling_pd.loc[p, 'remain_vs_get'] = 0
        for p in range(1, len(concat_pd)):
            if concat_pd.loc[p, 'use_amount'] != 0:
                rolling_pd.loc[p, 'remain_vs_use'] = concat_pd.loc[p-1, 'remain'] - concat_pd.loc[p, 'remain']
            elif concat_pd.loc[p, 'use_amount'] == 0:
                rolling_pd.loc[p, 'remain_vs_use'] = 0


        concat_pd_save_path = './DIA_log/{}/RawData'.format(day)
        rolling_pd_save_path = './DIA_log/{}/RollingData'.format(day)

        create_path(concat_pd_save_path)
        create_path(rolling_pd_save_path)

        concat_pd.to_csv(concat_pd_save_path+'/{}.csv'.format(name),encoding='utf-8-sig')
        rolling_pd.to_csv(rolling_pd_save_path+'/{}.csv'.format(name),encoding='utf-8-sig')

        Dia_graph(concat_pd, rolling_pd, name, day, dia_column_count)

    return None

def TICKET_logs_csv(ticket_csv_path, column, user_list, day):

    ticket_result = pd.read_csv(ticket_csv_path,encoding='utf-8')

    ticket_result = ticket_result[pd.to_datetime(ticket_result['log_date']).dt.date == day].reset_index(drop=True)

    ticket_result['date'] = pd.to_datetime(ticket_result['log_date']).dt.date
    ticket_result['time'] = pd.to_datetime(ticket_result['log_date']).dt.time

    for name in user_list:
        pd_logs_ticket = pd.DataFrame(columns=column)
        user_data = ticket_result[ticket_result['log_identifer'] == name].copy()

        pd_logs_ticket["UserID"] = user_data['log_identifer']
        pd_logs_ticket["Date"] = user_data['date']
        pd_logs_ticket["Time"] = user_data['time']
        pd_logs_ticket["DataDetail"] = user_data['log_details']
        pd_logs_ticket = pd_logs_ticket.reset_index(drop=True)

        concat_pd = pd.DataFrame(columns=['UserID', 'Date', 'Time', 'reason', 'bossticket', 'moneyticket',
                                          'skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                                          'weaponticket', 'accessoryticket', 'clothticket', 'skillticket',
                                          'jangsuticket', 'supportticket', 'edutimeone', 'edutimetwo',
                                          'edutimefour', 'edutimefull', 'abilstone', 'weaponss', 'weaponsss',
                                          'jangsupiece', 'gotchapiece'])

        for j in pd_logs_ticket.index:
            str_data = pd_logs_ticket.loc[j, 'DataDetail']
            str_data = str_data.replace('\n', '')
            str_data = str_data.replace('{', '{"')
            str_data = str_data.replace('}', '"}')
            str_data = str_data.replace(':', '" : "')
            str_data = str_data.replace('" ', '"')
            str_data = str_data.replace(',', '", "')

            if 'DailyShop'in str_data or 'Member' in str_data or 'StatData' in str_data:
                continue

            dict_data = ast.literal_eval(str_data)

            dict_data.update({'UserID': str(pd_logs_ticket.loc[j, 'UserID']), 'Date': str(pd_logs_ticket.loc[j, 'Date']),
                              'Time': str(pd_logs_ticket.loc[j, 'Time'])})
            concat_pd = pd.concat([concat_pd, pd.DataFrame([dict_data])], axis=0)

        concat_pd = concat_pd.reset_index(drop=True).fillna(0)

        concat_pd['reason'] = concat_pd['reason'].astype(str)

        for i in range(len(concat_pd)):
            if 'use' in concat_pd.loc[i,'reason']:
                for col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                    concat_pd.loc[i, col] = -int(concat_pd.loc[i, col])
            else:
                for col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                    concat_pd.loc[i, col] = int(concat_pd.loc[i, col])

        for col in concat_pd.columns:
            if col in ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                            'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket',
                            'supportticket', 'edutimeone', 'edutimetwo', 'edutimefour', 'edutimefull', 'abilstone',
                            'weaponss', 'weaponsss', 'jangsupiece', 'gotchapiece']:
                concat_pd[col+' remain'] = concat_pd[col].cumsum()

        if len(concat_pd) == 0:
            continue
        concat_pd_save_path = './TICKET_log/{}/RawData'.format(day)

        create_path(concat_pd_save_path)

        concat_pd.to_csv(concat_pd_save_path+'/{}.csv'.format(name))

        Ticket_graph(concat_pd, name, day)
        # Ticket_graph_test(concat_pd, name, day)

##############################################################################################################################################

def Dia_graph(concat_pd, rolling_pd, name, date,dia_column_count):
    f, axes = plt.subplots(dia_column_count, 1, figsize=(32, 8 * dia_column_count))

    # ODD POINT
    # '''
    mask_get = (concat_pd['get_amount'] > rolling_pd['get_amount+']) | (concat_pd['get_amount'] < rolling_pd['get_amount-'])
    mask_use = (concat_pd['use_amount'] > rolling_pd['use_amount+']) | (concat_pd['use_amount'] < rolling_pd['use_amount-'])

    mask_rvsg = (concat_pd['get_amount'] != rolling_pd['remain_vs_get']) & (concat_pd['get_amount'] != 0)
    mask_rvsu = (concat_pd['use_amount'] != rolling_pd['remain_vs_use']) & (concat_pd['use_amount'] != 0)

    mask_get[0], mask_use[0], mask_rvsu[0], mask_rvsg[0] = False, False, False, False

    x_len = [x for x in range(len(concat_pd))]
    for idx in range(len(concat_pd)):
        if mask_get[idx]:
            axes[0].scatter(x_len[idx], concat_pd['get_amount'][idx], marker='*', color='black', s=500)
            axes[0].text(x_len[idx], concat_pd['get_amount'][idx],
                         concat_pd['reason'][idx] + '\n' + concat_pd['Time'][idx],
                         fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        if mask_use[idx]:
            axes[1].scatter(x_len[idx], concat_pd['use_amount'][idx], marker='*', color='black', s=500)
            axes[1].text(x_len[idx], concat_pd['use_amount'][idx],
                         concat_pd['reason'][idx] + '\n' + concat_pd['Time'][idx],
                         fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        if mask_rvsg[idx] or mask_rvsu[idx]:
            axes[2].scatter(x_len[idx], concat_pd['remain'][idx], marker='*', color='black', s=500)
            axes[2].text(x_len[idx], concat_pd['remain'][idx],
                         concat_pd['reason'][idx] + '\n' + concat_pd['Time'][idx],
                         fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    # '''
    # 여기까지

    axes[0].bar(x_len, concat_pd['get_amount'], linewidth=4, color='red', label='GET AMOUNT')
    axes[1].bar(x_len, concat_pd['use_amount'], linewidth=4, color='red', label='USE AMOUNT')
    axes[2].plot(concat_pd['remain'], linewidth=4, color='red', label='REMAIN')
    axes[2].plot(rolling_pd['remain_vs_get'], linewidth=4, color='m', label='REMAIN vs GET AMOUNT')
    axes[2].plot(rolling_pd['remain_vs_use'], linewidth=4, color='c', label='REMAIN vs USE AMOUNT')


    # average 그리는 그래프
    # '''
    axes[0].plot(rolling_pd['get_amount+'], linewidth=4, color='green', linestyle='--', label='2Avg + 50%')
    axes[1].plot(rolling_pd['use_amount+'], linewidth=4, color='green', linestyle='--', label='2Avg + 50%')

    axes[0].plot(rolling_pd['get_amount-'], linewidth=4, color='blue', linestyle='--', label='2Avg - 50%')
    axes[1].plot(rolling_pd['use_amount-'], linewidth=4, color='blue', linestyle='--', label='2Avg - 50%')
    # '''
    # 여기까지

    axes[0].set_title('Get amount', fontsize=40)
    axes[1].set_title('Use amount', fontsize=40)
    axes[2].set_title('Remain', fontsize=40)

    try:
        axes[0].set_ylim(0, max(concat_pd['get_amount']) + 10000)
        axes[1].set_ylim(0, max(concat_pd['use_amount']) + 10000)
    except:
        pass

    def y_fmt(x, _):
        return '{:,.0f}'.format(x)

    for axe in range(len(axes)):
        axes[axe].tick_params(axis='both', labelsize=20)
        axes[axe].yaxis.set_major_formatter(FuncFormatter(y_fmt))
        axes[axe].grid(axis='both', color='gray')
        axes[axe].legend(loc='upper right', fontsize = 20)

    if len(concat_pd) // 9 < 1:
        xlabel_count = len(concat_pd)
    else:
        xlabel_count = len(concat_pd) // 9

    axes[0].set_xticklabels(concat_pd['Time'][::xlabel_count])
    axes[1].set_xticklabels(concat_pd['Time'][::xlabel_count])
    axes[2].set_xticklabels(concat_pd['Time'][::xlabel_count])
    axes[0].set_xticks([a for a in range(len(concat_pd['Time'])) if a % xlabel_count == 0])
    axes[1].set_xticks([a for a in range(len(concat_pd['Time'])) if a % xlabel_count == 0])
    axes[2].set_xticks([a for a in range(len(concat_pd['Time'])) if a % xlabel_count == 0])

    plt.tight_layout()

    graph_save_path = './Dia_log//{}/graph'.format(date)
    create_path(graph_save_path)
    if True in mask_rvsg.to_list() or True in mask_rvsu.to_list():
        plt.savefig(graph_save_path + '/{}_검출.jpg'.format(name))
    else:
        plt.savefig(graph_save_path + '/{}.jpg'.format(name))

    return

def Ticket_graph(concat_pd, name, date):
    colors = ['b','r','g','m','y','c','chocolate','darkorange','tan','lightcyan','slategray','navy','blueviolet',
              'pink','gold','olive','khaki','lime','azure','powderblue','mintcream','beige','olivedrab','lawngreen',
              'paleturquoise']
    ticket_column = ['bossticket', 'moneyticket','skillbookticket', 'awakenticket', 'pvpticket', 'gongbangticket',
                     'weaponticket', 'accessoryticket', 'clothticket', 'skillticket', 'jangsuticket', 'supportticket',
                     'edutimeone', 'edutimetwo','edutimefour', 'edutimefull', 'abilstone', 'weaponss', 'weaponsss',
                     'jangsupiece', 'gotchapiece']

    fig, ax = plt.subplots(figsize=(19.20, 10.80))

    for i, column in enumerate(ticket_column):
        lines, = ax.plot(concat_pd['Time'].astype(str),concat_pd[column+' remain'].astype(int),'-o', linewidth=4, label=column, color=colors[i], markersize=10)
        labels = [
            '<div style="border: 1px solid black; background-color: white; padding: 5px; border-radius: 5px;">Label: {}<br>Reason: {}<br>Amount: {}<br>Time: {}</div>'.format(
                column, 'None' if row[column] == 0 else row['reason'], abs(row[column]), row['Time']) for
            _, row in concat_pd.iterrows()]
        tooltip = plugins.PointHTMLTooltip(points=lines,labels=labels, voffset=-100, hoffset=-50)
        plugins.connect(fig, tooltip)

    ax.tick_params(axis='both', labelsize=20)
    ax.grid(axis='both', color='gray')
    fig.subplots_adjust(right=0.8, left=0.1, bottom=0.1, top=0.9)

    handles, labels = ax.get_legend_handles_labels()
    interactive_legend = plugins.InteractiveLegendPlugin(handles, labels, font_size=35)
    plugins.connect(fig, interactive_legend)

    # def on_legend_click(event):
    #     for i in range(len(lines)):
    #         if event.artist.get_label() == lines[i].get_label():
    #             lines[i].set_visible(not lines[i].get_visible())

    def on_legend_click(event):
        for i in range(len(lines)):
            if event.artist.get_label() == lines[i].get_label():
                lines[i].set_visible(not lines[i].get_visible())

    interactive_legend.on_legend_click = on_legend_click

    interval = len(concat_pd) // 9
    if interval > 0 :
        xtick_loc = [(interval * i) - 1 for i in range(1, 10)]
        xtick_labels = [concat_pd.Time[loc] for loc in xtick_loc]
    else:
        xtick_loc = range(len(concat_pd))
        xtick_labels = concat_pd.Time
    plt.xticks(xtick_loc, xtick_labels, fontsize=16)

    ax.set_xticks(xtick_loc)
    ax.set_xticklabels(xtick_labels, fontsize=16)

    graph_save_path = './TICKET_log//{}/graph'.format(date)
    create_path(graph_save_path)
    return mpld3.save_html(fig, graph_save_path + '/{}.html'.format(name))


############### HOST INFORMATION ###############
host = "uws64-158.cafe24.com"
port = 3306
database = "kgd3416"
username = "kgd3416"
password = "rudehd3416"

############### CSV FILE DIRECTION ###############
member_csv_path = './Member.csv'
dia_csv_path = './logs_DIA.csv'
ticket_csv_path = './logs_TICKET.csv'

############### USER LIST DEFINITION ############### (게임 서버에 있는 모든 유저를 불러오는 함수)
# un_list = member_connect(host, port, database, username, password)
un_list = member_list(member_csv_path)

############### COLUMN INFORMATION ###############
DiaColumn = ['UserID', 'Date', 'Time', 'DataDetail']
TicketColumn = ['UserID', 'Date', 'Time', 'DataDetail']
JangsuColumn = ['UserID', 'Date', 'Time', 'DataDetail']
WeaponColumn = ['UserID', 'Date', 'Time', 'DataDetail']
LogAllColumn = ['UserID', 'Date', 'Time', 'DataDetail']

############### ANALYSIS PARAMETER ############### (싸좡님 개인 취향에 맞게 분석하세융 ~)
overfitting = 0.5
window = 2

############### GRAPH PARAMETER ############### (로그 DataDetail에 들어가는 데이터 개수)
dia_column_count = 3

############### DATE TIME ############### (python datetime 형식으로 넣어야 함)
today = dt.datetime.today().date()

############### DEFINITION (SERVER CONNECTING) ###############
# DIA_logs_server(DiaColumn, un_list, host, username, password, database, port, today, overfitting, window, dia_column_count) #logs_DIA 데이터
# TICKET_logs_server(DiaColumn, un_list, host, username, password, database, port, today, overfitting, window, ticket_column_count) #logs_TICKET 데이터

############### DEFINITION (READ CSV) ###############
DIA_logs_csv(dia_csv_path, DiaColumn, un_list, today, overfitting, window, dia_column_count) #logs_DIA 데이터
TICKET_logs_csv(ticket_csv_path, TicketColumn, un_list, today) #logs_TICKET 데이터
