def serializePlaintextQuestionToXML(plainTextQuestion):
    openingTag = '\t\t<Question>'
    closingTag = '</Question>\n'
    questionAsXML = openingTag + plainTextQuestion + closingTag
    return questionAsXML


def serializePlaintextAnswerToXML(plainTextAnswer):
    openingTag = '\t\t<Answer>'
    closingTag = '</Answer>\n'
    answerAsXML = openingTag + plainTextAnswer + closingTag
    return answerAsXML


def generateQuestionAnswerEntry(question, answer):
    ENTRY_NODE_OPENING_TAG = '\t<Entry>\n'
    ENTRY_NODE_CLOSING_TAG = '\t</Entry>\n'

    SERIALIZED_QUESTION = serializePlaintextQuestionToXML(question)
    SERIALIZED_ANSWER = serializePlaintextAnswerToXML(answer)

    fullEntryAsXML = ENTRY_NODE_OPENING_TAG + SERIALIZED_QUESTION + SERIALIZED_ANSWER + ENTRY_NODE_CLOSING_TAG

    return fullEntryAsXML


def generateSerializedOutputFile(questions, answers):
    with open('output.xml', 'w') as outputFile:
        ROOT_NODE_OPENING_TAG = '<Quiz>\n'
        ROOT_NODE_CLOSING_TAG = '</Quiz>\n'

        outputFile.write(ROOT_NODE_OPENING_TAG)
        for i in range(0, len(questions)):
            outputFile.write(generateQuestionAnswerEntry(questions[i], answers[i]))
        outputFile.write(ROOT_NODE_CLOSING_TAG)