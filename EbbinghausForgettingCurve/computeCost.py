import math

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_squared_log_error, \
    median_absolute_error, explained_variance_score, max_error, mean_poisson_deviance, mean_gamma_deviance, \
    mean_tweedie_deviance, mean_absolute_percentage_error
import EbbinghausCurves as Eb


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


def return_result(result, a, b, pre_result):
    result0 = [i[0] for i in result]
    result1 = [i[1] for i in result]
    result0 = np.array(result0)
    result0 = result0.astype('float64')
    result1 = np.array(result1)
    result1 = result1.astype('float64')
    for i in range(len(result)):
        preresult = math.e ** (a * result0[i] + b)
        pre_result.append(preresult)
    computeCose(result1, pre_result)


if __name__ == '__main__':
    print('第一次做对，第二次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_T, Eb.a_FirstTrue, Eb.b_FirstTrue, pre_result)

    print('第一次做错，第二次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_F, Eb.a_FirstFalse, Eb.b_FirstFalse, pre_result)

    print('第一次做对，第二次做对，第三次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_T_T, Eb.a_FirstTrueSecondTrue, Eb.b_FirstTrueSecondTrue, pre_result)

    print('第一次做对，第二次做错，第三次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_T_F, Eb.a_FirstTrueSecondFalse, Eb.b_FirstTrueSecondFalse, pre_result)

    print('第一次做错，第二次做对，第三次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_F_T, Eb.a_FirstFalseSecondTrue, Eb.b_FirstFalseSecondTrue, pre_result)

    print('第一次做错，第二次做错，第三次作答的曲线拟合指标：')
    pre_result = []
    return_result(Eb.result_F_F, Eb.a_FirstFalseSecondFalse, Eb.b_FirstFalseSecondFalse, pre_result)
