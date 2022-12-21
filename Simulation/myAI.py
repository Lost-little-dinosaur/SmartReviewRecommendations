import pickle
import random
import time
from math import e

from matplotlib import pyplot as plt


# TODO 引入题库

def getQuestionSet(fileName):
    """
    从文件中读取题库
    :param fileName: 文件名
    :return: 题库
    """
    with open(fileName, 'rb') as f:
        questionSet = pickle.load(f)
    questionSetIDArr = list()
    for each in questionSet:
        questionSetIDArr.append(each["ID"])
    return questionSetIDArr


def smartSimulation(userAnswerDict, nowTime, questionArr, questionNum, proportion, accuracyRate, seed):
    """
    智能模拟用户答题
    :param userAnswerDict: 用户以前的答题情况字典
    :param nowTime: 现在的时间
    :param questionArr: 题库
    :param questionNum: 题目数量
    :param proportion: 新题目比例
    :param accuracyRate: 没做过的题的正确率
    :param seed: 随机数种子
    :return:
    returnDict: 返回的答题情况
    """
    if questionNum > len(questionArr):
        questionNum = len(questionArr)
    random.seed(seed)
    # 首先得到初始化函数
    # y = e**(aI * x + bI)
    returnDict = dict()
    alternativeOldQuestionArr = list()
    alternativeNewQuestionArr = list()
    for question in questionArr:
        if question in userAnswerDict.keys():
            alternativeOldQuestionArr.append(question)
        else:
            alternativeNewQuestionArr.append(question)
    # 根据比例选出旧的题目
    oldQuestionNum = int(questionNum * (100 - proportion) / 100)
    if oldQuestionNum > len(alternativeOldQuestionArr):
        oldQuestionNum = len(alternativeOldQuestionArr)
    newQuestionNum = questionNum - oldQuestionNum
    if newQuestionNum > len(alternativeNewQuestionArr):
        newQuestionNum = len(alternativeNewQuestionArr)
    newQuestionArr = random.sample(alternativeNewQuestionArr, newQuestionNum)
    # 答新题
    for question in newQuestionArr:
        if random.random() < accuracyRate:
            returnDict[question] = [[1, nowTime]]
        else:
            returnDict[question] = [[0, nowTime]]
    # 答旧题
    memoryRateArr = []
    for question in alternativeOldQuestionArr:
        # 计算时间间隔
        # 计算可能的正确率
        memoryRateArr.append(getMemoryRateArr(userAnswerDict[question], nowTime))
        # print(timeInterval, memoryRateArr[-1])
    # 根据memoryRateArr中的值，随机选出oldQuestionNum个题目
    for i in range(oldQuestionNum):
        tempJ = random.choices(range(len(memoryRateArr)), weights=memoryRateArr)[0]
        if random.random() <= (memoryRateArr[tempJ] + accuracyRate if memoryRateArr[tempJ] + accuracyRate < 1 else 1):
            userAnswerDict[alternativeOldQuestionArr[tempJ]].append([1, nowTime])
            returnDict[alternativeOldQuestionArr[tempJ]] = userAnswerDict[alternativeOldQuestionArr[tempJ]]
        else:
            userAnswerDict[alternativeOldQuestionArr[tempJ]].append([0, nowTime])
            returnDict[alternativeOldQuestionArr[tempJ]] = userAnswerDict[alternativeOldQuestionArr[tempJ]]
        memoryRateArr.pop(tempJ)
        alternativeOldQuestionArr.pop(tempJ)
    for question in userAnswerDict:
        if question not in returnDict.keys():
            returnDict[question] = userAnswerDict[question]
    return returnDict


def getMemoryRateArr(tempArr, nowTime):
    if len(tempArr) == 1:
        if tempArr[0][0] == 1:
            a = -1.4865132163367318e-07
            b = -0.06476805277713989
            y = 1 - e ** (a * (nowTime - tempArr[0][1]) + b)
        else:
            a = -5.033426596650367e-06
            b = -0.2784718873971984
            y = 1 - e ** (a * (nowTime - tempArr[0][1]) + b)
    else:
        if tempArr[-2][0] == 1 and tempArr[-1][0] == 1:
            # 计算出当前的记忆率
            a = -2.2515171935807575e-06
            b = -0.03234073841959593
            y = 1 - e ** (a * (nowTime - tempArr[-1][1]) + b)
        elif tempArr[-2][0] == 1 and tempArr[-1][0] == 0:
            a = -1.2467053258896204e-05
            b = -0.13903372905214134
            y = 1 - e ** (a * (nowTime - tempArr[-1][1]) + b)
        elif tempArr[-2][0] == 0 and tempArr[-1][0] == 1:
            a = -8.57839280720141e-06
            b = -0.0890746714685621
            y = 1 - e ** (a * (nowTime - tempArr[-1][1]) + b)
        else:
            a = -1.2833467689157539e-05
            b = -0.3447389387293679
            y = 1 - e ** (a * (nowTime - tempArr[-1][1]) + b)
    return y


def simulationAccuracyRate(userAnswerDict, nowTime, questionArr, accuracyRate):
    """
    测试该用户在特定题库下，特定正确率下，特定种子下，答题正确率
    :param userAnswerDict: 用户以前的答题情况字典
    :param nowTime: 现在的时间
    :param questionArr: 题库
    :param accuracyRate: 没做过的题的正确率
    :return:
    returnDict: 返回的答题情况
    """
    # 选出做过的题
    alternativeOldQuestionArr = list()
    for question in questionArr:
        if question in userAnswerDict.keys():
            alternativeOldQuestionArr.append(question)
    accuracyRateArr = [accuracyRate for i in range(len(questionArr) - len(alternativeOldQuestionArr))]
    for question in alternativeOldQuestionArr:
        # 计算可能的正确率
        accuracyRateArr.append(1 - getMemoryRateArr(userAnswerDict[question], nowTime))
    return sum(accuracyRateArr) / len(accuracyRateArr)


def randomSimulation(userAnswerDict, nowTime, questionArr, questionNum, proportion, accuracyRate, seed):
    """
    模拟用户答题
    :param userAnswerDict: 用户以前的答题情况字典
    :param nowTime: 现在的时间
    :param questionArr: 题库
    :param questionNum: 题目数量
    :param proportion: 新题目比例
    :param accuracyRate: 没做过的题的正确率
    :param seed: 随机数种子
    :return:
    returnDict: 返回的答题情况
    """
    if questionNum > len(questionArr):
        questionNum = len(questionArr)
    random.seed(seed)
    # 首先得到初始化函数
    # y = e**(aI * x + bI)
    returnDict = dict()
    alternativeOldQuestionArr = list()
    alternativeNewQuestionArr = list()
    for question in questionArr:
        if question in userAnswerDict.keys():
            alternativeOldQuestionArr.append(question)
        else:
            alternativeNewQuestionArr.append(question)
    # 根据比例选出旧的题目
    oldQuestionNum = int(questionNum * (100 - proportion) / 100)
    if oldQuestionNum > len(alternativeOldQuestionArr):
        oldQuestionNum = len(alternativeOldQuestionArr)
    newQuestionNum = questionNum - oldQuestionNum
    if newQuestionNum > len(alternativeNewQuestionArr):
        newQuestionNum = len(alternativeNewQuestionArr)
    newQuestionArr = random.sample(alternativeNewQuestionArr, newQuestionNum)
    # 答新题
    for question in newQuestionArr:
        if random.random() < accuracyRate:
            returnDict[question] = [[1, nowTime]]
        else:
            returnDict[question] = [[0, nowTime]]
    # 答旧题
    memoryRateArr = []
    for question in alternativeOldQuestionArr:
        # 计算时间间隔
        # 计算可能的正确率
        memoryRateArr.append(getMemoryRateArr(userAnswerDict[question], nowTime))
        # print(timeInterval, memoryRateArr[-1])
    # 根据memoryRateArr中的值，随机选出oldQuestionNum个题目
    for i in range(oldQuestionNum):
        tempJ = random.choices(range(len(memoryRateArr)))[0]
        if random.random() <= (memoryRateArr[tempJ] + accuracyRate if memoryRateArr[tempJ] + accuracyRate < 1 else 1):
            userAnswerDict[alternativeOldQuestionArr[tempJ]].append([1, nowTime])
            returnDict[alternativeOldQuestionArr[tempJ]] = userAnswerDict[alternativeOldQuestionArr[tempJ]]
        else:
            userAnswerDict[alternativeOldQuestionArr[tempJ]].append([0, nowTime])
            returnDict[alternativeOldQuestionArr[tempJ]] = userAnswerDict[alternativeOldQuestionArr[tempJ]]
        memoryRateArr.pop(tempJ)
        alternativeOldQuestionArr.pop(tempJ)
    for question in userAnswerDict:
        if question not in returnDict.keys():
            returnDict[question] = userAnswerDict[question]
    return returnDict


def doWrongSimulation(userAnswerDict, nowTime, questionArr, questionNum, proportion, accuracyRate, seed):
    if questionNum > len(questionArr):
        questionNum = len(questionArr)
    random.seed(seed)
    # 首先得到初始化函数
    # y = e**(aI * x + bI)
    returnDict = dict()
    alternativeOldQuestionArr = list()
    alternativeNewQuestionArr = list()
    for question in questionArr:
        if question in userAnswerDict.keys():
            alternativeOldQuestionArr.append(question)
        else:
            alternativeNewQuestionArr.append(question)
    # 根据比例选出旧的题目
    oldQuestionNum = int(questionNum * (100 - proportion) / 100)
    if oldQuestionNum > len(alternativeOldQuestionArr):
        oldQuestionNum = len(alternativeOldQuestionArr)
    newQuestionNum = questionNum - oldQuestionNum
    if newQuestionNum > len(alternativeNewQuestionArr):
        newQuestionNum = len(alternativeNewQuestionArr)
    newQuestionArr = random.sample(alternativeNewQuestionArr, newQuestionNum)
    # 答新题
    for question in newQuestionArr:
        if random.random() < accuracyRate:
            returnDict[question] = [[1, nowTime]]
        else:
            returnDict[question] = [[0, nowTime]]
    # 答旧题
    # print(timeInterval, memoryRateArr[-1])
    # 根据memoryRateArr中的值，随机选出oldQuestionNum个题目
    # 选出所有未曾做对的题目
    wrongQuestionArr = []
    for i in range(len(alternativeOldQuestionArr)):
        if 1 not in [each[0] for each in userAnswerDict[alternativeOldQuestionArr[i]]]:
            wrongQuestionArr.append(alternativeOldQuestionArr[i])
    if len(wrongQuestionArr) < oldQuestionNum:
        oldQuestionNum = len(wrongQuestionArr)
    memoryRateArr = []
    for question in wrongQuestionArr:
        # 计算时间间隔
        # 计算可能的正确率
        memoryRateArr.append(getMemoryRateArr(userAnswerDict[question], nowTime))
    for i in range(oldQuestionNum):
        tempJ = random.choices(range(len(memoryRateArr)))[0]
        if random.random() <= (memoryRateArr[tempJ] + accuracyRate if memoryRateArr[tempJ] + accuracyRate < 1 else 1):
            userAnswerDict[wrongQuestionArr[tempJ]].append([1, nowTime])
            returnDict[wrongQuestionArr[tempJ]] = userAnswerDict[wrongQuestionArr[tempJ]]
        else:
            userAnswerDict[wrongQuestionArr[tempJ]].append([0, nowTime])
            returnDict[wrongQuestionArr[tempJ]] = userAnswerDict[wrongQuestionArr[tempJ]]
        memoryRateArr.pop(tempJ)
        wrongQuestionArr.pop(tempJ)
    for question in userAnswerDict:
        if question not in returnDict.keys():
            returnDict[question] = userAnswerDict[question]
    return returnDict


def main(practiceDays, eachDayNum, proportion, seed, rightAccuracy):
    random.seed(seed)
    dirPath = "../GetData/AllUsersAnswers/"
    each = "2022年马原题库.pkl"
    with open(dirPath + each, 'rb') as f:
        allUsersAnswersArr = pickle.load(f)
    # 随即从中选出一个用户
    userAnswerDict = random.choice(allUsersAnswersArr)
    with open("tempUserAnswerDict.pkl", 'wb') as f:
        pickle.dump(userAnswerDict, f)
    with open("tempUserAnswerDict.pkl", 'rb') as f:
        userAnswerDict1 = pickle.load(f)
    # 选出一个题库
    dirPath = "../GetData/QuestionSet/"
    fileName = "2022年马原题库.pkl"
    questionSet = getQuestionSet(dirPath + fileName)
    nowTime = time.time() // 60
    smartSimulationResult = []
    for i in range(practiceDays):
        userAnswerDict1 = smartSimulation(userAnswerDict1, nowTime, questionSet, eachDayNum, proportion, rightAccuracy,
                                          seed)
        # 计算正确率
        smartSimulationResult.append(simulationAccuracyRate(userAnswerDict1, nowTime, questionSet, rightAccuracy))
        nowTime += 60 * 24

    nowTime = time.time() // 60
    with open("tempUserAnswerDict.pkl", 'rb') as f:
        userAnswerDict2 = pickle.load(f)
    randomSimulationResult = []
    for i in range(practiceDays):
        userAnswerDict2 = randomSimulation(userAnswerDict2, nowTime, questionSet, eachDayNum, proportion, rightAccuracy,
                                           seed)
        # 计算正确率
        randomSimulationResult.append(simulationAccuracyRate(userAnswerDict2, nowTime, questionSet, rightAccuracy))
        nowTime += 60 * 24

    nowTime = time.time() // 60
    with open("tempUserAnswerDict.pkl", 'rb') as f:
        userAnswerDict3 = pickle.load(f)
    doWrongSimulationResult = []
    for i in range(practiceDays):
        userAnswerDict3 = doWrongSimulation(userAnswerDict3, nowTime, questionSet, eachDayNum, proportion,
                                            rightAccuracy, seed)
        if userAnswerDict3 == -1:
            break
        # 计算正确率
        doWrongSimulationResult.append(simulationAccuracyRate(userAnswerDict3, nowTime, questionSet, rightAccuracy))
        nowTime += 60 * 24
    # 画图
    plt.plot(range(practiceDays), smartSimulationResult, label="smartSimulationResult")
    plt.plot(range(practiceDays), randomSimulationResult, label="randomSimulationResult")
    plt.plot(range(len(doWrongSimulationResult)), doWrongSimulationResult, label="doWrongSimulationResult")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    practiceDays = 10
    eachDayNum = 500
    proportion = 50
    seed = 1
    rightAccuracy = 0.5
    main(practiceDays, eachDayNum, proportion, seed, rightAccuracy)
