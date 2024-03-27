import matplotlib.pyplot as plt

a = [1,2,3,4,5]
b = [1,2,3,4,5]
c = [2,3,4,5,6]
d = [2,3,4,5,6]
fig,ax1=plt.subplots()

ax1.plot(a,b,color='b',label='Air outlet temperature (200 Mesh 4)')
# ax1.plot(a,b,color='c',linestyle='--',label='Fan step (No fault)')
# ax1.plot(a,b,color='g',label='Air outlet temperature (Fault type 2)')
ax1.plot(a,b,color='gray',linestyle='--',label='200 Mesh 4 - Power')
# ax1.plot(a,b,color='r',label='Fault')
# ax1.plot(a,b,color='m',linestyle='--',label='Fan step (Fault type 2)')

plt.legend(bbox_to_anchor=[0, 0],ncol=2)
plt.tight_layout()
plt.show()