import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd


def solve(m1, m2, std1, std2):
    aa = 1 / (2 * std1 ** 2) - 1 / (2 * std2 ** 2)
    b = m2 / (std2 ** 2) - m1 / (std1 ** 2)
    cc = m1 ** 2 / (2 * std1 ** 2) - m2 ** 2 / (2 * std2 ** 2) - np.log(std2 / std1)
    print(aa, b, cc)
    print(np.roots([aa, b, cc]))
    return np.roots([aa, b, cc])


normal_mean = 31.9
normal_std = 1.7386663455358611

fault_mean1 = 1.4
fault_std1 = 1.7386663455358611

line_x = np.linspace(-100, 200, 10000)

result1 = solve(normal_mean, fault_mean1, normal_std, fault_std1)


def airflow_sensor_prediction(x, mean_base, std_base, mean_fault, std_fault, result1,):
    plt.subplots(figsize=(10, 9))

    plt.plot(x, norm.pdf(x, mean_fault, std_fault), color='r', linewidth=2)
    # plt.plot(x, norm.pdf(x, mean_fault2, std_fault2), color='g', linewidth=2)
    # plt.plot(x, norm.pdf(x, mean_fault3, std_fault3), color='b', linewidth=2)
    # plt.plot(x, norm.pdf(x, mean_fault4, std_fault4), color='c', linewidth=2)
    # plt.plot(x, norm.pdf(x, mean_fault5, std_fault5), color='m', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_base, std_base), color='k', linewidth=2)

    plt.plot([mean_fault, mean_fault], [0, 2], color='r', linestyle='-.', linewidth=2)
    # plt.plot([mean_fault2, mean_fault2], [0, 2], color='g', linestyle='-.', linewidth=2)
    # plt.plot([mean_fault3, mean_fault3], [0, 2], color='b', linestyle='-.', linewidth=2)
    # plt.plot([mean_fault4, mean_fault4], [0, 2], color='c', linestyle='-.', linewidth=2)
    # plt.plot([mean_fault5, mean_fault5], [0, 2], color='m', linestyle='-.', linewidth=2)
    plt.plot([mean_base, mean_base], [0, 2], color='k', linestyle='-.', linewidth=2)

    r1 = result1[0]
    # r2 = result2[0]
    # r3 = result3[0]
    # r4 = result4[0]
    # r5 = result5[0]

    plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], mean_base, std_base), color='red', alpha=0.3)
    plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], mean_fault, std_fault), color='red', alpha=0.3)
    area1 = 1-norm.cdf(r1, mean_fault, std_fault) + (norm.cdf(r1, mean_base, std_base))
    # plt.fill_between(x[x < r2], 0, norm.pdf(x[x < r2], mean_base, std_base), color='g', alpha=0.3)
    # plt.fill_between(x[x > r2], 0, norm.pdf(x[x > r2], mean_fault2, std_fault2), color='g', alpha=0.3)
    # area2 = 1-norm.cdf(r2, mean_fault2, std_fault2) + (norm.cdf(r2, mean_base, std_base))
    # plt.fill_between(x[x < r3], 0, norm.pdf(x[x < r3], mean_base, std_base), color='b', alpha=0.3)
    # plt.fill_between(x[x > r3], 0, norm.pdf(x[x > r3], mean_fault3, std_fault3), color='b', alpha=0.3)
    # area3 = 1-norm.cdf(r3, mean_fault3, std_fault3) + (norm.cdf(r3, mean_base, std_base))
    # plt.fill_between(x[x < r4], 0, norm.pdf(x[x < r4], mean_base, std_base), color='c', alpha=0.3)
    # plt.fill_between(x[x > r4], 0, norm.pdf(x[x > r4], mean_fault4, std_fault4), color='c', alpha=0.3)
    # area4 = 1-norm.cdf(r4, mean_fault4, std_fault4) + (norm.cdf(r4, mean_base, std_base))
    # plt.fill_between(x[x < r5], 0, norm.pdf(x[x < r5], mean_base, std_base), color='m', alpha=0.3)
    # plt.fill_between(x[x > r5], 0, norm.pdf(x[x > r5], mean_fault5, std_fault5), color='m', alpha=0.3)
    # area5 = 1-norm.cdf(r5, mean_fault5, std_fault5) + (norm.cdf(r5, mean_base, std_base))

    # else:
    #     plt.fill_between(x[x > r], 0, norm.pdf(x[x > r], mean_base, std_base), color='red', alpha=0.3)
    #     plt.fill_between(x[x < r], 0, norm.pdf(x[x < r], mean_fault, std_fault), color='red', alpha=0.3)
    #     area = norm.cdf(r, mean_fault, std_fault) + 1 - (norm.cdf(r, mean_base, std_base))

    area1 = float("{0:.2f}".format(area1))
    # area2 = float("{0:.2f}".format(area2))
    # area3 = float("{0:.2f}".format(area3))
    # area4 = float("{0:.2f}".format(area4))
    # area5 = float("{0:.2f}".format(area5))
    print("Normal distribution area under curves ", area1)
    # print("Normal distribution area under curves ", area2)
    # print("Normal distribution area under curves ", area3)
    # print("Normal distribution area under curves ", area4)
    # print("Normal distribution area under curves ", area5)

    axes = plt.gca()
    axes.set_ylim([0, max(norm.pdf(x, normal_mean, normal_std)) + 0.05])
    yticks = axes.get_yticks()
    axes.set_yticklabels([round(yticks[i], 2) for i in range(len(yticks))], fontsize=24)
    axes.set_xlim([normal_mean - 40, normal_mean + 10])
    xticks = axes.get_xticks()
    axes.set_xticklabels([xticks[i] for i in range(len(xticks))], fontsize=24)
    plt.ylabel('Probability', fontsize=26, fontweight='bold')
    plt.xlabel('Airflow [kg/s]', fontsize=26, fontweight='bold')
    axes.text(1, 0.95, 'Fault type 2 area under curves: {}'.format(area1), horizontalalignment='right',transform=axes.transAxes, fontsize=22, color='k', fontdict={'weight': 'bold'})
    # axes.text(1, 0.9, '200 Mesh area under curves: {}'.format(area2), horizontalalignment='right', transform=axes.transAxes,fontsize=12, color='g')
    # axes.text(1, 0.85, 'Towel 4 area under curves: {}'.format(area3), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='b')
    # axes.text(1, 0.8, 'Towel 3 area under curves: {}'.format(area4), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='c')
    # axes.text(1, 0.75, 'Towel 2 area under curves: {}'.format(area5), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='m')
    plt.legend(['[No fault - 01/17]','[Fault type 2 - 01/19 ]'],ncol=3, loc='center',fontsize=22, bbox_to_anchor=(0.5, -0.15))
    plt.tight_layout()
    plt.show()
    # return fig.savefig('./SAT.png', bbox_extra_artists=(legend,), bbox_inches='tight')


airflow_sensor_prediction(line_x,normal_mean,normal_std,fault_mean1,fault_std1,result1)


def airflow_sensor_fault_level(x, mean_base, std_base, mean_fault, std_fault, mean_fault2, std_fault2, mean_fault3, std_fault3, mean_fault4, std_fault4, mean_fault5, std_fault5, result1, result2, result3, result4, result5):
    plt.subplots(figsize=(8, 7))
    plt.title('Fault level', fontsize=24, fontweight='bold')

    plt.plot(x, norm.pdf(x, mean_fault, std_fault), color='r', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_fault2, std_fault2), color='g', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_fault3, std_fault3), color='b', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_fault4, std_fault4), color='c', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_fault5, std_fault5), color='m', linewidth=2)
    plt.plot(x, norm.pdf(x, mean_base, std_base), color='k', linewidth=2)

    plt.plot([mean_fault, mean_fault], [0, 2], color='r', linestyle='-.', linewidth=2)
    plt.plot([mean_fault2, mean_fault2], [0, 2], color='g', linestyle='-.', linewidth=2)
    plt.plot([mean_fault3, mean_fault3], [0, 2], color='b', linestyle='-.', linewidth=2)
    plt.plot([mean_fault4, mean_fault4], [0, 2], color='c', linestyle='-.', linewidth=2)
    plt.plot([mean_fault5, mean_fault5], [0, 2], color='m', linestyle='-.', linewidth=2)
    plt.plot([mean_base, mean_base], [0, 2], color='k', linestyle='-.', linewidth=2)

    r1 = result1[0]
    r2 = result2[0]
    r3 = result2[0]
    r4 = result2[0]
    r5 = result2[0]

    plt.fill_between(x[x > r1], 0, norm.pdf(x[x > r1], mean_base, std_base), color='r', alpha=0.3)
    plt.fill_between(x[x < r1], 0, norm.pdf(x[x < r1], mean_fault, std_fault), color='r', alpha=0.3)
    area1 = norm.cdf(r1, mean_fault, std_fault) + 1-(norm.cdf(r1, mean_base, std_base))
    plt.fill_between(x[x > r2], 0, norm.pdf(x[x > r2], mean_base, std_base), color='g', alpha=0.3)
    plt.fill_between(x[x < r2], 0, norm.pdf(x[x < r2], mean_fault2, std_fault2), color='g', alpha=0.3)
    area2 = norm.cdf(r2, mean_fault2, std_fault2) + 1-(norm.cdf(r2, mean_base, std_base))
    plt.fill_between(x[x > r3], 0, norm.pdf(x[x > r3], mean_base, std_base), color='b', alpha=0.3)
    plt.fill_between(x[x < r3], 0, norm.pdf(x[x < r3], mean_fault3, std_fault3), color='b', alpha=0.3)
    area3 = norm.cdf(r3, mean_fault3, std_fault3) + 1 - (norm.cdf(r2, mean_base, std_base))
    plt.fill_between(x[x > r4], 0, norm.pdf(x[x > r4], mean_base, std_base), color='c', alpha=0.3)
    plt.fill_between(x[x < r4], 0, norm.pdf(x[x < r4], mean_fault4, std_fault4), color='c', alpha=0.3)
    area4 = norm.cdf(r4, mean_fault4, std_fault4) + 1 - (norm.cdf(r4, mean_base, std_base))
    plt.fill_between(x[x > r5], 0, norm.pdf(x[x > r5], mean_base, std_base), color='m', alpha=0.3)
    plt.fill_between(x[x < r5], 0, norm.pdf(x[x < r5], mean_fault5, std_fault5), color='m', alpha=0.3)
    area5 = norm.cdf(r5, mean_fault5, std_fault5) + 1 - (norm.cdf(r5, mean_base, std_base))
    # else:
    #     plt.fill_between(x[x > r], 0, norm.pdf(x[x > r], mean_base, std_base), color='red', alpha=0.3)
    #     plt.fill_between(x[x < r], 0, norm.pdf(x[x < r], mean_fault, std_fault), color='red', alpha=0.3)
    #     area = norm.cdf(r, mean_fault, std_fault) + 1 - (norm.cdf(r, mean_base, std_base))

    area1 = float("{0:.2f}".format(area1))
    area2 = float("{0:.2f}".format(area2))
    area3 = float("{0:.2f}".format(area3))
    area4 = float("{0:.2f}".format(area4))
    area5 = float("{0:.2f}".format(area5))

    print("Normal distribution area under curves ", area1)
    print("Normal distribution area under curves ", area2)
    print("Normal distribution area under curves ", area3)
    print("Normal distribution area under curves ", area4)
    print("Normal distribution area under curves ", area5)

    axes = plt.gca()
    axes.set_ylim([0, 0.2])
    axes.set_xlim([mean_base - 20, mean_base + 100])
    plt.ylabel('Probability', fontsize=14, fontweight='bold')
    plt.xlabel('Fault level [%]', fontsize=14, fontweight='bold')
    axes.text(1, 0.95, '40 Mesh area under curves: {}'.format(area1), horizontalalignment='right', transform=axes.transAxes,fontsize=12, color='r')
    axes.text(1, 0.9, '200 Mesh area under curves: {}'.format(area2), horizontalalignment='right', transform=axes.transAxes,fontsize=12, color='g')
    axes.text(1, 0.85, 'Towel 4 area under curves: {}'.format(area3), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='b')
    axes.text(1, 0.8, 'Towel 3 area under curves: {}'.format(area4), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='c')
    axes.text(1, 0.75, 'Towel 2 area under curves: {}'.format(area5), horizontalalignment='right',transform=axes.transAxes, fontsize=12, color='m')
    plt.legend(['[40 Mesh - 07/29]','[200 Mesh - 08/10]','[Towel 4 - 07/30]','[Towel 3 - 08/04]','[Towel 2 - 08/05]','[Normal - 07/28]'],ncol=3, loc='center',fontsize=12, bbox_to_anchor=(0.5, -0.15))
    plt.tight_layout()
    plt.show()
    # return fig.savefig('./SAT.png', bbox_extra_artists=(legend,), bbox_inches='tight')


# airflow_sensor_fault_level(line_x,normal_mean,normal_std,fault_mean1,fault_std1,result1)