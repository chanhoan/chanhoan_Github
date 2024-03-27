import matplotlib.pyplot as plt

unit_3065_step = [5,6,8,10,11,12,13,15,16]

unit_3066_step = [7,13,14,15,21,22]

unit_3067_step = [10,16,18,21,25]

unit_3065_velocity = [0.023666667,0.252666667,0.256111111,0.538333333,0.456666667,0.576663043,0.4512,0.6702,0.839777778]

unit_3066_velocity = [0.357333333,0.419137255,0.48943634,0.541360577,0.532782051,0.909840345]

unit_3067_velocity = [0.425066667,0.527692308,0.53,0.741727273,0.791166667]

fig, ax1 = plt.subplots(3,1,figsize=(12,6))

ax1[0].plot(unit_3065_step,unit_3065_velocity,color='r',marker='o',markersize=10)
ax1[1].plot(unit_3066_step,unit_3066_velocity,color='b',marker='^',markersize=10)
ax1[2].plot(unit_3067_step,unit_3067_velocity,color='g',marker='s',markersize=10)

ax1[0].set_xticks(unit_3065_step)
ax1[1].set_xticks(unit_3066_step)
ax1[2].set_xticks(unit_3067_step)

ax1[0].set_ylabel('Velocity [m/s]')
ax1[1].set_ylabel('Velocity [m/s]')
ax1[2].set_ylabel('Velocity [m/s]')

ax1[2].set_xlabel('Fan step')

ax1[0].text(min(unit_3065_step),max(unit_3065_velocity)-0.1,'velocity = 0.033 x fan step', horizontalalignment='left', color='red')
ax1[1].text(min(unit_3066_step),max(unit_3066_velocity)-0.1,'velocity = 0.0346 x fan step', horizontalalignment='left', color='b')
ax1[2].text(min(unit_3067_step),max(unit_3067_velocity)-0.1,'velocity = 0.0442 x fan step', horizontalalignment='left', color='g')

plt.tight_layout()

plt.show()