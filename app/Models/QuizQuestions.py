class QuizQuestions:
    questions = []

    def __init__(self, questions):
        self.questions = questions

    def getQuestions():
        return questions

    def setQuestions(questions):
        self.questions = questions

    @property
    def json_data(self):
        return {'questions': self.questions}