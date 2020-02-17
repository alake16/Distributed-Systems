import requests
import json

class Metrics:

    @staticmethod
    def retrieveQuestionsByQuizName(quizName):
        #TODO Clean this url up -- url args should be added via variable or method
        #TODO Should return a status code, etc
        returnedResponse = requests.get("http://127.0.0.1:5000/allQuestionsByQuizName?quizName={}".format(quizName))

        print('the data returned is: {}'.format(returnedResponse.json()))
        return returnedResponse.json()