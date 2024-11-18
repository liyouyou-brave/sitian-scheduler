from datetime import datetime, timedelta
# import pymysql
from gschedule.sblock import Sblock
import mysql.connector
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

def Site(SB: Sblock, directory: str, task_num):
    # 打开数据库连接
    # 主机名、用户名、密码和数据库名
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'rainy',
        password = '@Sql2024',
        database = 'sitian_db'
        )

    # # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql = "INSERT INTO task (task_id, targ_id, site_id, obstime) VALUES (%s, %s, %s, %s)"

    cursor.execute(sql, (task_num, SB.target.num, SB.site.num, 1))
    with open(f"./output/{directory}/site/log.txt", 'a') as file:
        file.write(f"At time {time_after_timeslot(SB.start_time, 0)}, tele={1}, target={SB.target.num}, exp_time={1}")
        file.write("\n")

    cursor.execute(sql, (task_num+1, SB.target.num, SB.site.num, 1))
    with open(f"./output/{directory}/site/log.txt", 'a') as file:
        file.write(f"At time {time_after_timeslot(SB.start_time, 1)}, tele={2}, target={SB.target.num}, exp_time={1}")
        file.write("\n")

    cursor.execute(sql, (task_num+2, SB.target.num, SB.site.num, 1))
    with open(f"./output/{directory}/site/log.txt", 'a') as file:
        file.write(f"At time {time_after_timeslot(SB.start_time, 2)}, tele={3}, target={SB.target.num}, exp_time={1}")
        file.write("\n")

    cursor.execute(sql, (task_num+3, SB.target.num, SB.site.num, 1))
    with open(f"./output/{directory}/site/log.txt", 'a') as file:
        file.write(f"At time {time_after_timeslot(SB.start_time, 3)}, tele={4}, target={SB.target.num}, exp_time={1}")
        file.write("\n")

    cursor.execute(sql, (task_num+4, SB.target.num, SB.site.num, 1))
    with open(f"./output/{directory}/site/log.txt", 'a') as file:
        file.write(f"At time {time_after_timeslot(SB.start_time, 4)}, tele={5}, target={SB.target.num}, exp_time={1}")
        file.write("\n")

    db.commit()
    cursor.close()
    db.close()

