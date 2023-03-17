import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from scipy.optimize import curve_fit
import math
from sklearn.cluster import KMeans

np.set_printoptions(threshold=np.inf)

dirPath_SAQSD = '../GetData/SeveralAnswerQuestionSetDict/'
dirPath_All_Correct_rate = '../GetData/AllQuestionsCorrectRate/'
dirpath_Allusers_Answers = '../GetData/AllUsersAnswers/'

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

# files = os.listdir(dirpath_Allusers_Answers)
# AllAnswers = {}
# for file in files:
#     with open(dirpath_Allusers_Answers + file, 'rb') as f2:
#         Answers = pickle.load(f2)
#         AllAnswers.update(Answers)

# print(type(AllAnswerData[2]))
MaxTimeStamp = []

# 将dict转化成list，此时所有次数2-26次的答案都保存在了AllAnswerData1中了

AllAnswerData1 = []
for key in AllAnswerData.keys():
    AllAnswerData1.append(AllAnswerData[key])

AllAnswerData2 = AllAnswerData1

# print(list(AllAnswerData2[0][0].keys())[0])
# # for i  in AllAnswerData2[0][0].keys():
# #     print(i)
# print(AllAnswerData2[0][0][list(AllAnswerData2[0][0].keys())[0]])
#
# print(AllAnswerData2[0][0][list(AllAnswerData2[0][0].keys())[0]][0])
# print(AllCorrectRate[list(AllAnswerData2[0][0].keys())[0]][0])
# print(AllAnswerData1[0][0])


# 将列表所有答案中的正确的转化成其正确率，错误的还为0,存储在AllAnswerData2中
for i in range(len(AllAnswerData2)):
    for j in AllAnswerData2[i]:
        for k in range(i + 2):
            if j[list(j.keys())[0]][k] == 1:
                if list(j.keys())[0] in AllCorrectRate.keys():
                    j[list(j.keys())[0]][k] = \
                        AllCorrectRate[list(j.keys())[0]][0]

# 构造AllAnswerData3存放所有的答题记录的列表values值
levels = len(AllAnswerData2)
AllAnswerData3 = [[] for i in range(levels)]

for i in range(len(AllAnswerData2)):
    for j in AllAnswerData2[i]:
        AllAnswerData3[i].append(j[list(j.keys())[0]])

# 构造AllAnswerData4存放所有的分类完成后的values列表

levels1 = len(AllAnswerData3)
AllAnswerData4 = [[] for i in range(levels1)]
for i in range(levels1):
    AllAnswerData4[i] = [[] for j in range(i + 3)]

# for i in range(len(AllAnswerData3[0])):
#     print(AllAnswerData3[0][i])
#     if 0 in AllAnswerData3[0][i]


# 将答题记录再按照错误次数进行分类，并保存
# def fenlei_answers(answers):
levels1 = len(AllAnswerData3)
for i in range(levels1):
    myclassifications = i + 3
    for j in AllAnswerData3[i]:
        zero_exist = False  # 假设前两列中不存在0
        zero_num = 0
        if 0 in j[:myclassifications]:
            zero_exist = True
            zero_num = zero_num + 1
        AllAnswerData4[i][zero_num].append(j)
#             else:  # 如果j有多行，遍历每一行判断前两列是否存在0
#                 for row in j:
#                     if 0 in row[:i+3]:
#                         zero_exist = True
#                         zero_num = zero_num + 1
#                     AllAnswerData4.append(row)
