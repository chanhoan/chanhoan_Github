import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
import statistics


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: creating directory. ' + directory)


unit = "3069"
target = "Volume"

fig_save = r'C:\Users\user\OneDrive - Chonnam National University\학석사 연계과정\코드\FDD python\samsung\Experiment\probability\Overall\{}'.format(unit)
create_folder(fig_save)

mean1 = 4070
mean2 = 346
mean3 = 234
mean4 = 329
mean5 = 2129
mean6 = 1749
std1 = 222
std2 = 158
std3 = 62
std4 = 88
std5 = 271
std6 = 498

x = np.linspace(-10000, 20000, 100000)

plt.subplots(figsize=(10, 9))
plt.plot(x, norm.pdf(x, mean1, std1), color='k', linewidth=2, label='Nofault')
plt.plot([mean1, mean1], [0, 2], color='k', linestyle='-.', linewidth=2)
plt.plot(x, norm.pdf(x, mean2, std2), color='r', linewidth=2, label='Kitchen towel2')
plt.plot([mean2, mean2], [0, 2], color='r', linestyle='-.', linewidth=2)
plt.plot(x, norm.pdf(x, mean3, std3), color='b', linewidth=2, label='Kitchen towel3')
plt.plot([mean3, mean3], [0, 2], color='b', linestyle='-.', linewidth=2)
plt.plot(x, norm.pdf(x, mean4, std4), color='g', linewidth=2, label='Kitchen towel4')
# plt.plot([mean4, mean4], [0, 2], color='g', linestyle='-.', linewidth=2)
# plt.plot(x, norm.pdf(x, mean5, std5), color='m', linewidth=2, label='Kitchen towel3')
# plt.plot([mean5, mean5], [0, 2], color='m', linestyle='-.', linewidth=2)
# plt.plot(x, norm.pdf(x, mean6, std6), color='c', linewidth=2, label='Kitchen towel4')
# plt.plot([mean6, mean6], [0, 2], color='c', linestyle='-.', linewidth=2)
axes = plt.gca()
axes.set_ylim([0, max(norm.pdf(x, mean3, std3)) + 0.0001])
yticks = axes.get_yticks()
axes.set_yticklabels([round(yticks[i], 5) for i in range(len(yticks))], fontsize=24)
axes.set_xlim([mean1 - 5000, mean1 + 5000])
xticks = axes.get_xticks()
axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
plt.ylabel('Probability', fontsize=26, fontweight='bold')
plt.xlabel('Volume [$m^3/h$]', fontsize=26, fontweight='bold')
plt.tight_layout()
plt.legend(fontsize=16)
# plt.show()
plt.savefig(fig_save+'/{}_{}.png'.format(unit,target))