import pandas as pd
import os
import numpy as np
import tensorflow as tf

path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/virtual air flow sensor/'
fault_level_path = 'C:/Users/user/OneDrive - Chonnam National University/학석사 연계과정/코드/FDD python/samsung/Dataset2/3066/fault_level'
datalist = {'3066': ['0728','0729','0730','0804','0805']}

data = pd.DataFrame()
level = pd.DataFrame()
data_level = pd.DataFrame()
for unit, datelist in datalist.items():
    for day in datelist:
        dataa = pd.read_csv(path+unit+'/'+day+'/virtual_blockage_sensor.csv').set_index('Time').drop('Unnamed: 0',axis=1)
        # fault_level = pd.read_csv(fault_level_path+'/'+day+'/cond_in_air_velocity_{}_fault_level.csv'.format(day)).drop('Unnamed: 0',axis=1)
        data = pd.concat([data,dataa],axis=0)
        # level = pd.concat([level, fault_level], axis=0)
    # data_level = pd.concat([data,level],axis=1)
    # data_level = data_level.dropna(axis=0)
    data = data.dropna(axis=0)

# data_level['fan_step'] = data_level['fan_step'].apply(lambda x: None if x == 0 else x)
# data_level['fault_level'] = data_level['fault_level'].apply(lambda x: None if x > 1 else x)
# data_level = data_level.dropna(axis=0)

print(data)


overall = pd.DataFrame()
target = pd.DataFrame()

target['fault_level'] = data['fault_level'].astype(float)
overall['cond_temp_diff'] = (data['cond_in_ref'] - data['cond_out_ref']) - 30
overall['fan_step'] = data['fan_step'] - 14
overall['cond_temp_diff*fan_step'] = overall['cond_temp_diff'] * overall['fan_step']

overall = overall.rolling(15).mean().fillna(method='bfill')
target = target.rolling(15).mean().fillna(method='bfill')

overall.to_csv('./input.csv')

x_data = overall
y_data = target
predict = []

#placeholder
X = tf.compat.v1.placeholder(tf.float32, [None,len(overall.columns)])
Y = tf.compat.v1.placeholder(tf.float32,[None,len(target.columns)])

# weight, bias, hypothesis
W = tf.compat.v1.Variable(tf.compat.v1.random_normal([len(overall.columns),1]), name="weight1")
B = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]), name="bias")
hypothesis = tf.compat.v1.matmul(X,W)

#cost / loss
cost = tf.reduce_mean(tf.square(hypothesis - Y))

#opimizer
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-2)
train = optimizer.minimize(cost)

saver = tf.compat.v1.train.Saver()
with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())
    for step in range(10000):
        cost_val, W_val, B_val, hy_val, _ = sess.run([cost, W, B, hypothesis, train], feed_dict={X: x_data, Y: y_data})
        if step % 1000 == 0:
            print(step, "Cost: ", cost_val, "\nWeights: \n", W_val, "\nBias: \n", B_val)

columns = ['Actual', 'Predict']
result = pd.DataFrame(np.column_stack((target,hy_val)),columns=columns)
result.to_csv('./virtual_blockage_sensor.csv',header=True)
f = open('./coefficient_blockage.txt', 'a')
f.write("Weights: \n: {}, \nBias: \n: {}".format(W_val,B_val))
f.close()
