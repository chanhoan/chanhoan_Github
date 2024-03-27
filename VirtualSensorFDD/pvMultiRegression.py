import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import CoolProp as CP


def T_sat(P_dis,P_suc,ref):
    T_c = []
    T_e = []
    for i in range(len(P_dis)):
        T_c.append(CP.CoolProp.PropsSI('T', 'P', P_dis[i] * 100000, 'Q', 0.5, ref) - 273.15)
        T_e.append(CP.CoolProp.PropsSI('T', 'P', P_suc[i] * 100000, 'Q', 0.5, ref) - 273.15)
    return T_c, T_e

tf.compat.v1.disable_eager_execution()

diretory = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\SEER\Data\2021-10-15'
data_list = ['\RTU_Split_vrc.csv']

df_total = pd.DataFrame()
for i in range(len(data_list)):
    data = pd.read_csv(diretory+data_list[i], encoding='euc-kr').dropna(axis=0).reset_index()

    T_sc = data['SC']
    T_sh = data['SH']

    T_sc_rated = 5.783
    T_sh_rated = 5.511
    T_sc_diff = []
    T_sh_diff = []
    y = []
    for i in range(len(data)):
        T_sc_diff.append(T_sc[i]-T_sc_rated)
        T_sh_diff.append(T_sh[i]-T_sh_rated)
    df = pd.DataFrame()
    df['T_sc_diff'] = T_sc_diff
    df['T_sh_diff'] = T_sh_diff
    df['Chrg%'] = data['Chrg%']
    df_total = pd.concat([df_total,df],axis=0)
    print(df_total)
df_total.to_csv('./input.csv')
T_sc_diff = df_total['T_sc_diff']
T_sh_diff = df_total['T_sh_diff']
yd = df_total['Chrg%']

#input data, output data split
x_data = pd.DataFrame(np.column_stack([T_sc_diff,T_sh_diff]))
print(x_data)
y_data = pd.DataFrame(yd)
predict = []

#placeholder
X = tf.compat.v1.placeholder(tf.float32, [None,2])
Y = tf.compat.v1.placeholder(tf.float32,[None,1])

# weight, bias, hypothesis
W = tf.compat.v1.Variable(tf.compat.v1.random_normal([2,1]), name="weight1")
hypothesis = tf.compat.v1.matmul(X,W)

#cost / loss
cost = tf.reduce_mean(tf.square(hypothesis - Y))

#opimizer
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=1e-3)
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
saver = tf.compat.v1.train.Saver()
with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())
    # new_saver = tf.compat.v1.train.import_meta_graph(r'C:\Users\user\Desktop\saver-94200.meta')
    # new_saver.restore(sess, tf.compat.v1.train.latest_checkpoint(r'C:\Users\user\Desktop'))
    for step in range(10000):
        cost_val, W_val, hy_val, _ = sess.run([cost, W, hypothesis, train], feed_dict={X: x_data, Y: y_data})
        if step % 100 == 0:
            print(step, "Cost: ", cost_val, "\nWeights: \n", W_val)
            # saver.save(sess, r'C:\Users\user\Desktop\saver', step)

plt.scatter(y_data,hy_val,c='red')
plt.show()
columns = ['Actual', 'Predict']
result = pd.DataFrame(np.column_stack((yd,hy_val)),columns=columns)
result.to_csv('./VRC.csv',header=True)