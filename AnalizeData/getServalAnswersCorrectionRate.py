import os
import pickle


def main():
    # 首先读取数据
    dirPath = "../GetData/SeveralAnswerQuestionSetDict/"
    for each in os.listdir(dirPath):
        with open(dirPath + each, 'rb') as f:
            SeveralAnswerQuestionSetDict = pickle.load(f)
            # print(tempSeveralAnswerArr)

    allSituationsCorrectRate = {}
    for eachAnswerQuestionSetDict in SeveralAnswerQuestionSetDict:
        allSituationsCorrectRate[eachAnswerQuestionSetDict] = getThisSituationCorrectRate(
            SeveralAnswerQuestionSetDict[eachAnswerQuestionSetDict])
    print(allSituationsCorrectRate)  # 得到了所有情况的正确率

    classifySituationsCorrectRate = {}
    for eachAnswerQuestionSetDict in SeveralAnswerQuestionSetDict:
        classifySituationsCorrectRate[eachAnswerQuestionSetDict] = classifyThisSituationCorrectRate(
            allSituationsCorrectRate[eachAnswerQuestionSetDict])
    print(classifySituationsCorrectRate)  # 对所有情况的正确率进行分类

    # 计算方差
    varianceSituationsCorrectRate = {}
    for eachAnswerQuestionSetDict in SeveralAnswerQuestionSetDict:
        varianceSituationsCorrectRate[eachAnswerQuestionSetDict] = {}
        for eachClassify in classifySituationsCorrectRate[eachAnswerQuestionSetDict].keys():
            varianceSituationsCorrectRate[eachAnswerQuestionSetDict][eachClassify] = getVariance(
                classifySituationsCorrectRate[eachAnswerQuestionSetDict][eachClassify])
    print(varianceSituationsCorrectRate)  # 得到了所有情况的正确率的方差


def getThisSituationCorrectRate(thisSituationAnswerList):  # 获取所有情况的正确率
    nowCount = (len(thisSituationAnswerList[0]) + 1) // 2 - 1
    correctRateDictOfSituations = {}
    correctDictOfSituations = {}
    answerCountDictOfSituations = {}
    for eachAnswer in thisSituationAnswerList:
        if str(eachAnswer[:nowCount]) not in answerCountDictOfSituations.keys():
            answerCountDictOfSituations[str(eachAnswer[:nowCount])] = 1
            correctDictOfSituations[str(eachAnswer[:nowCount])] = 0
            correctRateDictOfSituations[str(eachAnswer[:nowCount])] = 0
        else:
            answerCountDictOfSituations[str(eachAnswer[:nowCount])] += 1
        correctDictOfSituations[str(eachAnswer[:nowCount])] += eachAnswer[nowCount]
    for eachSituation in answerCountDictOfSituations.keys():
        correctRateDictOfSituations[eachSituation] = correctDictOfSituations[eachSituation] / \
                                                     answerCountDictOfSituations[eachSituation]
    return correctRateDictOfSituations


def classifyThisSituationCorrectRate(thisSituationCorrectRateDict):  # 将正确率分类
    classifyCorrectRateDict = {}
    for eachSituation in thisSituationCorrectRateDict.keys():
        tempKey = "对" + str(eachSituation.count("1")) + "题"
        if tempKey not in classifyCorrectRateDict.keys():
            classifyCorrectRateDict[tempKey] = [thisSituationCorrectRateDict[eachSituation]]
        else:
            classifyCorrectRateDict[tempKey].append(
                thisSituationCorrectRateDict[eachSituation])
    return classifyCorrectRateDict


def getVariance(thisSituationClassifyCorrectRateList):  # 计算方差
    sum = 0
    for eachCorrectRate in thisSituationClassifyCorrectRateList:
        sum += eachCorrectRate
    average = sum / len(thisSituationClassifyCorrectRateList)
    sum = 0
    for eachCorrectRate in thisSituationClassifyCorrectRateList:
        sum += (eachCorrectRate - average) ** 2
    return sum / len(thisSituationClassifyCorrectRateList)


if __name__ == '__main__':
    main()
