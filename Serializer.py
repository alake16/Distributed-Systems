
def serializePlaintextQuestionToXML(plainTextQuestion):
    openingTag = '<Question>'
    closingTag = '</Question>'
    questionAsXML = openingTag + plainTextQuestion + closingTag
    return questionAsXML

def serializePlaintextAnswerToXML(plainTextAnswer):
    openingTag = '<Answer>'
    closingTag = '</Answer>'
    answerAsXML = openingTag + plainTextAnswer + closingTag
    return answerAsXML

def generateSerializedOutputFile(questions, answers):
    print('Hello, from the Serializer.')