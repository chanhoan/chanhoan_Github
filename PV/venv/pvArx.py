import pandas as pd
from math import sin, cos, pi
import numpy as np
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.8)

class NARXnetwork():
    def __init__(self):
        self.data_ = pd.read_csv(r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\PV python\PV\venv\merged_202008~202012.csv', delimiter=",").set_index(['time'])
        self.daymin = 144 # 1 day / 5 min
        self.temp = np.array(self.data_['temp']).reshape(-1, 1)
        self.ii = np.array(self.data_['ii']).reshape(-1, 1)
        self.hi = np.array(self.data_['hi']).reshape(-1, 1)
        self.at = np.array(self.data_['at']).reshape(-1, 1)
        self.st = np.array(self.data_['st']).reshape(-1, 1)
        self.hum = np.array(self.data_['hum']).reshape(-1, 1)
        self.pv_power_output = np.array(self.data_['power']).reshape(-1, 1)

        #NARX parameter
        self.past = 144
        self.input_dim = self.past*2
        self.checkpoint_path = "./checkpotint/arx_ckpt.ckpt"
        self.model_path = "./checkpoint/arxmodel.h5"
        self.scaler = MinMaxScaler()

    def build_input_dataset(self):
        temp = self.temp
        ii = self.ii
        hi = self.hi
        at = self.at
        st = self.st
        hum = self.hum
        self.xdata = np.column_stack([temp,ii,hi,at,st,hum])
        return self.xdata

    def build_output_dataset(self):
        self.ydata = []
        self.ydata.extend(self.pv_power_output)
        self.ydata = np.array(self.ydata)
        return self.ydata

    def form_data(self,input_seq,output_seq,past):
        data_len = np.max(input_seq.shape)
        X = np.zeros(shape=(data_len-past,2*past))
        Y = np.zeros(shape=(data_len-past,))
        for i in range(0,data_len-past):
            X[i,:past] = input_seq[i:i+past,0]
            X[i,past:] = output_seq[i:i+past,0]
            Y[i] = output_seq[i+past,0]
        return X, Y

    def build_set(self):
        print(self.build_input_dataset())
        print(self.build_output_dataset())
        self.X_, self.Y_ = self.form_data(self.build_input_dataset(), self.build_output_dataset(), self.past)
        self.train_size = int(len(self.X_) * 0.5)
        self.valid_size = int(len(self.X_) * 0.2)
        self.train_set_X = np.array(self.X_[0:self.train_size])
        self.train_set_Y = np.array(self.Y_[0:self.train_size]).reshape(-1, 1)
        self.test_set_X = np.array(self.X_[self.train_size + self.valid_size:])
        self.test_set_Y = np.array(self.Y_[self.train_size + self.valid_size:]).reshape(-1, 1)
        self.valid_set_X = np.array(self.X_[self.train_size:self.train_size + self.valid_size])
        self.valid_set_Y = np.array(self.Y_[self.train_size:self.train_size + self.valid_size]).reshape(-1, 1)
        return self.train_set_X,self.train_set_Y,self.valid_set_X,self.valid_set_Y,self.test_set_X,self.test_set_Y

    def ARX(self):
        self.train_set_X, self.train_set_Y, self.valid_set_X, self.valid_set_Y, self.test_set_X, self.test_set_Y = self.build_set()
        inputs = tf.keras.Input(shape=(self.input_dim,))
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(inputs)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.relu)(x)
        x = layers.Dense(self.input_dim, activation=tf.keras.activations.linear)(x)
        prediction = layers.Dense(1)(x)
        self.model = tf.keras.Model(inputs=inputs,outputs=prediction)
        self.model.compile(optimizer=tf.keras.optimizers.Adam(0.00001),loss=tf.keras.losses.mean_squared_error)
        self.model.summary()
        self.history = self.model.fit(self.train_set_X,self.train_set_Y,epochs=1000,batch_size=1,verbose=1,
                                      validation_data=(self.valid_set_X,self.valid_set_Y))
        self.model.save('arxmodel.h5')
        self.prediction = self.model.predict(self.test_set_X,verbose=1)

        # self.plt_prediction = self.scaler.inverse_transform(self.prediction)
        self.actual = pd.DataFrame(self.test_set_Y)
        self.prediction = pd.DataFrame(self.prediction)
        result = pd.concat([self.actual, self.prediction], ignore_index=True, axis=1)
        result.columns = ['Train', 'Prediction']
        result.to_csv('./result.csv')
        return self.test_set_Y, self.prediction

    def call_model(self):
        self.train_set_X, self.train_set_Y, self.valid_set_X, self.valid_set_Y, self.test_set_X, self.test_set_Y = self.build_set()
        self.new_model = tf.keras.models.load_model('arxmodel.h5')
        self.new_model.summary()
        self.prediction = self.new_model.predict(self.test_set_X,verbose=1)
        self.result = pd.DataFrame(self.prediction).to_csv('arxresult23.csv')
        return self.test_set_Y, self.prediction

    def show_graph(self):
        self.test_set_Y, self.prediction = self.ARX()
        plt.figure()
        plt.plot(self.test_set_Y,'b',label='Real output')
        plt.plot(self.prediction,'r',label='Predicted ouput')
        plt.xlabel('timestep')
        plt.ylabel('pv power')
        plt.legend()
        plt.savefig('arxresult.png')
        plt.show()

arxmodel = NARXnetwork()
call_model = arxmodel.show_graph()