import json

class QuizQuestions:

    def __init__(self, questionsList):
        self.questionsList = questionsList

    def getQuestions(self):
        return self.questionsList

    def setQuestions(self, questionsList):
        self.questionsList = questionsList

    @property
    def json_data(self):
        return {'questions': self.questionsList}         