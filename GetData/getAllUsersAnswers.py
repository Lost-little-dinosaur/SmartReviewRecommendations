import json
import pickle

import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import time


# def getAllQuestions():
#     returnArr = []
#     for each in jsonData["AllUsersAnswers"]:
#         returnArr.append({
#             "ID": each["ID"],
#             "text": each["text"],
#             "answerList": [{
#                 "text": eachAnswer["text"],
#                 "isTrue": eachAnswer["isTrue"]
#             } for eachAnswer in each["answerList"]]
#         })
#     return returnArr

def getAllUsersAnswerList():  # 返回一个数组，每一个元素代表一个用户的答题情况，每一个元素是一个数组，数组中的每一个元素代表一个问题的答题情况，其中包含是否正确和答题时间
    # 数据库连接
    # 打开数据库连接
    db = pymysql.connect(host='rm-bp1bc34p4d5tr12n7uo.mysql.rds.aliyuncs.com',
                         port=3306,
                         user='pinnacle',
                         password='anEN4zwJmDha3fGBbuhzFE7p',
                         database='pinnacle')
    # db = pymysql.connect(host='127.0.0.1',
    #                      port=3306,
    #                      user='root',
    #                      password='1234',
    #                      database='pinnacle_template')
    # cursor = db.cursor()
    # 利用pandas读取数据库
    sql = "SELECT * FROM `users`"
    dfUsers = pd.read_sql(sql, db)
    sql = "SELECT * FROM `user_answers`"
    dfUserAnswers = pd.read_sql(sql, db)
    sql = "SELECT * FROM `question_sets`"
    dfQuestionSets = pd.read_sql(sql, db)
    # 选出所有的question_set_id
    questionSetUserAnswerArr = {}
    questionSetIDArr = dfUserAnswers['question_set_id'].unique()
    for eachQuestionSet in questionSetIDArr:
        # 从dfQuestionSets中选出当前question_set_id对应的name
        questionSetName = dfQuestionSets[dfQuestionSets['id'] == eachQuestionSet]['name'].values[0]
        questionSetUserAnswers = dfUserAnswers[dfUserAnswers['question_set_id'] == eachQuestionSet]
        # 筛选出所有的用户的答题数目
        # sql = "SELECT id FROM `users`"  # `pinnacle`.`user_answers`
        # cursor.execute(sql)
        # userIDArr = cursor.fetchall()
        # 读取pandas的数据
        userIDArr = dfUsers['id'].values
        # print(userIDArr)
        # print(len(userIDArr))
        # 去user_answers中查询每个用户的答题量，筛掉少于10次答题个数的用户id
        # 去除第一个用户，因为第一个用户是黑洞用户
        userIDArr = userIDArr[1:]
        tempUserIDArr = []
        # countArr = []
        for each in userIDArr:
            if len(each) != 0:
                # sql = "SELECT COUNT(*) FROM `user_answers` WHERE user_id = '%s'" % each
                # cursor.execute(sql)
                # count = cursor.fetchone()[0]
                # 读取pandas的数据
                count = questionSetUserAnswers[questionSetUserAnswers['user_id'] == each].shape[0]
                if count > 10:
                    tempUserIDArr.append(each)
        # 画图
        # plt.hist(countArr, bins=100)
        # plt.show()
        print("筛选掉了少于等于10次答题的用户，剩余用户数目为：", len(userIDArr), "，筛选掉了",
              len(userIDArr) - len(tempUserIDArr), "个用户")
        userIDArr = tempUserIDArr
        # print(userIDArr)
        # print(len(userIDArr))
        userAnswerArr = []
        for each in userIDArr:
            # sql = "SELECT * FROM `user_answers` WHERE user_id = '%s'" % each
            # cursor.execute(sql)
            # tempArr = cursor.fetchall()
            # 读取pandas的数据
            tempArr = questionSetUserAnswers[questionSetUserAnswers['user_id'] == each].values
            tempTempArr = []
            for eachTemp in tempArr:
                for eachTempTemp in tempTempArr:
                    if [eachTemp[5], eachTemp[6]] == eachTempTemp[1:3]:
                        break
                else:
                    tempTempArr.append([eachTemp[1], eachTemp[5], eachTemp[6], eachTemp[9]])
            tempArr = tempTempArr
            tempDict = dict()
            for eachAnswer in tempArr:
                # 将 eachAnswer[1]转换成数字类型的时间戳
                tempTime = eachAnswer[0].value // 60000000000
                if eachAnswer[2] not in tempDict:
                    tempDict[eachAnswer[2]] = [[eachAnswer[3], tempTime]]
                else:
                    tempDict[eachAnswer[2]].append([eachAnswer[3], tempTime])
            userAnswerArr.append(tempDict)
        questionSetUserAnswerArr[questionSetName] = userAnswerArr
    return questionSetUserAnswerArr


if __name__ == '__main__':
    questionSetUserAnswerArr = getAllUsersAnswerList()
    # 将变量userAnswerArr序列化到本地
    dirPath = "allUsersAnswers/"
    for each in questionSetUserAnswerArr.keys():
        with open(dirPath + each + '.pkl', 'wb') as f:
            pickle.dump(questionSetUserAnswerArr[each], f)
    # 将变量questionSetUserAnswerArr反序列化到本地
    # for each in questionSetUserAnswerArr.keys():
# temp = getAllQuestions()
