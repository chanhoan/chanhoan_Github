from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import numpy as np
import matplotlib as mlt
import matplotlib.pyplot as plt
import os
import pandas as pd


# # GPU
# gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)
# sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

tf.compat.v1.set_random_seed(777)

if  "DISPLAY" not in os.environ:
    # remove Travis CI Error
    mlt.use('Agg')

# nomalize
def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)

# train Parameters
seq_length = 28
input_dim = 9
hidden_dim = 64
output_dim = 1
learning_rate = 0.01
iterations = 500

# Open, High, Low, Volume, Close
xy = np.loadtxt('test1data.csv', delimiter=",")

# train/test split
train_size = int(len(xy) * 0.7)
train_set = xy[0:train_size]
test_set = xy[train_size - seq_length:]
# Scale each
train_set = MinMaxScaler(train_set)
test_set = MinMaxScaler(test_set)

# build datasets
def build_dataset(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        _x = time_series[i: i + seq_length, :]
        _y = time_series[i + seq_length, [-1]] # Next Power Output
        # print(_x, "->", _y)
        dataX.append(_x)
        dataY.append(_y)
    return np.array(dataX), np.array(dataY)

trainX, trainY = build_dataset(train_set, seq_length)
testX, testY = build_dataset(test_set, seq_length)
print(np.shape(testX))

# placeholder
X = tf.compat.v1.placeholder(tf.float32, [None, seq_length, input_dim])
Y = tf.compat.v1.placeholder(tf.float32, [None, 1])


 # build a LSTM network
cell = tf.compat.v1.nn.rnn_cell.BasicLSTMCell(
    num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
output4, _states = tf.compat.v1.nn.dynamic_rnn(cell, X, dtype=tf.float32)

class FULLYCONNECTED(keras.Model): # tf.keras.layers.fully_connected()
    def __init__(self):
        super().__init__('mlp_policy')

        self.dl1 = keras.layers.Dense(output_dim, activation=None)

    def call(self, inputs):
        dl1 = self.dl1(inputs)

        return dl1
fully_connected = FULLYCONNECTED()
Y_pred = fully_connected.call(output4[:, -1]) #fully_connected() output
print(np.shape(Y_pred))


# cost/loss
loss = tf.reduce_sum(tf.square(Y_pred - Y)) # sum of the squares?
# loss = tf.keras.losses.MSE(y_true=Y,y_pred=Y_pred)

# Optimizer
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

#RMSE
targets = tf.compat.v1.placeholder(tf.float32, [None, 1])
predictions = tf.compat.v1.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets-predictions)))

# Model Saver
saver = tf.compat.v1.train.Saver()

with tf.compat.v1.Session() as sess:
    init = tf.compat.v1.global_variables_initializer()
    sess.run(init)
    new_saver = tf.compat.v1.train.import_meta_graph(r'C:\Users\user\Desktop\PV\venv\checkpoint\test_saver-29900.meta')
    new_saver.restore(sess, tf.compat.v1.train.latest_checkpoint(r'C:\Users\user\Desktop\PV\venv\checkpoint'))

    # Test step
    test_predict = sess.run(Y_pred, feed_dict={X: testX})
    rmse_val = sess.run(rmse, feed_dict={targets: testY, predictions: test_predict})
    print("RMSE: {}".format(rmse_val))

Test_pred = pd.DataFrame(test_predict)
TestY = pd.DataFrame(testY)
Train_result = pd.concat([TestY, Test_pred], ignore_index=True, axis=1)
Train_result.columns = ['Train', 'Prediction']
Train_result.to_csv(r'C:\Users\user\Desktop\PV\venv\result\model_result.csv')
