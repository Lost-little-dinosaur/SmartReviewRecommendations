# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import  math
# ##对于艾宾浩斯遗忘曲线的拟合，很多学者只使用一个函数。虽然整体拟合程度较好，但在0～60分钟内拟合函数与原始数据点差异较大。因此，尝试拟合0～60分钟的遗忘曲线，试图建立一个新的函数。
#
#
# plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
#
#
# ##幂函数 b = k * t^(-0.125)
# #时间设定为分钟为单位，选取10080，正好7天整
# #第一次作对的情况下
# t_T = np.arange(1,10080,1)
# b_T = 31.8 * np.power(t_T,-0.125)
# print(b_T)
# plt.xlabel('t')
# plt.ylabel('b')
# plt.title("遗忘曲线1")
# plt.plot(t_T, b_T)
# plt.savefig('./True_First.png')
# plt.show()
#
#
#
# #第一次做错的情况下
# t_F = np.arange(1,10080,1)
# b_F = 31.8 * np.power(t_F,-0.5)
# print(b_F)
# plt.xlabel('t')
# plt.ylabel('b')
# plt.title("遗忘曲线2")
# plt.plot(t_F, b_F)
# plt.savefig('./False_First.png')
# plt.show()
#
#
# ##对数函数（艾宾浩斯的拟合函数） b = 100k / ((logt)^c + k)
#
# t = np.arange(2,100,1)
# f = np.log2(t)
# b = 100 * 1.84 / (np.power(f,1.25) + 1.84)
# plt.xlabel('t')
# plt.ylabel('b')
# plt.title("遗忘曲线3")
# plt.plot(t, b)
# plt.savefig('./True_First_ori.png')
# plt.show()
#


#使用该幂函数拟合艾宾浩斯初始曲线
#第一次做对
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
np.seterr(divide='ignore', invalid='ignore')  # 消除被除数为0的警告
def Ebbinghaus_fun_orig_t(xdata,ydata):
    # xdata = [19.8, 60, 528, 1440, 2880,14880]
    # ydata = [58.2, 44.2, 35.8, 33.7, 27.8,25.4]


    ### define the fit functions, y = a * x^b ###
    def target_func(x, a, b,c):
        return a * (x ** b) + c


    ### curve fit ###
    popt, pcov = curve_fit(target_func, xdata, ydata)

    ### Calculate R Square ###
    calc_ydata = [target_func(i, popt[0], popt[1],popt[2]) for i in xdata]
    res_ydata = np.array(ydata) - np.array(calc_ydata)
    ss_res = np.sum(res_ydata ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # ### Output results ###
    print("a = %f  b = %f   R2 = %f" % (popt[0], popt[1], r_squared))
    print(ydata, calc_ydata)
    return popt[0], popt[1],popt[2]

#使用该幂函数拟合艾宾浩斯初始曲线
#第一次做错
from scipy.optimize import curve_fit
import numpy as np
def Ebbinghaus_fun_orig_f(xdata,ydata):
    # xdata = [19.8, 60, 528, 1440, 2880,14880]
    # ydata = [50.0, 40.0, 32.0, 25.0, 23.6,21.4]


    ### define the fit functions, y = a * x^b ###
    def target_func(x, a, b,c):
        return a * (x ** b)+c


    ### curve fit ###
    popt, pcov = curve_fit(target_func, xdata, ydata)

    ### Calculate R Square ###
    calc_ydata = [target_func(i, popt[0], popt[1],popt[2]) for i in xdata]
    res_ydata = np.array(ydata) - np.array(calc_ydata)
    ss_res = np.sum(res_ydata ** 2)
    ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # ### Output results ###
    print("a = %f  b = %f c = %f  R2 = %f" % (popt[0], popt[1],popt[2], r_squared))
    print(ydata, calc_ydata)
    return popt[0],popt[1],popt[2]


##输入时间间隔输出参数K,A,C  B = K * t ^ A + C
def para_return_ff(t):

    # 两次都错
    xdata_f_f_60 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_f_60 = [100, 85.0, 80.0, 76.7, 60.2, 58.7, 45.4]

    xdata_f_f_1440 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_f_1440 = [100, 84.3, 78.5, 71.4, 56.8, 50.6, 40.4]

    xdata_f_f_2880 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_f_2880 = [100, 80.0, 72.8, 68.4, 50.8, 48.6, 35.4]

    xdata_f_f_14480 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_f_14480 = [100, 74.4, 67.8, 60.4, 55.8, 44.6, 30.2]

    t = [60,1440,2880,14480]
    k_f_f_1, c_f_f_1, a_f_f_1 = Ebbinghaus_fun_orig_f(xdata_f_f_60, ydata_f_f_60)
    k_f_f_2, c_f_f_2, a_f_f_2 = Ebbinghaus_fun_orig_f(xdata_f_f_1440, ydata_f_f_1440)
    k_f_f_3, c_f_f_3, a_f_f_3 = Ebbinghaus_fun_orig_f(xdata_f_f_2880, ydata_f_f_2880)
    k_f_f_4, c_f_f_4, a_f_f_4 = Ebbinghaus_fun_orig_f(xdata_f_f_14480, ydata_f_f_14480)
    K_f_f = [k_f_f_1,k_f_f_2,k_f_f_3,k_f_f_4]
    C_f_f = [c_f_f_1,c_f_f_2,c_f_f_3,c_f_f_4]
    A_f_f = [a_f_f_1,a_f_f_2,a_f_f_3,a_f_f_4]
    # print(K_f_f, A_f_f, C_f_f)
    t = np.array(t)
    #调参K
    K_f_f = np.array(K_f_f)
    Z_K = np.polyfit(t,K_f_f,3)
    K_F_F = np.poly1d(Z_K)
    #调参C
    C_f_f = np.array(C_f_f)
    Z_C = np.polyfit(t,C_f_f,3)
    C_F_F = np.poly1d(Z_C)
    #调参A
    A_f_f = np.array(A_f_f)
    Z_A = np.polyfit(t,A_f_f,3)
    A_F_F = np.poly1d(Z_A)

    return K_F_F(t),A_F_F(t),C_F_F(t)


##输入时间间隔输出参数K,A,C  B = K * t ^ A + C
def para_return_ft(t):

    # 第一次错，第二次对
    xdata_f_t_60 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_t_60 = [100, 95.6, 92.4, 88.6, 78.8, 70.6, 60.4]

    xdata_f_t_1440 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_t_1440 = [100, 90.0, 88.5, 80.4, 76.8, 70.6, 66.4]

    xdata_f_t_2880 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_t_2880 = [100, 88.0, 80.8, 78.4, 70.8, 68.6, 65.4]

    xdata_f_t_14480 = [0, 19.8, 60, 528, 1440, 2880, 14880]
    ydata_f_t_14480 = [100, 80.0, 77.8, 70.4, 65.8, 64.6, 60.2]

    k_f_t_1, c_f_t_1, a_f_t_1 = Ebbinghaus_fun_orig_f(xdata_f_t_60, ydata_f_t_60)
    k_f_t_2, c_f_t_2, a_f_t_2 = Ebbinghaus_fun_orig_f(xdata_f_t_1440, ydata_f_t_1440)
    k_f_t_3, c_f_t_3, a_f_t_3 = Ebbinghaus_fun_orig_f(xdata_f_t_2880, ydata_f_t_2880)
    k_f_t_4, c_f_t_4, a_f_t_4 = Ebbinghaus_fun_orig_f(xdata_f_t_14480, ydata_f_t_14480)

    K_f_t = [k_f_t_1, k_f_t_2, k_f_t_3, k_f_t_4]
    C_f_t = [c_f_t_1, c_f_t_2, c_f_t_3, c_f_t_4]
    A_f_t = [a_f_t_1, a_f_t_2, a_f_t_3, a_f_t_4]

    t = [60, 1440, 2880, 14480]
    t = np.array(t)
    #调参K
    K_f_t = np.array(K_f_t)
    Z_K = np.polyfit(t,K_f_t,3)
    K_F_T = np.poly1d(Z_K)
    #调参C
    C_f_t = np.array(C_f_t)
    Z_C = np.polyfit(t,C_f_t,3)
    C_F_T = np.poly1d(Z_C)
    #调参A
    A_f_t = np.array(A_f_t)
    Z_A = np.polyfit(t,A_f_t,3)
    A_F_T = np.poly1d(Z_A)

    return K_F_T(t),A_F_T(t),C_F_T(t)



if __name__ == '__main__':
    #第一次错
    xdata_f = [0,19.8, 60, 528, 1440, 2880,14880]
    ydata_f = [100,50.0, 40.0, 32.0, 25.0, 23.6,21.4]
    #第一次对
    xdata_t = [0,19.8, 60, 528, 1440, 2880,14880]
    ydata_t = [100,98.2, 94.2, 88.8, 83.7, 77.8,75.4]







    k_t,c_t,a_t = Ebbinghaus_fun_orig_t(xdata_t,ydata_t)
    # plt.xlabel('t')
    # plt.ylabel('b')
    # plt.title("遗忘曲线3")
    # plt.plot(xdata_f, ydata_f)
    # plt.savefig('./True_First_ori.png')
    # plt.show()
    k_f,c_f,a_f = Ebbinghaus_fun_orig_f(xdata_f,ydata_f)
    # k_f_f, c_f_f, a_f_f = Ebbinghaus_fun_orig_f(xdata_f_f_60, ydata_f_f_60)

    # print(K_f_t,A_f_t,C_f_t)




