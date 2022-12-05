from static import jsonData


def getAllQuestions():
    returnArr = []
    for each in jsonData["data"]:
        returnArr.append({
            "ID": each["ID"],
            "text": each["text"],
            "answerList": [{
                "text": eachAnswer["text"],
                "isTrue": eachAnswer["isTrue"]
            } for eachAnswer in each["answerList"]]
        })
    return returnArr


if __name__ == '__main__':
    temp = getAllQuestions()
    print(temp)
