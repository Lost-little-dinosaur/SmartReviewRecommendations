import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt
import pickle
import os
from scipy.optimize import curve_fit
import math
import scipy.stats as stats

dirPath_SAQSD = '../GetData/SeveralAnswerQuestionSetDict/'
dirPath_All_Correct_rate = '../GetData/AllQuestionsCorrectRate/'
dirpath_Allusers_Answers = '../GetData/AllUsersAnswers/'

with open(dirPath_SAQSD + 'SeveralAnswerQuestionSetDict.pkl', 'rb') as f1:
    AllAnswerData_1 = pickle.load(f1)

# 将所有用户的答题记录读入到AllAnswers中，此为字典结构
with open(dirPath_SAQSD + 'SeveralAnswerQuestionSetDict.pkl', 'rb') as f1:
    AllAnswerData = pickle.load(f1)

# 将所有的题目正确率读入AllCorrectRate中
files = os.listdir(dirPath_All_Correct_rate)
AllCorrectRate = {}
for file in files:
    with open(dirPath_All_Correct_rate + file, 'rb') as f1:
        CorrectRate = pickle.load(f1)
        AllCorrectRate.update(CorrectRate)

intervals = [(0, 5), (5, 20), (20, 60), (60, 540), (540, 1440), (1440, 8640), (8640, 44640)]

intervals_list = [5, 20, 60, 540, 1440, 8640, 44640]

# 调用函数，返回时间间隔的分钟数列表
# intervals = get_time_intervals_in_minutes()

max_interval = 44640


def discretize_data(data, intervals):
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                # check if current data is a list and has length of 2i+4
                if isinstance(data[i][j][k], list) and len(data[i][j][k]) == 2 * i + 4:
                    # get the time intervals
                    time_intervals = data[i][j][k][i + 2:-1]
                    # discretize the time intervals
                    time_intervals_discretized = []
                    for t in time_intervals:
                        if t >= 0 and t <= 5:
                            time_intervals_discretized.append(5)
                        elif t > intervals[-1][1]:
                            time_intervals_discretized.append(44640)
                        elif t < 0:
                            time_intervals_discretized.append(0)
                        else:
                            time_intervals_discretized.append(
                                intervals[np.digitize(t, [interval[1] for interval in intervals])][0])
                    # update the data
                    data[i][j][k][i + 2:-1] = time_intervals_discretized
    return data


np.set_printoptions(threshold=np.inf)


# 构造转换权值函数 将1-正确率存放在newRate中
def subtract_from_one(data):
    # 将字典的值转换为 NumPy 数组
    values = np.array(list(data.values()))

    # 计算 1 减去第一个元素
    new_first_element = 1 - values[:, 0]

    # 将新值赋给第一个元素
    values[:, 0] = new_first_element

    # 重新构建字典
    new_data = {key: values[i].tolist() for i, key in enumerate(data.keys())}

    return new_data


newRate = subtract_from_one(AllCorrectRate)
# 将dict转化成list，此时所有次数2-26次的答案都保存在了AllAnswerData1中了

AllAnswerData1 = []

for key in AllAnswerData_1.keys():
    AllAnswerData1.append(AllAnswerData_1[key])

tempAllAnswerData1 = []

for eachList in AllAnswerData1:
    tempList = []
    for eachDict in eachList:
        if list(eachDict.keys())[0] in AllCorrectRate:
            tempList.append(eachDict)
    tempAllAnswerData1.append(tempList)

for i in range(len(tempAllAnswerData1)):
    for j in range(len(tempAllAnswerData1[i])):
        key = list(tempAllAnswerData1[i][j].keys())[0]
        tempAllAnswerData1[i][j][key].append(newRate[key][0])

# 将列表所有答案中的正确的转化成其正确率，错误的还为0,存储在tempAllAnswerData1中
for i in range(len(tempAllAnswerData1)):
    for j in tempAllAnswerData1[i]:
        # j[list(j.keys())[0]].append(newRate[list(j.keys())[0]][0])
        for k in range(i + 2):
            if j[list(j.keys())[0]][k] == 1:
                if list(j.keys())[0] in newRate.keys():
                    j[list(j.keys())[0]][k] = \
                        newRate[list(j.keys())[0]][0]

# 构造AllAnswerData3存放所有的答题记录的列表values值
levels = len(tempAllAnswerData1)
AllAnswerData3 = [[] for i in range(levels)]

for i in range(len(tempAllAnswerData1)):
    for j in tempAllAnswerData1[i]:
        AllAnswerData3[i].append(j[list(j.keys())[0]])


# 构造AllAnswerData4存放所有的分类完成后的values列表
def fenlei_list():
    levels1 = len(AllAnswerData3)
    AllAnswerData4 = [[] for i in range(levels1)]
    for i in range(levels1):
        AllAnswerData4[i] = [[] for j in range(i + 2)]
    return AllAnswerData4


# 将答题记录再按照错误次数进行分类，并保存
def fenlei_answers(answers, answers_fenlei):
    levels1 = len(answers)
    for i in range(levels1):
        mynum = i + 1
        for j in answers[i]:
            zero_num = 0
            # print(j)
            for k in range(mynum):
                # print(j[k])
                if j[k] == 0:
                    zero_num += 1
            if zero_num > mynum:
                zero_num = mynum
            answers_fenlei[i][zero_num].append(j)
        # answers_fenlei = np.array(answers_fenlei)
    # else:  # 如果j有多行，遍历每一行判断前两列是否存在0
    # for row in j:
    #     if 0 in row[:i + 3]:
    #         zero_exist = True
    #         zero_num = zero_num + 1
    #     AllAnswerData4.append(row)


# if __name__ == 'main':
AllAnswerData4 = fenlei_list()
# print(AllAnswerData4)
fenlei_answers(AllAnswerData3, AllAnswerData4)  # 运行该函数将AllAnswerData3数据分类后存入AllAnswerData4中

AllAnswerData4 = discretize_data(AllAnswerData4, intervals)


def processdata(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                # check if current data is a list and has length of 2i+4
                if isinstance(data[i][j][k], list) and len(data[i][j][k]) == 2 * i + 4:
                    data[i][j][k] = [data[i][j][k][i + 1], data[i][j][k][-2], data[i][j][k][-1]]
    return data


# 将答题正确与否的结果与最后一次答本题的时间间隔单独分离出来形成列表
AllAnswerData4 = processdata(AllAnswerData4)


def Get_result(data):
    result = []
    for i in range(len(data)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append([])
        result.append(sublist)
    for i in range(len(data)):
        # print(i)
        for j in range(len(data[i])):
            # print(j)
            for k in range(len(data[i][j])):
                sum_dict = {}
                key = data[i][j][k][1]
                if key not in sum_dict:
                    sum_dict[key] = [0, 0]  # 初始化
                sum_dict[key][0] = data[i][j][k][0]
                sum_dict[key][1] = data[i][j][k][2]
                result[i][j].append(sum_dict)
    return result


# for i in range(len(AllAnswerData4)):
#     for j in range(len(AllAnswerData4[i])):
#
result = Get_result(AllAnswerData4)


def cacu_num(result1):
    key_dict_list = []
    for i in range(len(result1)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append(
                {0: 0, 5: 0, 20: 0, 60: 0, 540: 0, 1440: 0, 8640: 0,
                 44640: 0})
        key_dict_list.append(sublist)
    for i in range(len(result1)):
        # print(len(result1), len(result2))
        for j in range(len(result1[i])):
            # print(len(result1[i]), len(result2[i]))
            for k in range(len(result1[i][j])):
                key = next(iter(result1[i][j][k].keys()))
                key_dict_list[i][j][key] += 1
    return key_dict_list


key_dict = cacu_num(result)


def my_correct_rate(result1, key_dict):
    result2 = []
    for i in range(len(tempAllAnswerData1)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append(
                [{0: [0, 0], 5: [0, 0], 20: [0, 0], 60: [0, 0], 540: [0, 0], 1440: [0, 0], 8640: [0, 0],
                  44640: [0, 0]}])
        result2.append(sublist)
    for i in range(len(result1)):
        # print(len(result1), len(result2))
        for j in range(len(result1[i])):
            # print(len(result1[i]), len(result2[i]))
            for h in range(len(result2[i][j])):
                keys_list = list(result2[i][j][h].keys())
                for k in range(len(result1[i][j])):
                    if len(result1[i][j]) >= 100:
                        key = next(iter(result1[i][j][k].keys()))
                        for key1 in keys_list:
                            # 此处为阈值，可以调节，目前是100个以上的点才会参与后续的计算
                            if key1 == key and key_dict[i][j][key] >= 10:
                                result2[i][j][h][key1][0] = result2[i][j][h][key1][0] + result1[i][j][k][key][0]
                                result2[i][j][h][key1][1] = result2[i][j][h][key1][1] + result1[i][j][k][key][1]
                            else:
                                continue
                # print(result2[i][j][h])
    return result2


my_cor_data = my_correct_rate(result, key_dict)


def fun_correc_rate(corr_data):
    my_corr_rate = []
    for i in range(len(corr_data)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append([{5: [], 20: [], 60: [], 540: [], 1440: [], 8640: [], 44640: []}])
        my_corr_rate.append(sublist)
    for i in range(len(corr_data)):
        for j in range(len(corr_data[i])):
            for k in range(len(corr_data[i][j])):
                keys_list = list(corr_data[i][j][k].keys())
                for key in keys_list:
                    if corr_data[i][j][k][key] and corr_data[i][j][k][key][1]:
                        my_corr_rate[i][j][k][key] = corr_data[i][j][k][key][0] / corr_data[i][j][k][key][1]
    return my_corr_rate


my_cor_rate = fun_correc_rate(my_cor_data)


def Fitring_curves(corr_rates, intervals_list):
    e = math.e

    def func(x, a, b, c):
        return (e ** (a * x + b) + c)

    my_curves_para = []
    for i in range(len(corr_rates)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append([])
        my_curves_para.append(sublist)
    my_curves_x_list = []
    for i in range(len(corr_rates)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append([])
        my_curves_x_list.append(sublist)
    my_curves_y_list = []
    for i in range(len(corr_rates)):
        sublist = []
        k = i + 2
        for j in range(k):
            sublist.append([])
        my_curves_y_list.append(sublist)
    for i in range(len(corr_rates)):
        for j in range(len(corr_rates[i])):
            # print(type(corr_rates[i][j][0].values()))
            time_stamp_list = list(corr_rates[i][j][0].keys())
            values_list = list(corr_rates[i][j][0].values())
            # empty_indices = [i for i, sublst in enumerate(values_list) if not sublst]
            # # 如果空子列表的个数 <= 1，则删除该空子列表
            # new_list = [sublst for i, sublst in enumerate(values_list) if i not in empty_indices]
            empty_indices = [i for i, sublst in enumerate(values_list) if not sublst]
            # 如果空子列表的个数 <= 1，则删除该空子列表，并记录保留下来的子列表在源列表中的位置
            new_lst = [sublst for i, sublst in enumerate(values_list) if i not in empty_indices]
            kept_indices = [i for i in range(len(values_list)) if i not in empty_indices]
            # print(values_list, time_stamp_list)
            # popt, pcov = curve_fit(func, time_stamp_list, values_list, p0=(1, 0))
            # popt, pcov = curve_fit(exgaussian, time_stamp_list, values_list,
            #                        p0=[np.mean(time_stamp_list), np.std(time_stamp_list),
            #                            np.mean(time_stamp_list)])
            if len(new_lst) >= 5:
                for k in range(1, len(new_lst)):
                    while new_lst[k] > new_lst[k - 1]:
                        new_lst[k] = new_lst[k] - 0.001

                # print(new_lst, kept_indices)
                new_time_list = [intervals_list[i] for i in kept_indices]
                # print(new_lst, new_time_list)
                new_time_list.insert(0, 0)
                new_lst.insert(0, 1)
                new_time_list = np.array(new_time_list)
                new_time_list.astype(float)
                new_lst = np.array(new_lst)
                new_lst.astype(float)
                param_bounds = ([-np.inf, -np.inf, -np.inf], [0, 1, np.inf])
                popt, pcov = curve_fit(func, new_time_list, new_lst, bounds=param_bounds)
                my_curves_para[i][j].append(popt[0])
                my_curves_para[i][j].append(popt[1])
                my_curves_para[i][j].append(popt[2])
                my_curves_y_list[i][j].append(new_lst)
                my_curves_x_list[i][j].append(new_time_list)
    return my_curves_para, my_curves_x_list, my_curves_y_list


Curves_paras, my_cor_rate_x_list, my_cor_rate_y_list = Fitring_curves(my_cor_rate, intervals_list)



def generate_yaml(paras):
    newparas = {}
    for i in range(len(paras)):
        count = 0
        # print(i+1," :",paras[i])
        for j in range(i + 2):
            if len(paras[i][j]) == 0:
                count = count + 1
                paras[i][j].extend([-1, -1])
            newparas[i] = [i + 2 - count, paras[i]]

    data_dict = {key: val[1] for key, val in newparas.items()}

    # print(data_dict)

    def generate_data(paras):
        data = []
        for i in range(len(paras)):
            data_dict = {}
            for j in range(len(paras[i])):
                data_dict[j] = paras[i][j]
            data.append(data_dict)
        return data

    data = generate_data(paras)
