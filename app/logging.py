from time import time
import json

def createResponseFile(quizID, quizName):
	open("../responses/" + quizID + "_" + quizName, "w+")

def logResponse(quizID, quizName, response):
    with open("../responses/" + quizID + "_" + quizName,'w') as f: 
        json.dump(response, f, indent=4)
