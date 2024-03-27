from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import numpy as np
import matplotlib as mlt
import matplotlib.pyplot as plt
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

tf.compat.v1.disable_eager_execution()

# GPU
gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

tf.compat.v1.set_random_seed(777)

if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    mlt.use('Agg')

# train Parameters
seq_length = 144
input_dim = 5
hidden_dim = 64
output_dim = 1
learning_rate = 0.01
iterations = 30000

data = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\PV python\poolday.csv').set_index('Date/Time')

REH = np.array(data['REH']).reshape(-1,1)
Tamb = np.array(data['T3H']).reshape(-1,1)
azimuth = np.array(data['azimuth']).reshape(-1,1)
altitude = np.array(data['hourangle']).reshape(-1,1)
radiation = np.array(data['Environment:Site Direct Solar Radiation Rate per Area [W/m2](TimeStep)']).reshape(-1,1)
target = np.array(data['PV LOAD CENTER:Electric Load Center Produced Electric Power [W](TimeStep)']).reshape(-1,1)

data = np.column_stack([REH,Tamb,azimuth,altitude,radiation,target])
print(pd.DataFrame(data))

train_size = int(len(data) * 0.7)
train_set = data[0:train_size]
test_set = data[:]
print(len(test_set))


def build_dataset(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        _x = time_series[i: i + seq_length, :-1]
        _y = time_series[i + seq_length, [-1]] # Next Power Output
        dataX.append(_x)
        dataY.append(_y)
    return np.array(dataX), np.array(dataY)


trainX, trainY = build_dataset(train_set, seq_length)
testX, testY = build_dataset(test_set, seq_length)

X = tf.compat.v1.placeholder(tf.float32, [None, seq_length, input_dim])
Y = tf.compat.v1.placeholder(tf.float32, [None, 1])


def lstm_cell():
    cell = tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=hidden_dim, activation=tf.tanh, state_is_tuple=True)
    return cell

cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([lstm_cell() for _ in range(2)],state_is_tuple=True)
output4, _states = tf.compat.v1.nn.dynamic_rnn(cell, X, dtype=tf.float32)


class FULLYCONNECTED(keras.Model): # tf.keras.layers.fully_connected()
    def __init__(self):
        super().__init__('mlp_policy')

        self.dl1 = keras.layers.Dense(output_dim, activation=tf.keras.activations.linear)

    def fully_connected(self, inputs):
        dl1 = self.dl1(inputs)

        return dl1


fully_connected = FULLYCONNECTED()
Y_pred = fully_connected.fully_connected(output4[:, -1]) #fully_connected() output

loss = tf.reduce_sum(tf.square(Y_pred - Y))

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

targets = tf.compat.v1.placeholder(tf.float32, [None, 1])
predictions = tf.compat.v1.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets-predictions)))

saver = tf.compat.v1.train.Saver()

with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)) as sess:
    init = tf.compat.v1.global_variables_initializer()
    sess.run(init)

    for i in range(iterations): # Training step
        _, step_loss = sess.run([train, loss], feed_dict={X:trainX, Y:trainY})

        if i% 100 == 0:
            print("[step:{}] loss: {}".format(i, step_loss))
            saver.save(sess, './checkpoint/test_saver', i)

    test_predict = sess.run(Y_pred, feed_dict={X:testX}) # Test step
    rmse_val = sess.run(rmse, feed_dict={targets:testY,predictions:test_predict})
    print("RMSE: {}".format(rmse_val))


Test_pred = pd.DataFrame(test_predict)
TestY = pd.DataFrame(testY)
Train_result = pd.concat([TestY, Test_pred], ignore_index=True, axis=1)
Train_result.columns = ['Train', 'Prediction']
Train_result.to_csv('./poolday_RNN.csv')


def plot_result():
    plt.cla()
    plt.clf()
    fig, ax1 = plt.subplots(figsize=(16, 9))
    ax1.plot(range(len(Test_pred)), Test_pred, color='b', linewidth=1.5,linestyle='-')
    ax1.plot(range(len(TestY)), TestY, color='r',linestyle='-', linewidth=1.5)
    ax1.set_ylabel('Target',fontsize=14)
    ax1.legend(['Predict','Actual'],loc='upper right',fontsize='large')
    plt.show()


plot_result()


