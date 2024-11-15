from gschedule import Global

from communication import global_server
#########################################################
# resource---------site
# surveyplan-------target

# 暂无 -------------telescope
# 结果 -------------task
#########################################################

#####

'''
    Global scheduler server
    Recieve request from main program
    And calculate schedule block 
    Then transfer schedule block to main program through socket
'''


# def global_cal():
#     '''
#         TODO: Call schedule algorithm to calculate the schedule block
#         response = global_schedule()
#     '''
#     time.sleep(3)
#     print("Calculate over!")
    # response = "From TJU\n"
    # # client.send(response.encode("utf-8"))
    # return response
    


####





# 数据格式转换->全局调度（改后）->SBlock->短期（学姐有）->结果->可视化
def main():
    # 输入
    # n = int(input("n:"))
    # m = int(input("m:"))
    # timeslot = int(input("timeslot:"))

    # # ISO格式的日期字符串
    # start_time = '2022-05-01T00:00:00'
    # end_time = '2022-05-03T00:00:00'
    global_server.start_server()
    # Global.GBlock(n, m, timeslot, start_time, end_time)



if __name__ == '__main__':
    print('Hello SiTian!')

    main()

