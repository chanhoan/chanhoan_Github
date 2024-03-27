import pandas as pd
import datetime as dt
import ast

def member_list(path):
    member_data = pd.read_csv(path,encoding='utf-8')

    member_list = member_data['username'].tolist()

    return member_list


def data_preprocessing_current(data):
    overall_dict = {}
    for jangsu in jangsuD + jangsuC + jangsuB + jangsuA + jangsuS:
        data.loc[0, jangsu] = list(filter(None, data.loc[0, jangsu].split(';')))
        data.loc[0, jangsu] = [data.loc[0, jangsu][i].split(',') for i in range(len(data.loc[0, jangsu]))]
        for s in range(len(data.loc[0, jangsu])):
            data.loc[0, jangsu][s][0] = jangsu_stat_index[data.loc[0, jangsu][s][0]]
            data.loc[0, jangsu][s][1] = round(float(data.loc[0, jangsu][s][1]) * 100)
            data.loc[0, jangsu][s][2] = round(float(data.loc[0, jangsu][s][2]) * 100)
        dict = {}
        for i in range(len(data.loc[0,jangsu])):
            value = {}
            if data.loc[0,jangsu][i][2] == 0 and data.loc[0,jangsu][i][1] != 0:
                value = {'능력치': data.loc[0,jangsu][i][0], '수치': '+' + str(data.loc[0,jangsu][i][1]) + '%'}
            elif data.loc[0,jangsu][i][1] == 0 and data.loc[0,jangsu][i][2] != 0:
                value = {'능력치': data.loc[0, jangsu][i][0], '수치': 'x' + str(data.loc[0,jangsu][i][2]) + '%'}
            elif data.loc[0,jangsu][i][1] == 0 and data.loc[0,jangsu][i][2] == 0:
                value = {'능력치': ' ', '수치': ' '}
            dict['능력치 {}'.format(i+1)] = value
        overall_dict[jangsu] = dict
    return overall_dict

def data_preprocessing_log(data):
    overall_dict = {}
    for jangsu in jangsuD + jangsuC + jangsuB + jangsuA + jangsuS:
        data_ = data[data['Jangsu'] == jangsu].reset_index(drop=True)
        for i in range(len(data_)):
            if jangsu in jangsuD:
                index = [j for j, x in enumerate(jangsuD) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsuC:
                index = [j for j, x in enumerate(jangsuC) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsuB:
                index = [j for j, x in enumerate(jangsuB) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsuA:
                index = [j for j, x in enumerate(jangsuA) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsuS:
                index = [j for j, x in enumerate(jangsuS) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            data_.loc[i, 'Special'] = [data_.loc[i, 'Special'][j].split(',') for j in range(len(data_.loc[i, 'Special']))]
            for s in range(len(data_.loc[i, 'Special'])):
                data_.loc[i, 'Special'][s][0] = jangsu_stat_index[data_.loc[i, 'Special'][s][0]]
                data_.loc[i, 'Special'][s][1] = round(float(data_.loc[i, 'Special'][s][1]) * 100)
                data_.loc[i, 'Special'][s][2] = round(float(data_.loc[i, 'Special'][s][2]) * 100)
        value = []
        dict = {}
        try:
            for k in range(len(data_.loc[0, 'Special'])):
                for i in range(len(data_)):
                    if data_.loc[i, 'Special'][k][2] == 0 and data_.loc[i, 'Special'][k][1] != 0:
                        value.append({'Date':data_.loc[i, 'Date'],'Time':data_.loc[i, 'Time'],'능력치': data_.loc[i, 'Special'][k][0], '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                    elif data_.loc[i, 'Special'][k][1] == 0 and data_.loc[i, 'Special'][k][2] != 0:
                        value.append({'Date':data_.loc[i, 'Date'],'Time':data_.loc[i, 'Time'],'능력치': data_.loc[i, 'Special'][k][0], '수치': 'x' + str(data_.loc[i, 'Special'][k][2]) + '%'})
                    dict['능력치 {}'.format(k + 1)] = value
                overall_dict[jangsu] = dict
        except:
            for k in range(1):
                for i in range(len(data_)):
                    if data_.loc[i, 'Special'][k][2] == 0 and data_.loc[i, 'Special'][k][1] != 0:
                        value.append({'Date':data_.loc[i, 'Date'],'Time':data_.loc[i, 'Time'],'능력치': data_.loc[i, 'Special'][k][0], '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                    elif data_.loc[i, 'Special'][k][1] == 0 and data_.loc[i, 'Special'][k][2] != 0:
                        value.append({'Date':data_.loc[i, 'Date'],'Time':data_.loc[i, 'Time'],'능력치': data_.loc[i, 'Special'][k][0], '수치': 'x' + str(data_.loc[i, 'Special'][k][2]) + '%'})
                    dict['능력치 {}'.format(k + 1)] = value
                overall_dict[jangsu] = dict
        if jangsu == '관우':
            print(data_)
            print(overall_dict['관우'])
    return overall_dict



jangsu_stat_index = {'0': '공격력', '1': '공격속도', '2': '이동속도', '3': '치명타 확률', '4': '치명타 데미지',
                     '5': '금화 획득', '6': '경험치 획득', '7': '체력'}

jangsuD = ['정원지', '등무', '엄정', '장보', '장량', '반봉', '유섭', '포충', '방열', '목순', '무안국']
jangsuC = ['이각', '곽사', '조무', '서영', '악진', '포신', '한복', '왕광', '장양']
jangsuB = ['하진', '동탁', '조홍', '이전', '화융', '원소']
jangsuA = ['유비', '하후돈', '공손찬', '손견']
jangsuS = ['여포', '조조', '장비', '관우']


today = dt.datetime.today().date()

member_csv_path = './Member.csv'

userID = member_list(member_csv_path)

jangsu_log_all_user = {}

# for name in userID:
#     if name != 'GM조운':
#         continue
#     raw_data_log = pd.read_csv('./JANGSU_log/{}/{}.csv'.format(today,name)).drop(['Unnamed: 0'], axis=1)
#     preprocessing_data_log = data_preprocessing_log(raw_data_log)
#
#     jangsu_log_all_user[name] = preprocessing_data_log

# print(jangsu_log_all_user['GM조운']['관우'])

# print(jangsu_current)

print('{Date} == {today}'.format(Date='Date',today=today))