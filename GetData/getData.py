import pickle
import os

if __name__ == '__main__':
    # dirPath = "AllUsersAnswers/"
    # for each in os.listdir(dirPath):
    #     with open(dirPath + each, 'rb') as f:
    #         questionSetUserAnswerArr = pickle.load(f)
    #         print(questionSetUserAnswerArr)
    dirPath = "TwoThreeAnswerQuestionSetDict/"
    for each in os.listdir(dirPath):
        with open(dirPath + each, 'rb') as f:
            eachData = pickle.load(f)
            print(eachData)
