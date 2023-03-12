import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from scipy.optimize import curve_fit
import math
from sklearn.cluster import KMeans

np.set_printoptions(threshold=np.inf)

dirPath_SAQSD = '../GetData/SeveralAnswerQuestionSetDict/'
dirPath_All_Correct_rate = '../GetData/AllQuestionsCorrectRate/'
dirpath_Allusers_Answers = '../GetData/AllUsersAnswers/'

##将所有用户的答题记录读入到AllAnswers中，此为字典结构
with open(dirPath_SAQSD + 'SeveralAnswerQuestionSetDict.pkl', 'rb') as f1:
    AllAnswerData = pickle.load(f1)



##将所有的题目正确率读入AllCorrectRate中
files = os.listdir(dirPath_All_Correct_rate)
AllCorrectRate = {}
for file in files:
    with open(dirPath_All_Correct_rate + file, 'rb') as f1:
        CorrectRate = pickle.load(f1)
        AllCorrectRate.update(CorrectRate)


# files = os.listdir(dirpath_Allusers_Answers)
# AllAnswers = {}
# for file in files:
#     with open(dirpath_Allusers_Answers + file, 'rb') as f2:
#         Answers = pickle.load(f2)
#         AllAnswers.update(Answers)

print(type(AllAnswerData[2]))
MaxTimeStamp = []

for key in AllAnswerData.keys():
    MaxTimeStamp.append(max(AllAnswerData[key][:(-key+1)]))
