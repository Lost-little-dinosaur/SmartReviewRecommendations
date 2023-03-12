import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from scipy.optimize import curve_fit
import math
from sklearn.cluster import KMeans

np.set_printoptions(threshold=np.inf)

dirPath = "../GetData/SeveralAnswerQuestionSetDict/"



with open(dirPath + 'ThreeAnswerList.pkl', 'rb') as f1:
    ThreeAnswerData = pickle.load(f1)
    # print(ThreeAnswerData)

with open(dirPath + 'TwoAnswerList.pkl', 'rb') as f2:
    TwoAnswerData = pickle.load(f2)
    # print(TwoAnswerData)

Third_TimesData = []

for ThreeKey in ThreeAnswerData.keys():
    Third_TimesData += ThreeAnswerData.get(ThreeKey)  # 读取三次记录的所有题库的数据

Third_TimesData = np.array(Third_TimesData)
# print(Third_TimesData)


Second_TimesData = []
for Twokey in TwoAnswerData.keys():
    Second_TimesData += TwoAnswerData.get(Twokey)  #读取两次记录的所有题库的数据
# print(Second_TimesData)

Second_TimesData = np.array(Second_TimesData)

#
##打印时间间隔的长度
# print(max(Second_TimesData[:, 2]))
# print(max(Third_TimesData[:, 3]))
# print(max(Third_TimesData[:, 4]))


# 打印第三次的最终结构化数组
# print(Third_TimesData)

##离散化时间戳,暂时使用使用KMeans离散化
def KMeans_Discretized_Timestamp(data):
    KMeans_model = KMeans(n_clusters=8, random_state=0)
    data1 = KMeans_model.fit_predict(data[:, 2].reshape(data[:, 2].shape[0], 1))
    data = np.insert(data, 3, data1, axis=1)


##自定义答过两次题目的离散化
def Customize_Discretized_Timestamp_SecondTimes(data):
    StandardTimeStamp = [0, 10, 30, 60, 720, 1440, 2880, 10080, 14880, 21600, 43200,
                         243697]  # 分别代表10分钟、30分钟、60分钟、12小时、一天、两天、7天、十天、15天、一个月、最大的169天
    se_TimeStamp = pd.Series(data[:, 2])
    se1 = pd.cut(se_TimeStamp, StandardTimeStamp, right=False,
                 labels=[10, 30, 60, 720, 1440, 2880, 6480, 12480, 18240, 32400, 243697])
    count = pd.value_counts(se1)
    se1 = np.array(se1)
    # print(se1)
    data_T = []
    data_F = []
    count_T = 0
    count_F = 0
    data1 = data
    data = np.insert(data, 3, se1, axis=1)
    # print(data)
    for i in range(len(data)):
        if data[i][0] == 1:
            data_T.append(data[i, 1:4])
            count_T = count_T + 1
        else:
            data_F.append(data[i, 1:4])
            count_F = count_F + 1
    data_T = np.array(data_T)
    data_F = np.array(data_F)
    # print(data_T)
    # print(data_F)
    return data_T, data_F, count_T, count_F


# 调用两次的函数返回数据和其对应数量
DiscretizedSecondTimesData_T, DiscretizedSecondTimesData_F, count_T_sec, count_F_sec = Customize_Discretized_Timestamp_SecondTimes(
    Second_TimesData)


##自定义答过三次题目的离散化
def Customize_Discretized_Timestamp_ThirdTimes(data):
    StandardTimeStamp = [0, 10, 30, 60, 720, 1440, 2880, 10080, 14880,
                         21600, 43200, 63560]  # 分别代表10分钟、30分钟、60分钟、12小时、1天、2天、7天、十天、16天(最大)
    se_TimeStamp = pd.Series(data[:, 4])
    se1 = pd.cut(se_TimeStamp, StandardTimeStamp, right=False,
                 labels=[10, 30, 60, 720, 1440, 2880, 6480, 12480, 18240, 32400, 63560])
    count = pd.value_counts(se1)
    se1 = np.array(se1)
    # print(se1)
    data_T_T = []
    data_T_F = []
    data_F_T = []
    data_F_F = []
    count_T_T = 0
    count_T_F = 0
    count_F_T = 0
    count_F_F = 0
    data1 = data
    data = np.insert(data, 5, se1, axis=1)
    # print(data)
    for i in range(len(data)):
        if data[i][0] == 1:
            if data[i][1] == 1:
                data_T_T.append(data[i, [2, 5]])
                count_T_T = count_T_T + 1
            else:
                data_T_F.append(data[i, [2, 5]])
                count_T_F = count_T_F + 1
        else:
            if data[i][1] == 1:
                data_F_T.append(data[i, [2, 5]])
                count_F_T = count_F_T + 1
            else:
                data_F_F.append(data[i, [2, 5]])
                count_F_F = count_F_F + 1
    data_T_T = np.array(data_T_T)
    data_T_F = np.array(data_T_F)
    data_F_T = np.array(data_F_T)
    data_F_F = np.array(data_F_F)
    # print(data_T_T)
    # print(data_F)
    return data_T_T, data_T_F, data_F_T, data_F_F, count_T_T, count_T_F, count_F_T, count_F_F


DiscretizedThirdTimesData_T_T, DiscretizedThirdTimesData_T_F, DiscretizedThirdTimesData_F_T, DiscretizedThirdTimesData_F_F, count_T_T_Third, count_T_F_Third, count_F_T_Third, count_F_F_Third = Customize_Discretized_Timestamp_ThirdTimes(
    Third_TimesData)


# print(DiscretizedThirdTimesData_F_F)
##定义2次答题的返回的离散化的y和其对应的x
def return_t_y_third(data):
    dic = {
        10: 0,
        30: 0,
        60: 0,
        720: 0,
        1440: 0,
        2880: 0,
        6480: 0,
        12480: 0,
        18240: 0,
        32400: 0,
        63560: 0
    }
    dic_T = {
        10: 0,
        30: 0,
        60: 0,
        720: 0,
        1440: 0,
        2880: 0,
        6480: 0,
        12480: 0,
        18240: 0,
        32400: 0,
        63560: 0

    }
    for i in data[:, 1]:
        if i in dic:
            dic[i] = dic[i] + 1
    for i in range(len(data)):
        if data[i][0] == 1:
            dic_T[data[i][1]] = dic_T[data[i][1]] + 1

    # print(dic)
    # print(dic_T)
    return dic, dic_T


ThirdTimesCountTT, ThirdTimesAnswersTTT = return_t_y_third(DiscretizedThirdTimesData_T_T)
ThirdTimesCountTF, ThirdTimesAnswersTFT = return_t_y_third(DiscretizedThirdTimesData_T_F)
ThirdTimesCountFT, ThirdTimesAnswersFTT = return_t_y_third(DiscretizedThirdTimesData_F_T)
ThirdTimesCountFF, ThirdTimesAnswersFFT = return_t_y_third(DiscretizedThirdTimesData_F_F)


# 定义三次答题的返回其正确率和对应时间的函数
def returntxandy_Third(x, y):
    dic = {}
    arr = [10, 30, 30, 60, 720, 1440, 2880, 6480, 12480, 18240, 32400, 63560]
    arr = np.array(arr)
    for i in arr:
        if y[i] == 0:
            dic[i] = 1
        else:
            dic[i] = x[i] / y[i]
    return dic


FirstTSecondT = returntxandy_Third(ThirdTimesAnswersTTT, ThirdTimesCountTT)
FirstTSecondF = returntxandy_Third(ThirdTimesAnswersTFT, ThirdTimesCountTF)
FirstFSecondT = returntxandy_Third(ThirdTimesAnswersFTT, ThirdTimesCountFT)
FirstFSecondF = returntxandy_Third(ThirdTimesAnswersFFT, ThirdTimesCountFF)


# print(FirstTSecondT)
# print(FirstTSecondF)
# print(FirstFSecondF)


# 将正确率正确化,也就是如果从第二个开始后面比前面大那么就减某个值直到其比前一个小为止
def accuacry(a):
    a = a.items()
    a = list(a)
    a = np.array(a)
    for i in range(1, 11):
        while a[i][1] > a[i - 1][1]:
            a[i][1] = a[i][1] - 0.01
    return a


result_T_T = accuacry(FirstTSecondT)
result_T_F = accuacry(FirstTSecondF)
result_F_T = accuacry(FirstFSecondT)
result_F_F = accuacry(FirstFSecondF)


# print(result_T_T)
# print(result_T_F)
# print(result_F_T)
# print(result_F_F)


# # print(result_T)#自定义的时间间隔和对应的正确率，第一次题目答对时的记录
# result_T_F = FirstTSecondF.items()
# result_T_F = list(result_T_F)
# result_T_F = np.array(result_T_F)
# for i in range(1, 10):
#     while result_T_F[i][1] > result_T_F[i - 1][1]:
#         result_T_F[i][1] = result_T_F[i][1] - 0.01


##定义2次答题的返回的离散化的y和其对应的x
def return_t_y(data):
    dic = {}
    dic_T = {
        10: 0,
        30: 0,
        60: 0,
        720: 0,
        1440: 0,
        2880: 0,
        6480: 0,
        12480: 0,
        18240: 0,
        32400: 0,
        243697: 0

    }
    for i in data[:, 2]:
        if i in dic:
            dic[i] = dic[i] + 1
        else:
            dic[i] = 1
    for i in range(len(data)):
        if data[i][0] == 1:
            dic_T[data[i][2]] = dic_T[data[i][2]] + 1
    # print(dic)
    # print(dic_T)
    return dic, dic_T


SecondeTimesCountT, SecondeTimesTrue = return_t_y(DiscretizedSecondTimesData_T)
SecondeTimesCountF, SecondeTimesFalse = return_t_y(DiscretizedSecondTimesData_F)


# print(SecondeTimesTrue[10])
# print(count_T_sec, count_F_sec)


#
def returntxandy(x, y):
    dic = {}
    arr = [10, 30, 30, 60, 720, 1440, 2880, 6480, 12480, 18240, 32400, 243697]
    arr = np.array(arr)
    for i in arr:
        dic[i] = x[i] / y[i]
    return dic


# print(returntxangy(SecondeTimesTrue, SecondeTimesCountT))##定义的字典，对应时间间隔的正确率，第一次题目回答正确
# print(returntxangy(SecondeTimesFalse, SecondeTimesCountF))##定义的字典，对应时间间隔的正确率，第一次题目回答正确

FirstT = returntxandy(SecondeTimesTrue, SecondeTimesCountT)
FirstF = returntxandy(SecondeTimesFalse, SecondeTimesCountF)
result_T = FirstT.items()
result_T = list(result_T)
result_T = np.array(result_T)
for i in range(1, 11):
    while result_T[i][1] > result_T[i - 1][1]:
        result_T[i][1] = result_T[i][1] - 0.01

# print(result_T)#自定义的时间间隔和对应的正确率，第一次题目答对时的记录
result_F = FirstF.items()
result_F = list(result_F)
result_F = np.array(result_F)
for i in range(1, 11):
    while result_F[i][1] > result_F[i - 1][1]:
        result_F[i][1] = result_F[i][1] - 0.01


# print(result_F)#自定义的时间间隔和对应的正确率，第一次题目答错时的记录


##定义调参的函数
def TwoAnswerCurves(data1, data2):
    # xdata = [19.8, 60, 528, 1440, 2880,14880]
    # ydata = [50.0, 40.0, 32.0, 25.0, 23.6,21.4]
    xdata = data1
    ydata = data2
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    xdata = xdata.astype('float64')
    ydata = ydata.astype('float64')
    # print(xdata, ydata)
    e = math.e

    ### define the fit functions, y = e^(x*[a*ln(x)]-b) ###
    def target_func(x, a, b):
        return e ** (x * a + b)

    param_bounds = ([-np.inf, -np.inf], [0, 1])
    ### curve fit ###
    popt, pcov = curve_fit(target_func, xdata, ydata, bounds=param_bounds)

    ### Calculate R Square ###
    calc_ydata = [target_func(i, popt[0], popt[1]) for i in xdata]
    res_ydata = np.array(ydata) - np.array(calc_ydata)
    ss_res = np.sum(res_ydata ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # ### Output results ###
    # print("a = %f  b = %f  R2 = %f" % (popt[0], popt[1], r_squared))
    # print(ydata, calc_ydata)
    return popt[0], popt[1]


##第2次答题最终的参数确定和部分时间间隔的输出测试
a_FirstTrue, b_FirstTrue = TwoAnswerCurves(result_T[:, 0], result_T[:, 1])
a_FirstFalse, b_FirstFalse = TwoAnswerCurves(result_F[:, 0], result_F[:, 1])

##第3次答题最终的参数确定和部分时间间隔的输出测试
a_FirstTrueSecondTrue, b_FirstTrueSecondTrue = TwoAnswerCurves(result_T_T[:, 0], result_T_T[:, 1])
a_FirstTrueSecondFalse, b_FirstTrueSecondFalse = TwoAnswerCurves(result_T_F[:, 0], result_T_F[:, 1])
a_FirstFalseSecondTrue, b_FirstFalseSecondTrue = TwoAnswerCurves(result_F_T[:, 0], result_F_T[:, 1])
a_FirstFalseSecondFalse, b_FirstFalseSecondFalse = TwoAnswerCurves(result_F_F[:, 0], result_F_F[:, 1])

# result_T_1 = np.delete(result_T,[9,10],axis=0)
# result_F_1 = np.delete(result_F,[9,10],axis=0)
#
# T_result = (result_T_1*0.6 +result_T_T*0.25+result_F_T*0.15)/3
# F_result = (result_F_1*0.6+result_T_F*0.15+result_F_F*0.25)/3


# a_zonghe_firsttrue,b_zonghefirsttrue = TwoAnswerCurves(T_result[:,0],T_result[:,1])
# a_zonghe_firstfalse,b_zonghefirstfalse  = TwoAnswerCurves(F_result[:,0],F_result[:,1])

import xlwt

myparameter = xlwt.Workbook(encoding='utf-8', style_compression=0)

sheet = myparameter.add_sheet('曲线参数表', cell_overwrite_ok=True)
col = ('图像名称', '参数a', '参数b')
for i in range(0, 3):
    sheet.write(0, i, col[i])

datalist = [['第一次做对', a_FirstTrue, b_FirstTrue], ['第一次做错', a_FirstFalse, b_FirstFalse],
            ['第一次做对，第二次做对', a_FirstTrueSecondTrue, b_FirstTrueSecondTrue],
            ['第一次做对，第二次做错', a_FirstTrueSecondFalse, b_FirstTrueSecondFalse],
            ['第一次做错，第二次做对', a_FirstFalseSecondTrue, b_FirstFalseSecondTrue],
            ['第一次做错，第二次做错', a_FirstFalseSecondFalse, b_FirstFalseSecondFalse]]

for i in range(0, 6):
    data = datalist[i]
    for j in range(0, 3):
        sheet.write(i + 1, j, data[j])

# savepath = 'D:/excel.xls'
# myparameter.save(savepath)


if __name__ == '__main__':
    print('该遗忘曲线的函数模型为 : y = e**(a * x + b) [注:y为记忆率]')

    print('当该题库的刷题记录大于2万时：')
    i = np.array([30, 60, 100, 720, 1440, 2880, 6480, 12480, 18240, 32400, 243697])
    for x in i:
        y_FirstTrue = math.e ** (a_FirstTrue * x + b_FirstTrue)
        y_FirstFalse = math.e ** (a_FirstFalse * x + b_FirstFalse)
        # print(x, '分钟间隔后第1次正确、错误的情况下第2次答题正确率为', y_FirstTrue, y_FirstFalse)

    print('第1次正确的参数为：', 'a = ', a_FirstTrue, 'b = ', b_FirstTrue)
    # print('绘制出其图像为：')
    print('第1次错误的参数为：', 'a = ', a_FirstFalse, 'b = ', b_FirstFalse)

    i = np.array([30, 60, 100, 720, 1440, 2880, 6480, 12480, 18240, 32400, 243697])
    for x in i:
        y_FirstTrue = math.e ** (a_FirstTrue * x + b_FirstTrue)
        y_FirstFalse = math.e ** (a_FirstFalse * x + b_FirstFalse)
        # print(x, '分钟间隔后第一次正确、错误的情况下第3次答题正确率为', y_FirstTrue, y_FirstFalse)

    print('第1次正确,第2次正确的参数为：', 'a = ', a_FirstTrueSecondTrue, 'b = ', b_FirstTrueSecondTrue)
    print('第1次正确,第2次错误的参数为：', 'a = ', a_FirstTrueSecondFalse, 'b = ', b_FirstTrueSecondFalse)
    print('第1次错误,第2次正确的参数为：', 'a = ', a_FirstFalseSecondTrue, 'b = ', b_FirstFalseSecondTrue)
    print('第1次错误,第2次错误的参数为：', 'a = ', a_FirstFalseSecondFalse, 'b = ', b_FirstFalseSecondFalse)

    # print('当该题库的刷题记录小于2万时：')
    # print('前一次作对时的参数为：','a = ',a_zonghe_firsttrue,'b = ',b_zonghefirsttrue)
    # print('前一次作错时的参数为：', 'a = ', a_zonghe_firstfalse, 'b = ', b_zonghefirstfalse)

# <<<<<<< HEAD
# ##完成
# =======
# >>>>>>> 3558b6620f448374d4242000364e400aace8ab72
# if __name__ == 'main':
