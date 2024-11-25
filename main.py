#!/usr/bin/env python3
from gschedule import Global
from communication import global_server_v2
from communication import site_server

import threading
#########################################################
# resource---------site
# surveyplan-------target

# 暂无 -------------telescope
# 结果 -------------task
#########################################################

# 数据格式转换->全局调度（改后）->SBlock->短期（学姐有）->结果->可视化
def main():
    # 输入
    # n = int(input("n:"))
    # m = int(input("m:"))
    # timeslot = int(input("timeslot:"))

    # # ISO格式的日期字符串
    # start_time = '2022-05-01T00:00:00'
    # end_time = '2022-05-03T00:00:00'
    threading.Thread(target=global_server_v2.start_global_server, args=()).start()
    # threading. Thread(target=site_server.start_site_server, args=()).start()
    
    # global_server.start_server()
    
    # site_server.start_site_server()
    # Global.GBlock(n, m, timeslot, start_time, end_time)



if __name__ == '__main__':
    print('Hello SiTian!')

    main()

