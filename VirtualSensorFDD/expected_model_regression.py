import statistics
import pandas as pd
import os
import CoolProp as CP
from sklearn.metrics import mean_squared_error
import math
import tensorflow as tf
import numpy as np


def Cv_rmse(actual, pred):
    mse = mean_squared_error(actual, pred)
    rmse = math.sqrt(mse)
    mean = statistics.mean(actual)
    if mean == 0:
        cv_rmse = 'None'
    else:
        cv_rmse = rmse / mean * 100
    return cv_rmse


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


def Qcond(data, mdot):
    delta_h = []
    dis_t = data['cond_in_temp']
    cond_o_t = data['cond_out_temp']
    high_p = data['high_pressure']
    for i in range(len(data)):
        try:
            h_dis = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', dis_t[i] + 273, 'R410A')
            h_cond = CP.CoolProp.PropsSI('H', 'P', high_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273, 'R410A')
        except:
            h_dis = 0
            h_cond = 0
        delta_h.append((h_dis - h_cond) / 1000)
    Q_cond = [x * y for x, y in zip(delta_h, mdot)]
    return Q_cond


def Qevap(data, mdot):
    delta_h = []
    suc_t1 = data['evap_out_temp']
    cond_o_t = data['evap_in_temp']
    low_p = data['low_pressure']
    for i in range(len(data)):
        h_suc = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', suc_t1[i] + 273, 'R410A')
        h_evap = CP.CoolProp.PropsSI('H', 'P', low_p[i] * 98.0665 * 1000, 'T', cond_o_t[i] + 273, 'R410A')
        delta_h.append(abs((h_evap - h_suc) / 1000))
    Q_evap = [x * y for x, y in zip(delta_h, mdot)]
    return Q_evap


file = {'3067/': ['0124']}

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Compressor map data/2022-02-09/'

for key, value in file.items():
    unit = key[:-1]
    overall_ = pd.DataFrame()
    target = pd.DataFrame()
    for date in value:
        testlist = os.listdir(path + key + date)
        directory = path + key + date + '/'
        room_temp_list = []
        relative_capa_list = []
        temp_diff_list = []
        room_temp_avg = 0
        relative_capa_avg = 0
        temp_diff_avg = 0
        df = pd.DataFrame()
        model = 'GB066_{}'.format(unit)
        for i in os.listdir(directory):
            dic = path + key + date + '/' + i
            if 'outdoor' in i:
                df_outdoor = pd.read_csv(dic, index_col=0)
                df['time'] = df_outdoor['updated_time']
                df['amb_temp'] = df_outdoor['outdoor_temperature']
                df['value'] = df_outdoor['value'].apply(lambda x: -x if x < 0 else x)
                df['cond_out_temp'] = df_outdoor['cond_out_temp1']
                if unit == '3065':
                    df['cond_in_temp'] = df_outdoor['discharge_temp1']
                else:
                    for j in range(len(df_outdoor)):
                        if df_outdoor['comp1'][j] == 0:
                            df_outdoor.loc[j, 'discharge_temp1'] = df_outdoor.loc[j, 'discharge_temp2']
                    for j in range(len(df_outdoor)):
                        if df_outdoor['comp2'][j] == 0:
                            df_outdoor.loc[j, 'discharge_temp2'] = df_outdoor.loc[j, 'discharge_temp1']
                    df['cond_in_temp'] = (df_outdoor['discharge_temp1'] + df_outdoor['discharge_temp2']) / 2
                df['evap_out_temp'] = df_outdoor['suction_temp1']
                df['evap_in_temp'] = df['cond_out_temp']
                df['high_pressure'] = df_outdoor['high_pressure']
                df['low_pressure'] = df_outdoor['low_pressure']
            elif 'indoor' in dic:
                room_temp = pd.read_csv(dic)['current_room_temp']
                relative_capa = pd.read_csv(dic)['relative_capa_code']
                setting_temp = pd.read_csv(dic)['indoor_set_temp']
                room_temp_list.append(room_temp)
                relative_capa_list.append(relative_capa)
                temp_diff_list.append(room_temp-setting_temp)
        for j in range(len(room_temp_list)):
            room_temp_avg = room_temp_avg + room_temp_list[j]
            relative_capa_avg = relative_capa_avg + relative_capa_list[j]
            temp_diff_avg = temp_diff_avg + temp_diff_list[j]
        df['room_temp'] = room_temp_avg / len(room_temp_list)
        df['relative_capa'] = relative_capa_avg / len(relative_capa_list)
        df['temp_diff'] = temp_diff_avg / len(temp_diff_list)

        data1 = pd.read_csv(directory+r'/freq1/{}.csv'.format(model))
        data2 = pd.read_csv(directory+r'/freq2/{}.csv'.format(model))

        df['m_dot'] = data1['m_dot_pred'] + data2['m_dot_pred']

        target['value'] = df['value'] / 1000
        target.index = pd.to_datetime(df['time'])

        df = df.reset_index().drop(['index','value'],axis=1)
        df['amb_temp^2'] = df['amb_temp'] * df['amb_temp']
        df['room_temp^2'] = df['room_temp'] * df['room_temp']
        df['relative_capa^2'] = df['relative_capa'] * df['relative_capa']
        df['temp_diff^2'] = df['temp_diff'] * df['temp_diff']
        df['amb_temp*room_temp'] = df['amb_temp'] * df['room_temp']
        df['amb_temp*relative_capa'] = df['amb_temp'] * df['relative_capa']
        df['amb_temp*temp_diff'] = df['amb_temp'] * df['temp_diff']
        df['room_temp*relative_capa'] = df['room_temp'] * df['relative_capa']
        df['room_temp*temp_diff'] = df['room_temp'] * df['temp_diff']
        df['relative_capa*temp_diff'] = df['relative_capa'] * df['temp_diff']

        overall_ = df[['amb_temp','room_temp','relative_capa','temp_diff','amb_temp^2','room_temp^2','relative_capa^2','temp_diff^2','amb_temp*room_temp','amb_temp*relative_capa','amb_temp*temp_diff','room_temp*relative_capa','room_temp*temp_diff','relative_capa*temp_diff']]
        overall_.index = pd.to_datetime(df['time'])

    target = target.resample('5T').mean()
    target = target.rolling(3).mean().fillna(method='bfill')

    overall_ = overall_.resample('5T').mean()
    overall_ = overall_.rolling(3).mean().fillna(method='bfill')

    x_data = overall_
    y_data = target
    predict = []

    tf.compat.v1.disable_eager_execution()

    # placeholder
    X = tf.compat.v1.placeholder(tf.float32, [None, len(overall_.columns)])
    Y = tf.compat.v1.placeholder(tf.float32, [None, len(target.columns)])

    # weight, bias, hypothesis
    W = tf.compat.v1.Variable(tf.compat.v1.random_normal([len(overall_.columns), 1]), name="weight1")
    B = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]), name="bias")
    hypothesis = tf.compat.v1.matmul(X, W)

    # cost / loss
    cost = tf.reduce_mean(tf.square(hypothesis - Y))

    # opimizer
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-2)
    train = optimizer.minimize(cost)

    saver = tf.compat.v1.train.Saver()
    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        for step in range(30000):
            cost_val, W_val, hy_val, _ = sess.run([cost, W, hypothesis, train],feed_dict={X: x_data, Y: y_data})
            if step % 1000 == 0:
                print(step, "Cost: ", cost_val, "\nWeights: \n", W_val)

    columns = ['Actual', 'Predict']
    result = pd.DataFrame(np.column_stack((target, hy_val)), columns=columns)
    result.to_csv('./heating_{}.csv'.format(unit), header=True)
    f = open('./heating_coef_{}.txt'.format(unit), 'a')
    f.write("Weights: \n: {}".format(W_val))
    f.close()