import os
from math import exp
import json
import pickle


def getTwoThreeAnswerList():
    twoAnswerQuestionSetDict = {}
    threeAnswerQuestionSetDict = {}
    dirPath = "AllUsersAnswers/"
    for each in os.listdir(dirPath):
        with open(dirPath + each, 'rb') as f:

            twoAnswerArr = []
            threeAnswerArr = []
            questionSetUserAnswerArr = pickle.load(f)
            # print(questionSetUserAnswerArr)
            for eachUserAnswer in questionSetUserAnswerArr:
                for eachQuestion in eachUserAnswer.keys():
                    if len(eachUserAnswer[eachQuestion]) == 2:
                        tempArr = eachUserAnswer[eachQuestion]
                        # 按照时间戳升序排序
                        tempArr.sort(key=lambda x: x[1])
                        twoAnswerArr.append([tempArr[0][0], tempArr[1][0], tempArr[1][1] - tempArr[0][1]])
                    elif len(eachUserAnswer[eachQuestion]) >= 3:
                        tempArr = eachUserAnswer[eachQuestion]
                        # 按照时间戳排序
                        tempArr.sort(key=lambda x: x[1])
                        tempArr2 = tempArr[0:2]
                        twoAnswerArr.append([tempArr2[0][0], tempArr2[1][0], tempArr2[1][1] - tempArr2[0][1]])
                        tempArr3 = tempArr[0:3]
                        threeAnswerArr.append(
                            [tempArr3[0][0], tempArr3[1][0], tempArr3[2][0], tempArr3[1][1] - tempArr3[0][1],
                             tempArr3[2][1] - tempArr3[1][1]])
            twoAnswerQuestionSetDict[each] = twoAnswerArr
            threeAnswerQuestionSetDict[each] = threeAnswerArr
    return twoAnswerQuestionSetDict, threeAnswerQuestionSetDict


if __name__ == '__main__':
    twoAnswerQuestionSetDict, threeAnswerQuestionSetDict = getTwoThreeAnswerList()
    # 将变量userAnswerArr序列化到本地
    dirPath = "TwoThreeAnswerQuestionSetDict/"
    filePath = "TwoAnswerList.pkl"
    with open(dirPath + filePath, 'wb') as f:
        pickle.dump(twoAnswerQuestionSetDict, f)
    filePath = "ThreeAnswerList.pkl"
    with open(dirPath + filePath, 'wb') as f:
        pickle.dump(threeAnswerQuestionSetDict, f)
