import pickle
import pandas as pd
import pymysql
import requests


def main():
    header = {
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJbmZvIjp7IlVJRCI6ImE4NThlNjQ4LTU3ZTMtNGU0Zi1iMmUxLWQ5NGVkZDVkMzYxMCIsIkluZm9Db21wbGV0ZSI6ZmFsc2UsIkxldmVsIjowfSwiZXhwIjoxNjcxMTIxOTU1LCJpc3MiOiJNSmNsb3VkcyJ9.YDCm01Rf1aM7PI4FUYa6PRLU5xsYlwKXxI8PsZ0g_fE"
    }
    db = pymysql.connect(host='sh-cdb-gn1fgn8u.sql.tencentcdb.com',
                         port=58976,
                         user='pinnacle_viewer',
                         password='VbfXD75GUh6u6ivFL9FMJrN4',
                         database='pinnacle')
    sql = "SELECT * FROM `question_sets`"
    dfQuestionSets = pd.read_sql(sql, db)
    questionSetIDArr = dfQuestionSets['id'].values
    for eachQuestionSetID in questionSetIDArr:
        i = 1
        questionSetName = dfQuestionSets[dfQuestionSets['id'] == eachQuestionSetID]['name'].values[0]
        allData = requests.get("https://api.pinnacle.mjclouds.com//questionSet/question/list?setID=" + str(
            eachQuestionSetID) + "&page=" + str(i) + "&limit=2000&withAnswer=True", headers=header).json()
        tempAllDataArr = allData['data']
        if len(tempAllDataArr) == 0:
            continue
        while len(allData["data"]) != 0:
            i += 1
            allData = requests.get("https://api.pinnacle.mjclouds.com//questionSet/question/list?setID=" + str(
                eachQuestionSetID) + "&page=" + str(i) + "&limit=2000&withAnswer=True",
                                   headers=header).json()
            tempAllDataArr += allData['data']
        with open("QuestionSet/" + questionSetName + ".pkl", 'wb') as f:
            pickle.dump(tempAllDataArr, f)


if __name__ == '__main__':
    main()
