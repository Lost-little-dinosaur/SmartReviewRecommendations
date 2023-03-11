import copy
import json
import os
import pickle

import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import time


def main():
    # 数据库连接
    # 打开数据库连接
    # db = pymysql.connect(host='127.0.0.1',
    #                      port=3306,
    #                      user='root',
    #                      password='1234',
    #                      database='pinnacle_test')
    # # 利用pandas读取数据库
    # sql = "SELECT * FROM `papers`"
    # dfPaper = pd.read_sql(sql, db)
    # # 筛选出所有gen_type=ForgettingCurve且create_at>2023.02.09 21:11的paper的ID
    # forgettingCurvePaper = dfPaper[
    #     (dfPaper['gen_type'] == 'ForgettingCurve') & (dfPaper['created_at'] > '2023-02-09 21:12:00')]
    # # 筛选出所有gen_type=general的paper
    # generalPaper = dfPaper[dfPaper['gen_type'] == 'general']
    #
    # # 只需要保留id、paper_set_id和created_at三列
    # forgettingCurvePaper = forgettingCurvePaper[['id', 'paper_set_id', 'created_at']]
    # generalPaper = generalPaper[['id', 'paper_set_id', 'created_at']]

    # 读取AllUsersAnswers文件夹下所有用户的答题记录
    allUserAnswers = {}
    for eachFile in os.listdir('AllUsersAnswers'):
        with open('AllUsersAnswers/' + eachFile, 'rb') as f:
            allUserAnswers[eachFile] = pickle.load(f)
    # 选出所有大于三次的答题记录
    valuableUserAnswers = copy.deepcopy(allUserAnswers)
    for eachQuestionSet in allUserAnswers:
        for eachUserI in range(len(allUserAnswers[eachQuestionSet])):
            for eachUserQuestion in allUserAnswers[eachQuestionSet][eachUserI].items():
                if len(eachUserQuestion[1]) < 3:
                    del valuableUserAnswers[eachQuestionSet][eachUserI][eachUserQuestion[0]]

    allValuableUserAnswersList = []
    for eachQuestionSet in valuableUserAnswers:
        eachUserI = 0
        while eachUserI < len(valuableUserAnswers[eachQuestionSet]):
            for eachUserQuestion in valuableUserAnswers[eachQuestionSet][eachUserI].items():
                allValuableUserAnswersList.append(eachUserQuestion[1])
            eachUserI += 1
    # 对所有用户的答题记录进行分类
    oneTrueTwoGeneralUserAnswers = []
    oneTrueThreeGeneralUserAnswers = []
    oneTrueFourGeneralUserAnswers = []
    oneTrueFiveGeneralUserAnswers = []

    oneFalseTwoGeneralUserAnswers = []
    oneFalseThreeGeneralUserAnswers = []
    oneFalseFourGeneralUserAnswers = []
    oneFalseFiveGeneralUserAnswers = []

    oneFalseTwoForgettingCurveUserAnswers = []
    oneFalseThreeForgettingCurveUserAnswers = []
    oneFalseFourForgettingCurveUserAnswers = []
    oneFalseFiveForgettingCurveUserAnswers = []

    oneTrueTwoForgettingCurveUserAnswers = []
    oneTrueThreeForgettingCurveUserAnswers = []
    oneTrueFourForgettingCurveUserAnswers = []
    oneTrueFiveForgettingCurveUserAnswers = []

    oneTrueTwoGeneralUserRightCount = 0
    oneTrueThreeGeneralUserRightCount = 0
    oneTrueFourGeneralUserRightCount = 0
    oneTrueFiveGeneralUserRightCount = 0

    oneFalseTwoGeneralUserRightCount = 0
    oneFalseThreeGeneralUserRightCount = 0
    oneFalseFourGeneralUserRightCount = 0
    oneFalseFiveGeneralUserRightCount = 0

    oneFalseTwoForgettingCurveUserRightCount = 0
    oneFalseThreeForgettingCurveUserRightCount = 0
    oneFalseFourForgettingCurveUserRightCount = 0
    oneFalseFiveForgettingCurveUserRightCount = 0

    oneTrueTwoForgettingCurveUserRightCount = 0
    oneTrueThreeForgettingCurveUserRightCount = 0
    oneTrueFourForgettingCurveUserRightCount = 0
    oneTrueFiveForgettingCurveUserRightCount = 0
    for eachUserAnswer in allValuableUserAnswersList:  # 筛选出
        if len(eachUserAnswer) == 3:
            if eachUserAnswer[0][0] == 1:  # 如果第一次答题正确
                if eachUserAnswer[1][2] == 'ForgettingCurve':  # 如果第二次答题是依照ForgettingCurve生成推荐的
                    oneTrueTwoForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneTrueTwoForgettingCurveUserRightCount += 1 if eachUserAnswer[2][0] == 1 else 0
                else:
                    oneTrueTwoGeneralUserAnswers.append(eachUserAnswer)
                    oneTrueTwoGeneralUserRightCount += 1 if eachUserAnswer[2][0] == 1 else 0
            else:
                if eachUserAnswer[1][2] == 'ForgettingCurve':
                    oneFalseTwoForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneFalseTwoForgettingCurveUserRightCount += 1 if eachUserAnswer[2][0] == 1 else 0
                else:
                    oneFalseTwoGeneralUserAnswers.append(eachUserAnswer)
                    oneFalseTwoGeneralUserRightCount += 1 if eachUserAnswer[2][0] == 1 else 0
        elif len(eachUserAnswer) == 4:
            if eachUserAnswer[0][0] == 1:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve':
                    oneTrueThreeForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneTrueThreeForgettingCurveUserRightCount += 1 if eachUserAnswer[3][0] == 1 else 0
                else:
                    oneTrueThreeGeneralUserAnswers.append(eachUserAnswer)
                    oneTrueThreeGeneralUserRightCount += 1 if eachUserAnswer[3][0] == 1 else 0
            else:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve':
                    oneFalseThreeForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneFalseThreeForgettingCurveUserRightCount += 1 if eachUserAnswer[3][0] == 1 else 0
                else:
                    oneFalseThreeGeneralUserAnswers.append(eachUserAnswer)
                    oneFalseThreeGeneralUserRightCount += 1 if eachUserAnswer[3][0] == 1 else 0
        elif len(eachUserAnswer) == 5:
            if eachUserAnswer[0][0] == 1:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve' and \
                        eachUserAnswer[3][2] == 'ForgettingCurve':
                    oneTrueFourForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneTrueFourForgettingCurveUserRightCount += 1 if eachUserAnswer[4][0] == 1 else 0
                else:
                    oneTrueFourGeneralUserAnswers.append(eachUserAnswer)
                    oneTrueFourGeneralUserRightCount += 1 if eachUserAnswer[4][0] == 1 else 0
            else:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve' and \
                        eachUserAnswer[3][2] == 'ForgettingCurve':
                    oneFalseFourForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneFalseFourForgettingCurveUserRightCount += 1 if eachUserAnswer[4][0] == 1 else 0
                else:
                    oneFalseFourGeneralUserAnswers.append(eachUserAnswer)
                    oneFalseFourGeneralUserRightCount += 1 if eachUserAnswer[4][0] == 1 else 0
        elif len(eachUserAnswer) == 6:
            if eachUserAnswer[0][0] == 1:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve' and \
                        eachUserAnswer[3][2] == 'ForgettingCurve' and eachUserAnswer[4][2] == 'ForgettingCurve':
                    oneTrueFiveForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneTrueFiveForgettingCurveUserRightCount += 1 if eachUserAnswer[5][0] == 1 else 0
                else:
                    oneTrueFiveGeneralUserAnswers.append(eachUserAnswer)
                    oneTrueFiveGeneralUserRightCount += 1 if eachUserAnswer[5][0] == 1 else 0
            else:
                if eachUserAnswer[1][2] == 'ForgettingCurve' and eachUserAnswer[2][2] == 'ForgettingCurve' and \
                        eachUserAnswer[3][2] == 'ForgettingCurve' and eachUserAnswer[4][2] == 'ForgettingCurve':
                    oneFalseFiveForgettingCurveUserAnswers.append(eachUserAnswer)
                    oneFalseFiveForgettingCurveUserRightCount += 1 if eachUserAnswer[5][0] == 1 else 0
                else:
                    oneFalseFiveGeneralUserAnswers.append(eachUserAnswer)
                    oneFalseFiveGeneralUserRightCount += 1 if eachUserAnswer[5][0] == 1 else 0
    print("第一次做对了第二次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneTrueTwoForgettingCurveUserRightCount / len(oneTrueTwoForgettingCurveUserAnswers), "一共有",
          len(oneTrueTwoForgettingCurveUserAnswers), "个样本")
    print("第一次做对了第二三次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneTrueThreeForgettingCurveUserRightCount / len(oneTrueThreeForgettingCurveUserAnswers), "一共有",
          len(oneTrueThreeForgettingCurveUserAnswers), "个样本")
    print("第一次做对了第二三四次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneTrueFourForgettingCurveUserRightCount / len(oneTrueFourForgettingCurveUserAnswers), "一共有",
          len(oneTrueFourForgettingCurveUserAnswers), "个样本")
    print("第一次做对了第二三四五次再用ForgettingCurve生成推荐的用户答题正确率为：",
            oneTrueFiveForgettingCurveUserRightCount / len(oneTrueFiveForgettingCurveUserAnswers), "一共有",
            len(oneTrueFiveForgettingCurveUserAnswers), "个样本")
    print()

    print("第一次做对了第二次再用general生成推荐的用户答题正确率为：",
          oneTrueTwoGeneralUserRightCount / len(oneTrueTwoGeneralUserAnswers), "一共有",
          len(oneTrueTwoGeneralUserAnswers), "个样本")
    print("第一次做对了第二三次再用general生成推荐的用户答题正确率为：",
          oneTrueThreeGeneralUserRightCount / len(oneTrueThreeGeneralUserAnswers), "一共有",
          len(oneTrueThreeGeneralUserAnswers), "个样本")
    print("第一次做对了第二三四次再用general生成推荐的用户答题正确率为：",
          oneTrueFourGeneralUserRightCount / len(oneTrueFourGeneralUserAnswers), "一共有",
          len(oneTrueFourGeneralUserAnswers), "个样本")
    print("第一次做对了第二三四五次再用general生成推荐的用户答题正确率为：",
            oneTrueFiveGeneralUserRightCount / len(oneTrueFiveGeneralUserAnswers), "一共有",
            len(oneTrueFiveGeneralUserAnswers), "个样本")
    print()

    print("第一次做错了第二次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneFalseTwoForgettingCurveUserRightCount / len(oneFalseTwoForgettingCurveUserAnswers), "一共有",
          len(oneFalseTwoForgettingCurveUserAnswers), "个样本")
    print("第一次做错了第二三次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneFalseThreeForgettingCurveUserRightCount / len(oneFalseThreeForgettingCurveUserAnswers), "一共有",
          len(oneFalseThreeForgettingCurveUserAnswers), "个样本")
    print("第一次做错了第二三四次再用ForgettingCurve生成推荐的用户答题正确率为：",
          oneFalseFourForgettingCurveUserRightCount / len(oneFalseFourForgettingCurveUserAnswers), "一共有",
          len(oneFalseFourForgettingCurveUserAnswers), "个样本")
    print("第一次做错了第二三四五次再用ForgettingCurve生成推荐的用户答题正确率为：",
            oneFalseFiveForgettingCurveUserRightCount / len(oneFalseFiveForgettingCurveUserAnswers), "一共有",
            len(oneFalseFiveForgettingCurveUserAnswers), "个样本")
    print()

    print("第一次做错了第二次再用general生成推荐的用户答题正确率为：",
          oneFalseTwoGeneralUserRightCount / len(oneFalseTwoGeneralUserAnswers), "一共有",
          len(oneFalseTwoGeneralUserAnswers), "个样本")
    print("第一次做错了第二三次再用general生成推荐的用户答题正确率为：",
          oneFalseThreeGeneralUserRightCount / len(oneFalseThreeGeneralUserAnswers), "一共有",
          len(oneFalseThreeGeneralUserAnswers), "个样本")
    print("第一次做错了第二三四次再用general生成推荐的用户答题正确率为：",
          oneFalseFourGeneralUserRightCount / len(oneFalseFourGeneralUserAnswers), "一共有",
          len(oneFalseFourGeneralUserAnswers), "个样本")
    print("第一次做错了第二三四五次再用general生成推荐的用户答题正确率为：",
          oneFalseFiveGeneralUserRightCount / len(oneFalseFiveGeneralUserAnswers), "一共有",
            len(oneFalseFiveGeneralUserAnswers), "个样本")
    print()


if __name__ == '__main__':
    main()
