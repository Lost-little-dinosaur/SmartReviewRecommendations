import pickle
import pandas as pd
import pymysql
import requests


def main():
    header = {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJbmZvIjp7IlVJRCI6IjYwZDhiZmI4LTUwNDQtNDZjYS1iYTRlLWRkNjkwM2ZjNzk5MCIsIkluZm9Db21wbGV0ZSI6dHJ1ZSwiTGV2ZWwiOjF9LCJleHAiOjE2Nzc2NjExNDEsImlzcyI6Ik1KY2xvdWRzIn0.LwrLeRLblhNsQAFpfvt77-gUT_6y71GDwYSfU0ZjXRI"
    }
    db = pymysql.connect(host='rm-bp1bc34p4d5tr12n7uo.mysql.rds.aliyuncs.com',
                         port=3306,
                         user='pinnacle',
                         password='anEN4zwJmDha3fGBbuhzFE7p',
                         database='pinnacle')
    sql = "SELECT * FROM `question_sets`"
    dfQuestionSets = pd.read_sql(sql, db)
    questionSetIDArr = dfQuestionSets['id'].values
    for eachQuestionSetID in questionSetIDArr:
        i = 1
        questionSetName = dfQuestionSets[dfQuestionSets['id'] == eachQuestionSetID]['name'].values[0]
        try:
            allData = requests.get("https://api.pinnacle.mjclouds.com/questionSet/question/list?setID=" + str(
                eachQuestionSetID) + "&page=" + str(i) + "&limit=2000&withAnswer=True", headers=header).json()
            tempAllDataArr = allData['data']
            if len(tempAllDataArr) == 0:
                continue
            while len(allData["data"]) != 0:
                i += 1
                allData = requests.get("https://api.pinnacle.mjclouds.com/questionSet/question/list?setID=" + str(
                    eachQuestionSetID) + "&page=" + str(i) + "&limit=2000&withAnswer=True",
                                       headers=header).json()
                tempAllDataArr += allData['data']
            with open("QuestionSet/" + questionSetName + ".pkl", 'wb') as f:
                pickle.dump(tempAllDataArr, f)
        except Exception as e:
            print(e)
            print(questionSetName)
            continue


if __name__ == '__main__':
    main()
