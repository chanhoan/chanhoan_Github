from dash import Dash, html, Input, Output, dcc, dash_table, ctx
import dash_bootstrap_components as dbc
import datetime as dt
import pandas as pd
import ast

jangsu_listD = ['정원지', '등무', '엄정', '장보', '장량', '반봉', '유섭', '포충', '방열', '목순', '무안국', ]
jangsu_listC = ['이각', '곽사', '조무', '서영', '악진', '포신', '한복', '왕광', '장양', '하진', '동탁', ]
jangsu_listB = ['조홍', '이전', '화웅', '원소', ]
jangsu_listA = ['유비', '하후돈', '공손찬', '손견', ]
jangsu_listS = ['여포', '조조', '장'
                            '비', '관우']

def member_list(path):
    member_data = pd.read_csv(path,encoding='utf-8')

    member_list = member_data['username'].tolist()

    return member_list


def data_preprocessing_current(data):
    overall_dict = {}
    for jangsu in jangsu_listD + jangsu_listC + jangsu_listB + jangsu_listA + jangsu_listS:
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
    for jangsu in jangsu_listD + jangsu_listC + jangsu_listB + jangsu_listA + jangsu_listS:
        data_ = data[data['Jangsu'] == jangsu].reset_index(drop=True)
        for i in range(len(data_)):
            if jangsu in jangsu_listD:
                index = [j for j, x in enumerate(jangsu_listD) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsu_listC:
                index = [j for j, x in enumerate(jangsu_listC) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsu_listB:
                index = [j for j, x in enumerate(jangsu_listB) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsu_listA:
                index = [j for j, x in enumerate(jangsu_listA) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            elif jangsu in jangsu_listS:
                index = [j for j, x in enumerate(jangsu_listS) if x == jangsu]
                data_.loc[i, 'Special'] = ast.literal_eval(data_.loc[i, 'Special'])[index[0]]
            data_.loc[i, 'Special'] = [data_.loc[i, 'Special'][j].split(',') for j in
                                       range(len(data_.loc[i, 'Special']))]
            for s in range(len(data_.loc[i, 'Special'])):
                data_.loc[i, 'Special'][s][0] = jangsu_stat_index[data_.loc[i, 'Special'][s][0]]
                data_.loc[i, 'Special'][s][1] = round(float(data_.loc[i, 'Special'][s][1]) * 100)
                data_.loc[i, 'Special'][s][2] = round(float(data_.loc[i, 'Special'][s][2]) * 100)
        dict = {}
        try:
            for k in range(len(data_.loc[0, 'Special'])):
                value = []
                for i in range(len(data_)):
                    if data_.loc[i, 'Special'][k][2] == 0 and data_.loc[i, 'Special'][k][1] != 0:
                        if data_.loc[i+1, 'Special'][k][2] != data_.loc[i, 'Special'][k][2] and data_.loc[i+1, 'Special'][k][1] != data_.loc[i, 'Special'][k][1]:
                            value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                          '능력치': data_.loc[i, 'Special'][k][0],
                                          '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                        elif i == len(data_)-1:
                            value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                          '능력치': data_.loc[i, 'Special'][k][0],
                                          '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                    elif data_.loc[i, 'Special'][k][1] == 0 and data_.loc[i, 'Special'][k][2] != 0:
                        if data_.loc[i + 1, 'Special'][k][2] != data_.loc[i, 'Special'][k][2] and data_.loc[i + 1, 'Special'][k][1] != data_.loc[i, 'Special'][k][1]:
                            value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                          '능력치': data_.loc[i, 'Special'][k][0],
                                          '수치': 'x' + str(data_.loc[i, 'Special'][k][2]) + '%'})
                        elif i == len(data_)-1:
                            value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                          '능력치': data_.loc[i, 'Special'][k][0],
                                          '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                    dict['능력치 {}'.format(k + 1)] = value
                overall_dict[jangsu] = dict
        except:
            for k in range(1):
                value = []
                for i in range(len(data_)):
                    if data_.loc[i, 'Special'][k][2] == 0 and data_.loc[i, 'Special'][k][1] != 0:
                        value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                      '능력치': data_.loc[i, 'Special'][k][0],
                                      '수치': '+' + str(data_.loc[i, 'Special'][k][1]) + '%'})
                    elif data_.loc[i, 'Special'][k][1] == 0 and data_.loc[i, 'Special'][k][2] != 0:
                        value.append({'Date': data_.loc[i, 'Date'], 'Time': data_.loc[i, 'Time'],
                                      '능력치': data_.loc[i, 'Special'][k][0],
                                      '수치': 'x' + str(data_.loc[i, 'Special'][k][2]) + '%'})
                    dict['능력치 {}'.format(k + 1)] = value
                overall_dict[jangsu] = dict
    return overall_dict


jangsu_stat_index = {'0': '공격력', '1': '공격속도', '2': '이동속도', '3': '치명타 확률', '4': '치명타 데미지',
                     '5': '금화 획득', '6': '경험치 획득', '7': '체력'}

# today = dt.datetime.today().date()
today = "2023-05-19"
today = dt.datetime.strptime(today,'%Y-%m-%d').date()
member_csv_path = './Member.csv'
userID = member_list(member_csv_path)

jangsu_current_all_user = {}
jangsu_log_all_user = {}

for name in userID:
    raw_data_current = pd.read_csv('./JANGSU_current/{}/{}.csv'.format(today,name)).drop(['Unnamed: 0', 'UserID'], axis=1)
    preprocessing_data_current = data_preprocessing_current(raw_data_current)
    jangsu_current_all_user[name] = preprocessing_data_current

    raw_data_log = pd.read_csv('./JANGSU_log/{}/{}.csv'.format(today,name)).drop(['Unnamed: 0'], axis=1)
    preprocessing_data_log = data_preprocessing_log(raw_data_log)
    jangsu_log_all_user[name] = preprocessing_data_log

app = Dash(__name__, suppress_callback_exceptions=True)

button_layoutS = []
button_layoutA = []
button_layoutB = []
button_layoutC = []
button_layoutD = []
row_layoutS = []
row_layoutA = []
row_layoutB = []
row_layoutC = []
row_layoutD = []
for i, jangsu in enumerate(jangsu_listS):
    button_style = {'font-size': '20px', 'width': '450px', 'height': '30px', 'color': 'white', 'margin-bottom': '5px',
                    'margin-right': '5px', 'border': '4.5px-black', 'background-color': 'purple'}

    button = html.Button(jangsu, id='S-btn-nclicks-{}'.format(i), n_clicks=0, style=button_style, )
    row_layoutS.append(button)
    if (i + 1) % 4 == 0:
        button_layoutS.append(dbc.Row(row_layoutS))
        row_layoutS = []
for i, jangsu in enumerate(jangsu_listA):
    button_style = {'font-size': '20px', 'width': '450px', 'height': '30px', 'color': 'white', 'margin-bottom': '5px',
                    'margin-right': '5px', 'border': '4.5px-black', 'background-color': 'red'}

    button = html.Button(jangsu, id='A-btn-nclicks-{}'.format(i), n_clicks=0, style=button_style, )
    row_layoutA.append(button)
    if (i + 1) % 4 == 0:
        button_layoutA.append(dbc.Row(row_layoutA))
        row_layoutA = []
for i, jangsu in enumerate(jangsu_listB):
    button_style = {'font-size': '20px', 'width': '450px', 'height': '30px', 'color': 'white', 'margin-bottom': '5px',
                    'margin-right': '5px', 'border': '4.5px-black', 'background-color': 'blue'}

    button = html.Button(jangsu, id='B-btn-nclicks-{}'.format(i), n_clicks=0, style=button_style, )
    row_layoutB.append(button)
    if (i + 1) % 4 == 0:
        button_layoutB.append(dbc.Row(row_layoutB))
        row_layoutB = []
for i, jangsu in enumerate(jangsu_listC):
    button_style = {'font-size': '20px', 'width': '450px', 'height': '30px', 'color': 'white', 'margin-bottom': '5px',
                    'margin-right': '5px', 'border': '4.5px-black', 'background-color': 'limegreen'}

    button = html.Button(jangsu, id='C-btn-nclicks-{}'.format(i), n_clicks=0, style=button_style, )
    row_layoutC.append(button)
    if (i + 1) % 4 == 0:
        button_layoutC.append(dbc.Row(row_layoutC))
        row_layoutC = []
for i, jangsu in enumerate(jangsu_listD):
    button_style = {'font-size': '20px', 'width': '450px', 'height': '30px', 'color': 'white', 'margin-bottom': '5px',
                    'margin-right': '5px', 'border': '4.5px-black', 'background-color': 'silver'}

    button = html.Button(jangsu, id='D-btn-nclicks-{}'.format(i), n_clicks=0, style=button_style, )
    row_layoutD.append(button)
    if (i + 1) % 4 == 0:
        button_layoutD.append(dbc.Row(row_layoutD))
        row_layoutD = []

if row_layoutS:
    button_layoutS.append(dbc.Row(row_layoutS))
if row_layoutA:
    button_layoutA.append(dbc.Row(row_layoutA))
if row_layoutB:
    button_layoutB.append(dbc.Row(row_layoutB))
if row_layoutC:
    button_layoutC.append(dbc.Row(row_layoutC))
if row_layoutD:
    button_layoutD.append(dbc.Row(row_layoutD))


app.layout = html.Div([
    dbc.Row([
        dcc.Dropdown(userID, 'user', id='user-dd',searchable=True),
        html.Div(id='user-output-container'),
        html.Hr(),
    ]),
    dbc.Row([
            dcc.Dropdown(['S등급', 'A등급', 'B등급', 'C등급', 'D등급'], 'value', id='grade-dd'),
            html.Div(id='grade-output-container'),
            html.Hr(),
    ])
])

def detale_table(dataframe, stat_num, msg):
    global update_trigger
    table_style_data = {'white_Space': 'normal', 'height': 'auto', 'font_size': '15px'}
    table_style_cond = [{column_name: '200px'} for column_name in dataframe.columns]
    if len(dataframe) == 0:
        msg2 = '최근 1주일 내 변동 이력이 없습니다.'

        return html.Div([
        html.Hr(),
        html.Div(msg),
        html.Div(msg2),
        dbc.Alert(id='tbl_out')
        ])
    else:
        update_trigger = today in dataframe['Date']
        dataframe = dataframe.sort_values(['Date','Time'], ascending=False)
        dafault_table = dash_table.DataTable(dataframe.to_dict('records'),
                                             id='data-detale-{}'.format(stat_num), fixed_rows={'headers':True},style_table={'height':'400px'},
                                             style_data=table_style_data, style_cell_conditional=table_style_cond,
                                             fill_width=True)

        return html.Div([
            html.Hr(),
            html.Div(msg),
            dafault_table,
            dbc.Alert(id='tbl_out')
        ])


def detail_table_reset():
    global existing_tables
    existing_tables = []


def generate_table(dataframe,msg):
    global jangsu_
    jangsu_ = msg
    column_widths = {'능력치': '200px', '수치': '200px'}
    table_style_data = {'white_Space': 'normal', 'height': 'auto', 'font_size': '15px'}
    table_style_cond = [{'if': {'column_id': col}, 'width': width} for col, width in column_widths.items()]

    dafault_table = dash_table.DataTable(dataframe.to_dict('records'),
                                         id='data-table',
                                         style_data=table_style_data, style_cell_conditional=table_style_cond,
                                         fill_width=False)

    return html.Div([
        html.Hr(),
        html.Div(msg),
        dafault_table,
        dbc.Alert(id='tbl_out')
    ])


def generate_button(grade, user):
    global username
    username = user
    if grade == 'S등급':
        return html.Div([
            dbc.Row([
                html.Hr(),
                html.Div(button_layoutS, className='scroll-container',
                         style={'overflowY': 'scroll', 'height': '140px'}),
                html.Div(id='container-button-timestamp-s'),
            ], className='button-wrapper')
        ])
    elif grade == 'A등급':
        return html.Div([
            dbc.Row([
                html.Hr(),
                html.Div(button_layoutA, className='scroll-container',
                         style={'overflowY': 'scroll', 'height': '140px'}),
                html.Div(id='container-button-timestamp-a'),
            ], className='button-wrapper')
        ])
    elif grade == 'B등급':
        return html.Div([
            dbc.Row([
                html.Hr(),
                html.Div(button_layoutB, className='scroll-container',
                         style={'overflowY': 'scroll', 'height': '140px'}),
                html.Div(id='container-button-timestamp-b'),
            ], className='button-wrapper')
        ])
    elif grade == 'C등급':
        return html.Div([
            dbc.Row([
                html.Hr(),
                html.Div(button_layoutC, className='scroll-container',
                         style={'overflowY': 'scroll', 'height': '140px'}),
                html.Div(id='container-button-timestamp-c'),
            ], className='button-wrapper')
        ])
    elif grade == 'D등급':
        return html.Div([
            dbc.Row([
                html.Hr(),
                html.Div(button_layoutD, className='scroll-container',
                         style={'overflowY': 'scroll', 'height': '140px'}),
                html.Div(id='container-button-timestamp-d'),
            ], className='button-wrapper')
        ])


@app.callback(
    Output('grade-output-container', 'children'),
    [Input('grade-dd', 'value'), Input('user-dd', 'value')]
)
def get_button(grade, user):
    detail_table_reset()
    if grade is not None and user is not None:
        return generate_button(grade, user),
    else:
        return None


@app.callback(
    Output('container-button-timestamp-d', 'children'),
    [Input('D-btn-nclicks-{}'.format(j), 'n_clicks') for j in range(len(jangsu_listD))],
)
def update_table_D(*args):
    detail_table_reset()
    if ctx.triggered_id:
        detail_table_reset()
        data = jangsu_current_all_user[username]
        button_id = ctx.triggered_id.split('-')[-1]
        selected_data = data[jangsu_listD[int(button_id)]]
        selected_df = pd.DataFrame.from_dict(selected_data, orient='index', columns=['능력치', '수치'])
        msg = '{}'.format(jangsu_listD[int(button_id)])
        return generate_table(selected_df,msg)


@app.callback(
    Output('container-button-timestamp-c', 'children'),
    [Input('C-btn-nclicks-{}'.format(j), 'n_clicks') for j in range(len(jangsu_listC))],
)
def update_table_C(*args):
    detail_table_reset()
    if ctx.triggered_id:
        detail_table_reset()
        data = jangsu_current_all_user[username]
        button_id = ctx.triggered_id.split('-')[-1]
        selected_data = data[jangsu_listC[int(button_id)]]
        selected_df = pd.DataFrame.from_dict(selected_data, orient='index', columns=['능력치', '수치'])
        msg = '{}'.format(jangsu_listC[int(button_id)])
        return generate_table(selected_df,msg)


@app.callback(
    Output('container-button-timestamp-b', 'children'),
    [Input('B-btn-nclicks-{}'.format(j), 'n_clicks') for j in range(len(jangsu_listB))],
)
def update_table_B(*args):
    detail_table_reset()
    if ctx.triggered_id:
        detail_table_reset()
        data = jangsu_current_all_user[username]
        button_id = ctx.triggered_id.split('-')[-1]
        selected_data = data[jangsu_listB[int(button_id)]]
        selected_df = pd.DataFrame.from_dict(selected_data, orient='index', columns=['능력치', '수치'])
        msg = '{}'.format(jangsu_listB[int(button_id)])
        return generate_table(selected_df,msg)


@app.callback(
    Output('container-button-timestamp-a', 'children'),
    [Input('A-btn-nclicks-{}'.format(j), 'n_clicks') for j in range(len(jangsu_listB))],
)
def update_table_A(*args):
    detail_table_reset()
    if ctx.triggered_id:
        detail_table_reset()
        data = jangsu_current_all_user[username]
        button_id = ctx.triggered_id.split('-')[-1]
        selected_data = data[jangsu_listA[int(button_id)]]
        selected_df = pd.DataFrame.from_dict(selected_data, orient='index', columns=['능력치', '수치'])
        msg = '{}'.format(jangsu_listA[int(button_id)])
        return generate_table(selected_df,msg)


@app.callback(
    Output('container-button-timestamp-s', 'children'),
    [Input('S-btn-nclicks-{}'.format(j), 'n_clicks') for j in range(len(jangsu_listS))],
)
def update_table_S(*args):
    detail_table_reset()
    if ctx.triggered_id:
        detail_table_reset()
        data = jangsu_current_all_user[username]
        button_id = ctx.triggered_id.split('-')[-1]
        selected_data = data[jangsu_listS[int(button_id)]]
        selected_df = pd.DataFrame.from_dict(selected_data, orient='index', columns=['능력치', '수치'])
        msg = '{}'.format(jangsu_listS[int(button_id)])
        return generate_table(selected_df,msg)



@app.callback(Output('tbl_out', 'children'), Input('data-table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell:
        table_id = 'data-detale-{}'.format(int(active_cell['row']) + 1)
        if int(active_cell['column']) == 1 and table_id not in existing_tables:
            try:
                selected_data = jangsu_log_all_user[username][jangsu_]['능력치 {}'.format(int(active_cell['row']) + 1)]
            except:
                selected_data = None
            msg = '능력치 {}'.format(int(active_cell['row']) + 1)
            selected_df = pd.DataFrame(selected_data)
            existing_tables.append(table_id)
            return detale_table(selected_df, int(active_cell['row'])+1,msg)


if __name__ == '__main__':
    app.run_server(debug=True)
