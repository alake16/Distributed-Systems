from os import listdir, getcwd
from os.path import isfile, join
from app.Models.Quiz import Quiz
from app.StorageHandler import load_file_as_json

def fetchAllUntakenQuizNames():
	path = getcwd() + "/../quizzes/untaken/"
	return [f.replace('.json','') for f in listdir(path) if isfile(join(path, f))]

def loadQuizFromName(quizName):
	quizJson = load_file_as_json(getcwd() + "/../quizzes/untaken/" + quizName + '.json')
	return Quiz.load_quiz_from_json(quizJson)
