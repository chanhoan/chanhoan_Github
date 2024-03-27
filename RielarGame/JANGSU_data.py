import re
import random
import pandas as pd
import datetime as dt
import os

jangsuD = ['정원지', '등무', '엄정', '장보', '장량', '반봉', '유섭', '포충', '방열', '목순', '무안국']
jangsuC = ['이각', '곽사', '조무', '서영', '악진', '포신', '한복', '왕광', '장양']
jangsuB = ['하진', '동탁', '조홍', '이전', '화웅', '원소']
jangsuA = ['유비', '하후돈', '공손찬', '손견']
jangsuS = ['여포', '조조', '장비', '관우']


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return None


def member_list(path):
    member_data = pd.read_csv(path, encoding='utf-8')

    member_list = member_data['username'].tolist()

    return member_list


def load_all_csv(path):
    combined_data = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):  # CSV 파일만 선택
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]  # 파일명에서 확장자 제거

                if file_name not in combined_data:
                    # 파일명이 딕셔너리에 없는 경우 새로운 키로 추가
                    combined_data[file_name] = pd.read_csv(file_path)
                else:
                    # 파일명이 딕셔너리에 있는 경우 기존 데이터에 추가
                    current_data = pd.read_csv(file_path)
                    combined_data[file_name] = pd.concat([combined_data[file_name], current_data], ignore_index=False).drop(['Unnamed: 0'],axis=1)

    return combined_data


def JANGSU_logs_csv_today(jangsu_csv_path, column, user_list, day, weekago):
    jangsu_result = pd.read_csv(jangsu_csv_path, encoding='utf-8')
    weekago = pd.to_datetime(weekago)
    day = pd.to_datetime(day)
    jangsu_result['log_date'] = pd.to_datetime(jangsu_result['log_date'])
    jangsu_result = jangsu_result[jangsu_result['log_date'].between(weekago, day)].reset_index(drop=True)

    jangsu_result['date'] = pd.to_datetime(jangsu_result['log_date']).dt.date
    jangsu_result['time'] = pd.to_datetime(jangsu_result['log_date']).dt.time

    for name in user_list:
        pd_logs_jangsu = pd.DataFrame(columns=column)
        user_data = jangsu_result[jangsu_result['log_identifer'] == name].copy()

        pd_logs_jangsu['UserID'] = user_data['log_identifer']
        pd_logs_jangsu["Date"] = user_data['date']
        pd_logs_jangsu["Time"] = user_data['time']
        pd_logs_jangsu["DataDetail"] = user_data['log_details']
        pd_logs_jangsu = pd_logs_jangsu.reset_index(drop=True)

        concat_pd = pd.DataFrame(columns=['UserID', 'Date', 'Time', 'Jangsu', 'Special'])

        jangsu_special = {'Date': [], 'Time': [], 'Jangsu': [], 'Special': []}
        for j in pd_logs_jangsu.index:
            str_data = pd_logs_jangsu.loc[j, 'DataDetail']
            pattern = r'\|([^|]+?)(?=;\||;\n})'
            matches = re.findall(pattern, str_data)
            jangsu_pattern = r'"whichjangsu": (\d+)'
            if 'specialD' in str_data:
                value_lists = [list(map(str, item.split(';'))) for item in matches]
                jangsu_special['Special'].append(value_lists)
                jangsu_special['Date'].append(pd_logs_jangsu.loc[j, 'Date'])
                jangsu_special['Time'].append(pd_logs_jangsu.loc[j, 'Time'])
                try:
                    whichjangsu_value = next(int(match.group(1)) for match in re.finditer(jangsu_pattern, str_data))
                    jangsu_special['Jangsu'].append(jangsuD[whichjangsu_value])
                except:
                    whichjangsu_value = random.randint(0,len(jangsuA)-1)
                    jangsu_special['Jangsu'].append(jangsuD[whichjangsu_value])
            elif 'specialC' in str_data:
                value_lists = [list(map(str, item.split(';'))) for item in matches]
                jangsu_special['Special'].append(value_lists)
                jangsu_special['Date'].append(pd_logs_jangsu.loc[j, 'Date'])
                jangsu_special['Time'].append(pd_logs_jangsu.loc[j, 'Time'])
                try:
                    whichjangsu_value = next(int(match.group(1)) for match in re.finditer(jangsu_pattern, str_data))
                    jangsu_special['Jangsu'].append(jangsuC[whichjangsu_value])
                except:
                    whichjangsu_value = random.randint(0,len(jangsuA)-1)
                    jangsu_special['Jangsu'].append(jangsuC[whichjangsu_value])
            elif 'specialB' in str_data:
                value_lists = [list(map(str, item.split(';'))) for item in matches]
                jangsu_special['Special'].append(value_lists)
                jangsu_special['Date'].append(pd_logs_jangsu.loc[j, 'Date'])
                jangsu_special['Time'].append(pd_logs_jangsu.loc[j, 'Time'])
                try:
                    whichjangsu_value = next(int(match.group(1)) for match in re.finditer(jangsu_pattern, str_data))
                    jangsu_special['Jangsu'].append(jangsuB[whichjangsu_value])
                except:
                    jangsu_special['Jangsu'].append(jangsuB[whichjangsu_value])
            elif 'specialA' in str_data:
                value_lists = [list(map(str, item.split(';'))) for item in matches]
                jangsu_special['Special'].append(value_lists)
                jangsu_special['Date'].append(pd_logs_jangsu.loc[j, 'Date'])
                jangsu_special['Time'].append(pd_logs_jangsu.loc[j, 'Time'])
                try:
                    whichjangsu_value = next(int(match.group(1)) for match in re.finditer(jangsu_pattern, str_data))
                    jangsu_special['Jangsu'].append(jangsuA[whichjangsu_value])
                except:
                    whichjangsu_value = random.randint(0,len(jangsuA)-1)
                    jangsu_special['Jangsu'].append(jangsuA[whichjangsu_value])
            elif 'specialS' in str_data:
                value_lists = [list(map(str, item.split(';'))) for item in matches]
                jangsu_special['Special'].append(value_lists)
                jangsu_special['Date'].append(pd_logs_jangsu.loc[j, 'Date'])
                jangsu_special['Time'].append(pd_logs_jangsu.loc[j, 'Time'])
                try:
                    whichjangsu_value = next(int(match.group(1)) for match in re.finditer(jangsu_pattern, str_data))
                    jangsu_special['Jangsu'].append(jangsuS[whichjangsu_value])
                except:
                    whichjangsu_value = random.randint(0,len(jangsuA)-1)
                    jangsu_special['Jangsu'].append(jangsuS[whichjangsu_value])

        # final_df = pd.DataFrame(columns=['Date', 'Time', 'Jangsu', 'Special'],index=range(len(jangsu_special)))
        jangsu_df = pd.DataFrame(jangsu_special)

        final_df_save_path = './JANGSU_log/{}'.format(day.date() - dt.timedelta(days=1))

        create_path(final_df_save_path)

        jangsu_df.to_csv(final_df_save_path + '/{}.csv'.format(name), encoding='utf-8-sig')


def current_jangsu(jangsu_csv_path, user_list, day):
    jangsu_result = pd.read_csv(jangsu_csv_path, encoding='utf-8')
    jangsu_result = jangsu_result[['username','specialD','specialC','specialB','specialA','specialS']]

    for name in user_list:
        current_jangsu_df = jangsu_result[jangsu_result['username'] == name]

        jangsu_special_D = {'specialD': []}
        jangsu_special_C = {'specialC': []}
        jangsu_special_B = {'specialB': []}
        jangsu_special_A = {'specialA': []}
        jangsu_special_S = {'specialS': []}
        for j in current_jangsu_df.index:
            str_data = current_jangsu_df.loc[j, 'specialD'].split('|')
            str_data = [x for x in str_data if x != '']
            jangsu_special_D['specialD'].append(str_data)

            str_data = current_jangsu_df.loc[j, 'specialC'].split('|')
            str_data = [x for x in str_data if x != '']
            jangsu_special_C['specialC'].append(str_data)

            str_data = current_jangsu_df.loc[j, 'specialB'].split('|')
            str_data = [x for x in str_data if x != '']
            jangsu_special_B['specialB'].append(str_data)

            str_data = current_jangsu_df.loc[j, 'specialA'].split('|')
            str_data = [x for x in str_data if x != '']
            jangsu_special_A['specialA'].append(str_data)

            str_data = current_jangsu_df.loc[j, 'specialS'].split('|')
            str_data = [x for x in str_data if x != '']
            jangsu_special_S['specialS'].append(str_data)


        jangsu_special_dict = {**jangsu_special_D, **jangsu_special_C, **jangsu_special_B, **jangsu_special_A, **jangsu_special_S}

        jangsu_df = pd.DataFrame(jangsu_special_dict)
        jangsu_df['UserID'] = [name for _ in range(len(jangsu_df))]
        final_df = pd.DataFrame(columns=jangsuD + jangsuC + jangsuB + jangsuA + jangsuS + ['UserID'], index=range(len(jangsu_df)))
        for i, jangsu in enumerate(jangsuD):
            try:
                final_df[jangsu] = jangsu_df.loc[0,'specialD'][i]
                final_df['UserID'] = jangsu_df['UserID']
            except:
                continue
        for i, jangsu in enumerate(jangsuC):
            try:
                final_df[jangsu] = jangsu_df.loc[0,'specialC'][i]
                final_df['UserID'] = jangsu_df['UserID']
            except:
                continue
        for i, jangsu in enumerate(jangsuB):
            try:
                final_df[jangsu] = jangsu_df.loc[0,'specialB'][i]
                final_df['UserID'] = jangsu_df['UserID']
            except:
                continue
        for i, jangsu in enumerate(jangsuA):
            try:
                final_df[jangsu] = jangsu_df.loc[0,'specialA'][i]
                final_df['UserID'] = jangsu_df['UserID']
            except:
                continue
        for i, jangsu in enumerate(jangsuS):
            try:
                final_df[jangsu] = jangsu_df.loc[0,'specialS'][i]
                final_df['UserID'] = jangsu_df['UserID']
            except:
                continue

        final_df_save_path = './JANGSU_current/{}'.format(day - dt.timedelta(days=1))

        create_path(final_df_save_path)

        final_df.to_csv(final_df_save_path + '/{}.csv'.format(name), encoding='utf-8-sig')


jangsu_list = ['정원지', '등무', '엄정', '장보', '장량', '반봉', '유섭', '포충', '방열', '목순', '무안국',
               '이각', '곽사', '조무', '서영', '악진', '포신', '한복', '왕광', '장양', '하진', '동탁',
               '조홍', '이전', '화웅', '원소', '유비', '하후돈', '공손찬', '손견', '여포', '조조', '장비',
               '관우']

current_jangsu_path = './JangsuData.csv '
jangsu_csv_path = './logs_JANGSU.csv'
member_csv_path = './Member.csv'
jangsu_csv_path_all = 'JANGSU_log'

weekago = dt.datetime.today().date() - dt.timedelta(weeks=1)
today = dt.datetime.today().date() + dt.timedelta(days=1)

JangsuColumn = ['UserID', 'Date', 'Time', 'DataDetail']

un_list = member_list(member_csv_path)

jangsu_csv_dict = load_all_csv(jangsu_csv_path_all)

JANGSU_logs_csv_today(jangsu_csv_path, JangsuColumn, un_list, today, weekago)
current_jangsu(current_jangsu_path, un_list, today)
