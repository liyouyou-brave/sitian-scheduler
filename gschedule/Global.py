from datetime import datetime, timedelta
import ephem
from gschedule.SunAlt import calculate_sun_position
from gschedule.AM import get_ZenithAngle, am
from gschedule.Performance import obs_success, num_of_obs, tar_airmass_var, tar_airmass_mean
from gschedule.observer import Observer
from gschedule.target import Target
from gschedule.sblock import Sblock
from sschedule.Site import Site
import numpy as np
import os
# import pymysql

import random
import json


# 全局调度
# n台站
# m天区
# timeslot时间片

# def readin_target_txt(m: int):
#     # surveyplan

#     # 打开数据库连接
#     # 主机名、用户名、密码和数据库名
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='1q2w3e4r',
#                          database='sitian',
#                          port=3306)

#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()

#     sql = "INSERT INTO target (targ_id, ra_targ, dec_targ) VALUES (%s, %s, %s)"

#     # 读文件并建立m个天区
#     with open(f'./input/surveyplan-{m}.txt', 'r') as file:
#         # 去掉第一行
#         lines = file.readlines()[1:]
#         for line in lines:
#             data = line.strip().split()
#             cursor.execute(sql, (data[0], data[1], data[2]))

#     db.commit()
#     cursor.close()
#     db.close()

# def readin_site_txt(n: int):
#     # resource

#     # 打开数据库连接
#     # 主机名、用户名、密码和数据库名
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='1q2w3e4r',
#                          database='sitian',
#                          port=3306)

#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()

#     sql = "INSERT INTO site (site_id, sitename, site_lon, site_lat, site_alt) VALUES (%s, %s, %s, %s, %s)"

#     # 读文件并建立n个台站
#     with open(f'./input/resources-{n}.txt', 'r') as file:
#         # 去掉第一行
#         lines = file.readlines()[1:]
#         for line in lines:
#             data = line.strip().split()
#             cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))

#     db.commit()
#     cursor.close()
#     db.close()

# def get_list_target(m: int):
#     # surveyplan

#     # 天区列表
#     listm = []

#     # 打开数据库连接
#     # 主机名、用户名、密码和数据库名
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='1q2w3e4r',
#                          database='sitian',
#                          port=3306)

#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()

#     sql = "SELECT * FROM target LIMIT %s"
#     cursor.execute(sql, m)
#     results = cursor.fetchall()
#     for row in results:
#         target_tem = Target(int(row[0]), float(row[2]), float(row[3]), -1, 0, 0, 1)
#         listm.append(target_tem)
#         # 打印结果
#         print(target_tem.num, target_tem.ra, target_tem.dec)

#     db.commit()
#     cursor.close()
#     db.close()

#     return listm

# def get_list_observer(n: int):
#     # resource

#     # 台站列表
#     listn = []

#     # 打开数据库连接
#     # 主机名、用户名、密码和数据库名
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='1q2w3e4r',
#                          database='sitian',
#                          port=3306)

#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = db.cursor()

#     sql = "SELECT * FROM site LIMIT %s"
#     cursor.execute(sql, n)
#     results = cursor.fetchall()
#     for row in results:
#         observer_tem = Observer(int(row[0]), str(row[1]), float(row[2]), float(row[3]), float(row[4]))
#         listn.append(observer_tem)
#         # 打印结果
#         print(observer_tem.num, observer_tem.name, observer_tem.ra, observer_tem.dec)

#     db.commit()
#     cursor.close()
#     db.close()

#     return listn


def get_list_target_from_txt(m: int):
    # 天区列表
    listm = []

    # 读文件并建立m个天区
    with open(f'./input/surveyplan-{m}.txt', 'r') as file:
        # 去掉第一行
        lines = file.readlines()[1:]
        for line in lines:
            data = line.strip().split()
            target_tem = Target(int(data[0]), float(data[1]), float(data[2]), -1, 0, int(data[3]), int(data[4]))
            listm.append(target_tem)

    for i in range(m):
        print(listm[i].num, listm[i].ra, listm[i].dec)

    return listm

def get_list_observer_from_txt(n: int):
    # 台站列表
    listn = []

    # 读文件并建立n个台站
    with open(f'./input/resources-{n}.txt', 'r') as file:
        # 去掉第一行
        lines = file.readlines()[1:]
        for line in lines:
            data = line.strip().split()
            observer_tem = Observer(int(data[0]), str(data[1]), float(data[2]), float(data[3]), float(data[4]))
            listn.append(observer_tem)

    for i in range(n):
        print(listn[i].num, listn[i].name, listn[i].ra, listn[i].dec, listn[i].elevation)

    return listn

# 时间推移timeslot的时间
def time_after_timeslot(t_now: str, timeslot: int):
    # 将字符串解析为 datetime 对象
    time_obj = datetime.fromisoformat(t_now)

    # 加上timeslot
    time_after = time_obj + timedelta(minutes=timeslot)

    # 将结果转换回字符串格式
    result_time_str = time_after.isoformat()

    # 输出结果
    return result_time_str

# 两个时间之间的分钟数
def calculate_minutes_between(time_str1: str, time_str2: str):
    # 将时间字符串解析为 datetime 对象
    time_obj1 = datetime.fromisoformat(time_str1)
    time_obj2 = datetime.fromisoformat(time_str2)

    # 计算时间差
    time_difference = abs(time_obj2 - time_obj1)

    # 将时间差转换为分钟
    minutes_difference = time_difference.total_seconds() / 60

    return minutes_difference

def globle_json(now: str, site: Observer, target: Target, timeslot: int):
    '''
    {
        "site_id": xxx,
        "target":
            [
                {
                    "targ_id": xxx,
                    "ra_targ": xxx,
                    "ra_dec": xxx,
                    "mode": "image",
                    "filter": "g",
                    "exptime": 60,
                    "nframe": 1
                },
                {
                    "targ_id": xxx,
                    "ra_targ": xxx,
                    "ra_dec": xxx,
                    "mode": "image",
                    "filter": "g",
                    "exptime": 60,
                    "nframe": 1
                }
            ]
    }
    '''

    if not os.path.exists(f"./output/{now}/global/{site.num}.json"):
        with open(f"./output/{now}/global/{site.num}.json", 'w') as file:
            json.dump({"site_id": site.num,"target":[]}, file, indent=4)


    # 读取JSON文件
    with open(f"./output/{now}/global/{site.num}.json", 'r') as file:
        data = json.load(file)

    # 往第二个键值对数组添加数据
    data['target'].append({
        "targ_id": target.num,
        "ra_targ": target.ra,
        "ra_dec": target.dec,
        "mode": "image",
        "filter": "g",
        "exptime": timeslot,
        "nframe": 1
    })

    # 把修改后的数据写回JSON文件
    with open(f"./output/{now}/global/{site.num}.json", 'w') as file:
        json.dump(data, file, indent=4) # indent缩进


def GBlock(n: int, m: int, timeslot: int, start_time: str, end_time: str):
    # test
    # readin_target_txt(m)
    # readin_site_txt(n)

    # 天区列表
    list_tar = get_list_target_from_txt(m)

    # 台站列表
    list_obs = get_list_observer_from_txt(n)



    # start_time----end_time 有几个时间片
    num_of_timeslots = int(calculate_minutes_between(start_time, end_time)/timeslot)

    # 记录哪个台站在哪个时间片观测哪个天区
    mat = np.zeros((n, num_of_timeslots), dtype = int)
    # 记录哪个台站在哪个时间片观测天区的airmass
    mat_am = np.zeros((n, num_of_timeslots), dtype=float)

    # 当前时间台站S是否有任务，初始化为0
    Sarray = np.zeros(n, dtype=int)

    time_now = start_time

    # 不同台站成功分配出去的时间片数量
    time_used = np.zeros(n, dtype=float)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.mkdir(f"./output/{now}")
    os.mkdir(f"./output/{now}/global")
    os.mkdir(f"./output/{now}/site")

    # 总观测次数
    total_obs_num = 0

    # task总数
    task_num = 1

    # 分配
    while time_now != end_time:
        airmass_min = 1.6
        list_tar.sort(key=lambda x: x.last_time)
        i = -1
        obs_j = -1
        target_i = -1
        while i < m:
            i += 1
            # 没有合适的，推进到下一个时间片。都分配出去了/airmass都过高都没分配出去
            if i == m:
                time_now = time_after_timeslot(time_now, timeslot)
                for k in range(len(Sarray)):
                    Sarray[k] = 0
                break
            # 找与现在分配的天区最适配的台站
            for j in range(n):
                # 该台站有任务
                if Sarray[j] == 1:
                    continue

                dushu_tempor = get_ZenithAngle(list_obs[j], list_tar[i], time_now)
                airmass = am(dushu_tempor)
                sun_alt = calculate_sun_position(list_obs[j], time_now)
                # 质量好，适宜观测
                if airmass < airmass_min and sun_alt < ephem.degrees('-18'):
                    # print(airmass)
                    airmass_min = airmass
                    obs_j = j
                    target_i = i
                else:
                    # ANSI转义代码
                    HIGHLIGHT_START = '\033[1;33m'  # 高亮颜色为黄色，1表示高亮，33m表示前景色
                    HIGHLIGHT_END = '\033[0m'  # 重置样式
                    print(f"airmass{HIGHLIGHT_START}{airmass}{HIGHLIGHT_END}")
                    print(f"sunalt{HIGHLIGHT_START}{sun_alt}{HIGHLIGHT_END}")


            # 表格中记录
            if obs_j != -1 and target_i != -1:
                Sarray[obs_j] = 1
                list_tar[target_i].last_time = int(calculate_minutes_between(start_time, time_now)/timeslot)
                mat[obs_j][list_tar[target_i].last_time] = list_tar[target_i].num
                list_tar[target_i].total_timenum += 1
                total_obs_num += 1
                list_tar[target_i].am.append(airmass_min)
                mat_am[obs_j][list_tar[target_i].last_time] = airmass_min
                with open(f"./output/{now}/global/log.txt", 'a') as file:
                    file.write(f"At time {time_now}, resource={list_obs[obs_j].name}, target={list_tar[target_i].num}, exp_time={timeslot}")
                    file.write("\n")
                globle_json(now, list_obs[obs_j], list_tar[target_i], timeslot)
                time_used[obs_j] += 1

                ############################################################
                SB = Sblock(timeslot, list_tar[target_i], list_obs[obs_j], time_now)
                Site(SB, now, task_num)
                task_num = task_num + 5
                ############################################################

                break
            else:
                continue


    # 结束！
    print("over！")
    print(mat)


    # 打开文件
    with open(f"./output/{now}/global/mat.txt", 'w') as file:
        # 遍历二维数组并写入文件
        for row in mat:
            # 将每行转换为字符串并用空格分隔
            row_str = ' '.join(map(str, row))
            # 写入文件并换行
            file.write(row_str + '\n')

    # 每个台站时间片的成功分配率
    obs_success(n, time_used, num_of_timeslots, f"./output/{now}/global/time_success.png")


    # 每个天区的观测次数
    num_of_obs(list_tar, f"./output/{now}/global/num_of_obs.png")


    # 每个天区airmass方差
    tar_airmass_var(m, list_tar, f"./output/{now}/global/var_airmass.png")

    # 每个天区airmass平均值
    tar_airmass_mean(m, list_tar, f"./output/{now}/global/mean_airmass.png")


