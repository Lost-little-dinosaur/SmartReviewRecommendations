import pandas as pd
import pymysql
import pickle


def getAllQuestionsCorrectRate():
    # 数据库连接
    # 打开数据库连接
    # db = pymysql.connect(host='rm-bp1bc34p4d5tr12n7uo.mysql.rds.aliyuncs.com',
    #                      port=3306,
    #                      user='pinnacle',
    #                      password='anEN4zwJmDha3fGBbuhzFE7p',
    #                      database='pinnacle')
    db = pymysql.connect(host='127.0.0.1',
                         port=3306,
                         user='root',
                         password='1234',
                         database='pinnacle_test')
    # 利用pandas读取数据库
    sql = "SELECT * FROM `users`"
    dfUsers = pd.read_sql(sql, db)
    sql = "SELECT * FROM `user_answers`"
    dfUserAnswers = pd.read_sql(sql, db)
    sql = "SELECT * FROM `question_sets`"
    dfQuestionSets = pd.read_sql(sql, db)

    # 筛选出所有的用户的答题数目，去除第一个用户，因为第一个用户是黑洞用户
    userIDArr = dfUsers['id'].values[1:]
    # 选出所有的question_set_id
    questionSetQuestionsCorrectRateDict = {}
    questionSetIDArr = dfUserAnswers['question_set_id'].unique()
    for eachQuestionSet in questionSetIDArr:
        # 从dfQuestionSets中选出当前question_set_id对应的name
        questionSetName = dfQuestionSets[dfQuestionSets['id'] == eachQuestionSet]['name'].values[0]
        # 每道题只取每个用户的第一次答题记录
        questionSetUserAnswers = dfUserAnswers[dfUserAnswers['question_set_id'] == eachQuestionSet].sort_values(
            by=['created_at']).drop_duplicates(subset=['user_id', 'question_id'], keep='first')
        questionsCorrectRateDict = {}
        for eachQuestion in questionSetUserAnswers['question_id'].unique():
            # 选出当前question_id对应的所有答题记录
            questionUserAnswers = questionSetUserAnswers[questionSetUserAnswers['question_id'] == eachQuestion]
            if len(questionUserAnswers) > 10:  # 答题数目大于10才计算正确率
                # 选出当前question_id对应的所有答题记录中的正确答题记录
                questionUserCorrectAnswers = questionUserAnswers[questionUserAnswers['question_correct'] == 1]
                # 计算正确率
                correctRate = len(questionUserCorrectAnswers) / len(questionUserAnswers)
                # 将正确率存入字典
                questionsCorrectRateDict[eachQuestion] = [correctRate, len(questionUserAnswers)]  # [正确率，答题数目]
        # 将字典存入字典
        questionSetQuestionsCorrectRateDict[questionSetName] = questionsCorrectRateDict
    return questionSetQuestionsCorrectRateDict


if __name__ == '__main__':
    # 序列化到本地
    dirPath = "AllQuestionsCorrectRate"
    questionSetQuestionsCorrectRateDict = getAllQuestionsCorrectRate()
    for eachQuestionSet in questionSetQuestionsCorrectRateDict:
        with open(dirPath + "\\" + eachQuestionSet + ".pkl", 'wb') as f:
            pickle.dump(questionSetQuestionsCorrectRateDict[eachQuestionSet], f)
