import os
from math import exp
import json
import pickle


def getTwoThreeAnswerList():
    severalAnswerQuestionSetDict = {}
    dirPath = "AllUsersAnswers/"
    for each in os.listdir(dirPath):
        with open(dirPath + each, 'rb') as f:
            questionSetUserAnswerArr = pickle.load(f)
            # print(questionSetUserAnswerArr)
            for eachUserAnswer in questionSetUserAnswerArr:
                for eachQuestionID in eachUserAnswer.keys():
                    tempArr = eachUserAnswer[eachQuestionID]
                    # 按照时间戳升序排序
                    tempArr.sort(key=lambda x: x[1])
                    answerCount = len(eachUserAnswer[eachQuestionID])
                    for nowAnswerCount in range(2, answerCount + 1):
                        processSeveralAnswer(tempArr[:nowAnswerCount], nowAnswerCount, severalAnswerQuestionSetDict,
                                             eachQuestionID)

    return severalAnswerQuestionSetDict


def processSeveralAnswer(answerArr, nowAnswerCount, severalAnswerQuestionSetDict, eachQuestionID):
    if nowAnswerCount not in severalAnswerQuestionSetDict.keys():
        severalAnswerQuestionSetDict[nowAnswerCount] = []
    tempArr = []
    for i in range(nowAnswerCount):
        tempArr.append(answerArr[i][0])
    for i in range(nowAnswerCount - 1):
        tempArr.append(answerArr[i + 1][1] - answerArr[i][1])
    severalAnswerQuestionSetDict[nowAnswerCount].append({eachQuestionID: tempArr})


if __name__ == '__main__':
    # 第一层是题库，第二层是每道题的答题记录数组，这个数组里依次存放的是[第一次正确与否、第二次正确与否、第三次正确与否、第一次与第二次的时间间隔、第二次与第三次的时间间隔]
    severalAnswerQuestionSetDict = getTwoThreeAnswerList()  # 第一层是题库，第二层是每道题的答题记录数组，这个数组里依次存放的是[第一次正确与否、第二次正确与否、第三次正确与否、第一次与第二次的时间间隔、第二次与第三次的时间间隔]
    # 将变量userAnswerArr序列化到本地
    dirPath = "SeveralAnswerQuestionSetDict/"
    with open(dirPath + "SeveralAnswerQuestionSetDict.pkl", 'wb') as f:
        pickle.dump(severalAnswerQuestionSetDict, f)
