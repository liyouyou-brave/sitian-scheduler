import numpy as np
from matplotlib import pyplot as plt

# 每个台站时间片的成功分配率
def obs_success(n: int, time_used: list, num_of_timeslots: int, path: str):
    for i in range(n):
        time_used[i] = time_used[i] / num_of_timeslots
        # print(list_obs[i].name, time_used[i])
    x = range(n)
    y = time_used
    plt.plot(x, y, 'b*-')
    # plt.legend()  # 显示上面的label
    plt.xlabel('station')
    plt.ylabel('time_used')
    plt.savefig(path)
    plt.show()
    plt.close()


# 每个天区的观测次数
def num_of_obs(list_tar: list, path: str):
    x = [tem_tar.num for tem_tar in list_tar]
    y = [tem_tar.total_timenum for tem_tar in list_tar]
    plt.scatter(x, y)
    # plt.legend()  # 显示上面的label
    plt.xlabel('tar')
    plt.ylabel('num_of_obs')
    plt.savefig(path)
    plt.show()
    plt.close()


# 每个天区airmass方差
def tar_airmass_var(m: int, list_tar: list, path: str):
    airmass = []
    for i in range(m):
        airmass.append(np.var(list_tar[i].am))

    x = range(m)
    y = airmass
    plt.plot(x, y, 'b*-')
    # plt.legend()  # 显示上面的label
    plt.xlabel('tar')
    plt.ylabel('var_airmass')
    plt.savefig(path)
    plt.show()
    plt.close()


# 每个天区airmass平均值
def tar_airmass_mean(m: int, list_tar: list, path: str):
    mean = []
    for i in range(m):
        mean.append(np.mean(list_tar[i].am))

    x = range(m)
    y = mean
    plt.plot(x, y, 'b*-', alpha=0.5, linewidth=1, label='mean_airmass')
    # for a, b in zip(x, y):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=7.5)
    plt.legend()  # 显示上面的label
    plt.xlabel('tar')
    plt.ylabel('mean_airmass')
    plt.savefig(path)
    plt.show()
    plt.close()
