import tensorflow as tf
import pandas as pd
import numpy as np

tf.compat.v1.disable_eager_execution()

#import data
data_ = pd.read_csv(r'C:\Users\user\Desktop\PV\venv\test1data.csv', delimiter=",")
data_ = data_.set_index(['Date/Time'])

#input data, output data split
x_data = data_[['Environment:Site Outdoor Air Relative Humidity [%](TimeStep)',
                 'Environment:Site Outdoor Air Drybulb Temperature [C](TimeStep)',
                 'Environment:Site Direct Solar Radiation Rate per Area [W/m2](TimeStep)',
                 'Environment:Site Solar Azimuth Angle [deg](TimeStep)',
                 'Environment:Site Solar Altitude Angle [deg](TimeStep)',
                 'Environment:Site Solar Hour Angle [deg](TimeStep)',
                 'PV:ZN_1:Generator PV Cell Temperature [C](TimeStep)',
                 'Environment:Site Rain Status [](TimeStep)']].values.tolist()
y_data = data_['PV:ZN_1:Generator Produced DC Electric Power [W](TimeStep)'].values.tolist()
y_data = np.array([y_data]).reshape([14400,1])
print(type(y_data))

#Normalize
def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)

# x_data = MinMaxScaler(x_data)
# y_data = MinMaxScaler(y_data)

#placeholder
X = tf.compat.v1.placeholder(tf.float32, shape=[None, 8])
Y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])

# weight, bias, hypothesis
W = tf.compat.v1.Variable(tf.compat.v1.random_normal([8,1]), name="weight1")
b = tf.compat.v1.Variable(tf.compat.v1.random_normal([1]), name="bias")
hypothesis = tf.compat.v1.matmul(X, W) + b

#cost / loss
cost = tf.reduce_mean(tf.square(hypothesis - Y))
#opimizer
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=1e-6)
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()

sess.run(tf.compat.v1.global_variables_initializer())

for step in range(1000000):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train], feed_dict={X: x_data, Y: y_data})

    if step % 100 == 0:
        print(step, "Cost: ", cost_val, "\nPrediction:\n", hy_val)


print('{}'.format(hy_val))