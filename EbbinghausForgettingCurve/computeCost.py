import csv
import math

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_squared_log_error, \
    median_absolute_error, explained_variance_score, max_error, mean_poisson_deviance, mean_gamma_deviance, \
    mean_tweedie_deviance, mean_absolute_percentage_error
# import EbbinghausCurves as Eb
import get_data


def computeCose(y_true, y_pred):
    # mean_absolute_error
    MAEArr = []
    # mean_squared_error
    MSEArr = []
    RMSEArr = []
    # r2_score
    R2Arr = []
    # mean_squared_log_error
    MSLEArr = []
    # median_absolute_error
    MedAEArr = []
    # explained_variance_score
    EVSArr = []
    # max_error
    MaxErrArr = []
    # mean_poisson_deviance
    MPDArr = []
    # mean_gamma_deviance
    MGDArr = []
    # mean_tweedie_deviance
    MTDArr = []
    # mean_absolute_percentage_error
    MAPEArr = []
    SMAPEArr = []
    MSEArr.append(mean_squared_error(y_true, y_pred))
    RMSEArr.append(mean_squared_error(y_true, y_pred, squared=False))
    MAEArr.append(mean_absolute_error(y_true, y_pred))
    MAPEArr.append(mean_absolute_percentage_error(y_true, y_pred))
    SMAPEArr.append(2.0 * np.mean(
        np.abs(np.array(y_pred) - np.array(y_true)) / (np.abs(np.array(y_pred)) + np.abs(np.array(y_true)))) * 100)
    R2Arr.append(r2_score(y_true, y_pred))
    MSLEArr.append(mean_squared_log_error(y_true, y_pred))
    MedAEArr.append(median_absolute_error(y_true, y_pred))
    EVSArr.append(explained_variance_score(y_true, y_pred))
    MaxErrArr.append(max_error(y_true, y_pred))
    MPDArr.append(mean_poisson_deviance(y_true, y_pred))
    MGDArr.append(mean_gamma_deviance(y_true, y_pred))
    MTDArr.append(mean_tweedie_deviance(y_true, y_pred))

    # print("R2:", R2Arr[0])
    # print("下面是拟合优度的各种指标(以下除了R2和EVS越接近1越好外，其他指标越接近0越好)：")
    # print("MSE:", MSEArr[0])
    # print("RMSE:", RMSEArr[0])
    # print("MAE:", MAEArr[0])
    # print("MAPE:", MAPEArr[0])
    # print("SMAPE:", SMAPEArr[0])

    # print("R2:", R2Arr[0])
    print("下面是拟合优度的各种指标(以下除了R2和EVS越接近1越好外，其他指标越接近0越好)：")
    print("MSE:", MSEArr[0])
    print("RMSE:", RMSEArr[0])
    print("MAE:", MAEArr[0])
    print("MAPE:", MAPEArr[0])
    print("SMAPE:", SMAPEArr[0])
    print("R2:", R2Arr[0])
    print("MSLE:", MSLEArr[0])
    print("MedAE:", MedAEArr[0])
    print("EVS:", EVSArr[0])
    print("MaxErr:", MaxErrArr[0])
    print("MPD:", MPDArr[0])
    print("MGD:", MGDArr[0])
    print("MTD:", MTDArr[0])
    return [MSEArr[0], RMSEArr[0], MAEArr[0], MAPEArr[0], SMAPEArr[0], R2Arr[0], MSLEArr[0], MedAEArr[0], EVSArr[0],
            MaxErrArr[0], MPDArr[0], MGDArr[0], MTDArr[0]]


def return_result(result, a, b):
    pre_result = []
    result0 = [i[0] for i in result]
    result1 = [i[1] for i in result]
    result0 = np.array(result0)
    result0 = result0.astype('float64')
    result1 = np.array(result1)
    result1 = result1.astype('float64')
    for i in range(len(result)):
        preresult = math.e ** (a * result0[i] + b)
        pre_result.append(preresult)
    return computeCose(result1, pre_result)


def return_result_new(result0, result1, a, b, c, d):
    pre_result = []
    # result0 = [i[0] for i in result]
    # result1 = [i[1] for i in result]
    result0 = np.array(result0[0])
    result0 = result0.astype('float64')
    result1 = np.array(result1[0])
    result1 = result1.astype('float64')
    for i in range(len(result0)):
        preresult = a * math.e ** (b * result0[i] + c) + d
        pre_result.append(preresult)
    return computeCose(result1, pre_result)


def writeCSV(resultArr, HeadName):
    # 将resultArr转置一下
    resultArr = np.array(resultArr)
    resultArr = resultArr.T
    resultArr = resultArr.tolist()
    # 先写第一列的评价指标名字
    firstColumn = ["", 'MSE', 'RMSE', 'MAE', 'MAPE', 'SMAPE', 'R2', 'MSLE', 'MedAE', 'EVS', 'MaxErr', 'MPD', 'MGD',
                   'MTD']
    # 写入文件
    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([""] + HeadName)
        for i in range(len(resultArr)):
            writer.writerow([firstColumn[i + 1]] + resultArr[i])


# def old_curves():
# coseResult = [0, 0, 0, 0, 0, 0]
# print('第一次做对，第二次作答的曲线拟合指标：')
# coseResult[0] = return_result(Eb.result_T, Eb.a_FirstTrue, Eb.b_FirstTrue)
# # print(Eb.result_T,Eb.a_FirstFalse,Eb.b_FirstTrue)
# # writeCSV(coseResult, 'FirstTrue')
# print('第一次做错，第二次作答的曲线拟合指标：')
# coseResult[1] = return_result(Eb.result_F, Eb.a_FirstFalse, Eb.b_FirstFalse)
# # writeCSV(coseResult, 'FirstFalse')
# print('第一次做对，第二次做对，第三次作答的曲线拟合指标：')
# coseResult[2] = return_result(Eb.result_T_T, Eb.a_FirstTrueSecondTrue, Eb.b_FirstTrueSecondTrue)
# # writeCSV(coseResult, 'FirstTrueSecondTrue')
# print('第一次做对，第二次做错，第三次作答的曲线拟合指标：')
# coseResult[3] = return_result(Eb.result_T_F, Eb.a_FirstTrueSecondFalse, Eb.b_FirstTrueSecondFalse)
# # writeCSV(coseResult, 'FirstTrueSecondFalse')
# print('第一次做错，第二次做对，第三次作答的曲线拟合指标：')
# coseResult[4] = return_result(Eb.result_F_T, Eb.a_FirstFalseSecondTrue, Eb.b_FirstFalseSecondTrue)
# # writeCSV(coseResult, 'FirstFalseSecondTrue')
# print('第一次做错，第二次做错，第三次作答的曲线拟合指标：')
# coseResult[5] = return_result(Eb.result_F_F, Eb.a_FirstFalseSecondFalse, Eb.b_FirstFalseSecondFalse)
# writeCSV(coseResult,
#          ["第一次对", "第一次错", "第一次对第二次对", "第一次对第二次错", "第一次错第二次对", "第一次错第二次错"])

def new_curves():
    paras = get_data.Curves_paras
    x = get_data.my_cor_rate_x_list
    y = get_data.my_cor_rate_y_list

    for i in range(len(paras)):
        for j in range(i + 2):
            if len(paras[i][j]) != 0:
<<<<<<< HEAD
                print(i + 1, "次答题，错", j, "个的拟合曲线的指标如下：")
                return_result_new(x[i][j], y[i][j], paras[i][j][0], paras[i][j][1], paras[i][j][2], paras[i][j][3])
                print("\n")
=======
                # print(i + 1, "次答题，错", j, "个的拟合曲线的指标如下：")
                resultArr = return_result_new(x[i][j], y[i][j], paras[i][j][0], paras[i][j][1], paras[i][j][2])
                if resultArr[5]>0.85:
                    print(i + 1, "次答题，错", j, "个的拟合曲线的指标如下：")
                    print("R2:", resultArr[5])
                    print("MAE:", resultArr[2])
                    print("RMSE:", resultArr[1])
                    # print("\n")
                    a = paras[i][j][0]
                    b = paras[i][j][1]
                    c = paras[i][j][2]
                    print('遗忘率曲线参数为：', 'a = ', a, '; b = ', b, '; c = ', c, ";")
                    print("\n")
>>>>>>> dc670841d8f4b6e70c289f711843c526d5c7cca9


if __name__ == '__main__':
    new_curves()
    # myarray = np.array(get_data.my_cor_rate_y_list[0][0][0])
    # print(myarray)
    # print(get_data.Curves_paras[0][0])
