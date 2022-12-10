import random


def simulation(userAnswerDict, nowTime, questionArr, questionNum, proportion, accuracyRate, seed):
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
    # y=31.8*(t/1460)^(-0.125)
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
    oldQuestionArr = random.sample(alternativeOldQuestionArr, oldQuestionNum)
    newQuestionNum = questionNum - oldQuestionNum
    newQuestionArr = random.sample(alternativeNewQuestionArr, newQuestionNum)
    # 答新题
    for question in newQuestionArr:
        if random.random() < accuracyRate:
            returnDict[question] = 1
        else:
            returnDict[question] = 0
    # 答旧题
    for question in oldQuestionArr:
        # 计算时间间隔  TODO
        # timeInterval = nowTime - userAnswerDict[question][0]
        # # 计算正确率
        # accuracyRate = 31.8 * (timeInterval / 1460) ** (-0.125)
        # if random.random() < accuracyRate:
        #     returnDict[question] = 1
        # else:
        #     returnDict[question] = 0


if __name__ == '__main__':
    simulation()
