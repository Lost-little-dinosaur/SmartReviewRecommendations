import json

if __name__ == '__main__':
    # 将变量userAnswerArr反序列化到本地
    with open('userAnswerArr.txt', 'r') as f:
        userAnswerArr = json.loads(f.read())
    print(userAnswerArr)  # 返回一个数组，每一个元素代表一个用户的答题情况，每一个元素是一个数组，数组中的每一个元素代表一个问题的答题情况，其中包含是否正确和答题时间
