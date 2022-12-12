import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from scipy.optimize import curve_fit
import math
from sklearn.cluster import KMeans

np.set_printoptions(threshold=np.inf)

dirPath = "../GetData/TwoThreeAnswerQuestionSetDict/"

with open(dirPath + 'ThreeAnswerList.pkl', 'rb') as f1:
    ThreeAnswerData = pickle.load(f1)
    # print(ThreeAnswerData)

with open(dirPath + 'TwoAnswerList.pkl', 'rb') as f2:
    TwoAnswerData = pickle.load(f2)
    # print(TwoAnswerData)
maogai_third_times = ThreeAnswerData.get('2021毛概题库.pkl')
xigai_third_times = ThreeAnswerData.get('2022年习概题库.pkl')
mayuan_third_times = ThreeAnswerData.get('2022年马原题库.pkl')
safety_third_times = ThreeAnswerData.get('安全基本知识.pkl')

Third_TimesData = maogai_third_times + xigai_third_times + mayuan_third_times + safety_third_times
# print(Third_TimesData)
Third_TimesData = np.array(Third_TimesData)
# print(Third_TimesData)

maogai_second_times = TwoAnswerData.get('2021毛概题库.pkl')
xigai_second_times = TwoAnswerData.get('2022年习概题库.pkl')
mayuan_second_times = TwoAnswerData.get('2022年马原题库.pkl')
safety_second_times = TwoAnswerData.get('安全基本知识.pkl')

Second_TimesData = maogai_second_times + xigai_second_times + mayuan_second_times + safety_second_times
Second_TimesData = np.array(Second_TimesData)

# print(Second_TimesData)
#
print(max(Second_TimesData[:, 2]))
print(max(Third_TimesData[:, 3]))
print(max(Third_TimesData[:, 4]))


##离散化时间戳,暂时使用使用KMeans离散化
def KMeans_Discretized_Timestamp(data):
    KMeans_model = KMeans(n_clusters=8, random_state=0)
    data1 = KMeans_model.fit_predict(data[:, 2].reshape(data[:, 2].shape[0], 1))
    data = np.insert(data, 3, data1, axis=1)


##自定义的离散化
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


DiscretizedSecondTimesData_T, DiscretizedSecondTimesData_F, count_T_sec, count_F_sec = Customize_Discretized_Timestamp_SecondTimes(
    Second_TimesData)


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
    print(dic)
    print(dic_T)
    return dic, dic_T


SecondeTimesCountT, SecondeTimesTrue = return_t_y(DiscretizedSecondTimesData_T)
SecondeTimesCountF, SecondeTimesFalse = return_t_y(DiscretizedSecondTimesData_F)
# print(SecondeTimesTrue[10])
print(count_T_sec, count_F_sec)


#
def returntxangy(x, y):
    dic = {}
    arr = [10, 30, 30, 60, 720, 1440, 2880, 6480, 12480, 18240, 32400, 243697]
    arr = np.array(arr)
    for i in arr:
        dic[i] = x[i] / y[i]
    return dic


print(returntxangy(SecondeTimesTrue, SecondeTimesCountT))
print(returntxangy(SecondeTimesFalse, SecondeTimesCountF))

FirstT = returntxangy(SecondeTimesTrue, SecondeTimesCountT)
FirstF = returntxangy(SecondeTimesFalse, SecondeTimesCountF)
result_T = FirstT.items()
result_T = list(result_T)
result_T = np.array(result_T)
for i in range(1, 11):
    while result_T[i][1] > result_T[i - 1][1]:
        result_T[i][1] = result_T[i][1] - 0.01

print(result_T)


# 定义错两次的调参函数
def TwoAnswerCurves(data1, data2):
    # xdata = [19.8, 60, 528, 1440, 2880,14880]
    # ydata = [50.0, 40.0, 32.0, 25.0, 23.6,21.4]
    xdata = data1
    ydata = data2
    xdata = np.array(xdata)
    ydata = np.array(ydata)
    xdata = xdata.astype('float64')
    ydata = ydata.astype('float64')
    print(xdata, ydata)
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
    print("a = %f  b = %f  R2 = %f" % (popt[0], popt[1], r_squared))
    print(ydata, calc_ydata)
    return popt[0], popt[1]


a, b = TwoAnswerCurves(result_T[:, 0], result_T[:, 1])
print(a, b)

x = 14,400,000
y = math.e ** (-1.486513215951767e-07 * x - 0.0647680527844464
               )
print(y)
