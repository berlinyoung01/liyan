"""
__author__ = 'berlinyoung'
@File   :2-5test.py
@Date   :2024/5/10 21:47
-*- coding: utf-8 -*-
"""
'''
    明确任务：比较共享单车用户类别（会员（订阅Subscriber）、非会员（用户Customer）的平均骑行时间的趋势
'''
import os
import numpy as np
import matplotlib.pyplot as plt


data_path = './data/bikeshare'
# data_filenames = ['2017-q1_trip_history_data.csv','2017-q2_trip_history_data.csv',
#                  '2017-q3_trip_history_data.csv','2017-q4_trip_history_data.csv']
data_filenames = ['201701-citibike-tripdata.csv','201702-citibike-tripdata.csv',
                 '201703-citibike-tripdata.csv']

def collect_and_process_data():
    '''
        Step1+2 : 数据获取，数据处理
    '''
    cln_data_arr_list = []
    for data_filename in data_filenames:
        data_file = os.path.join(data_path, data_filename)
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)

        # 去掉双引号
        cln_data_arr = np.core.defchararray.replace(data_arr, '"', '')
        cln_data_arr_list.append(cln_data_arr)

    return cln_data_arr_list

def get_mean_duration_by_type(data_arr_list, member_type):
    """
        Step3 : 数据分析
    """
    mean_duration_list = []
    for data_arr in data_arr_list:
        bool_arr = data_arr[:,-3] == member_type
        filtered_arr = data_arr[bool_arr]

        mean_duration = np.mean(filtered_arr[:,0].astype('float') / 60)
        mean_duration_list.append(mean_duration)

    return mean_duration_list

def save_and_show_results(member_mean_duration_list, casual_mean_duration_list):
    """
        Step4 : 结果展示

        # 第57行，遍历所有的月份，为了更兼容些直接取循环列表的长度
    """
    # 1. 信息输出
    for idx in range(len(member_mean_duration_list)):
        member_mean_duration = member_mean_duration_list[idx]
        casual_mean_duration = casual_mean_duration_list[idx]
        print('第{}个季度，会员平均骑行时长：{:.2f}分钟，非会员平均骑行时长：{:.2f}分钟。'.format(
            idx + 1, member_mean_duration, casual_mean_duration))

    # 2. 分析结果保存
    # 构造多维数组，np.array方法需要调试看结果是生成怎样的数组，通过调试看文件可以看出默认2行4列，通过transpose转成4行2列
    mean_duration_arr = np.array([member_mean_duration_list, casual_mean_duration_list]).transpose()
    # fmt指定格式，不然默认是科学技术法显示值。comment需要初始化，默认开头带个#
    np.savetxt('./mean_duration.csv',mean_duration_arr, delimiter=',',
               header='Subscriber Mean Duration, Customer Mean Duration', fmt='%.4f',
               comments='')

    #3. 可视化结果保存，plt.figure生成空的画布，plt.plot生成折线图，
    plt.figure()
    plt.plot(member_mean_duration_list, color='g', linestyle='-', marker='o', label='Subscriber')
    plt.plot(casual_mean_duration_list, color='r', linestyle='--', marker='*', label='Customer')
    plt.title('Subscriber vs Customer')
    # plt.xticks(range(0,4), ['1st','2nd','3rd','4th'], rotation=45)
    # 在X轴上给出刻度用来代表X轴上的值，rotation是旋转45度
    plt.xticks(range(0, 3), ['1st', '2nd', '3rd'], rotation=45)
    # X轴是我们的月份/季度，给的值为月份Month/季度Quarter
    plt.xlabel('Quarter')
    # Y轴是我们的均值，单位min
    plt.ylabel('Mean duration (min)')
    # 指定个图例，location给个best就会自动放在自适应的位置上
    plt.legend(loc='best')
    # 由于部分被遮盖住，plt.tight_layout() 紧凑型去布局输出
    plt.tight_layout()

    # 需要放在plt.show之前保存，不然会保存一个空的图片
    plt.savefig('./duration_trend.png')
    plt.show()

def main():
    '''
        主函数
    '''
    # 数据获取 + 数据处理
    cln_data_arr_list = collect_and_process_data()

    # 数据分析
    # 会员数据分析
    member_mean_duration_list = get_mean_duration_by_type(cln_data_arr_list, 'Subscriber')
    # 非会员数据分析
    casual_mean_duration_list = get_mean_duration_by_type(cln_data_arr_list, 'Customer')

    save_and_show_results(member_mean_duration_list, casual_mean_duration_list)


if __name__ == '__main__':
    main()