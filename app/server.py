from typing import Dict
from flask import Flask, request, jsonify
from flask import Response as flaskResponse
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion, FillInTheBlankQuestion
from app.Models.Response import Response, MultipleChoiceResponse, FillInTheBlankResponse
import json
from app.Models.QuizQuestions import QuizQuestions
from app.JSONHandler import ProjectJSONEncoder

app = Flask(__name__)

activeQuestion = None
currentQuizName = None

'''
Will store all of the instructor's posed questions
-- which, in turn, also provides a list of all the
answer choices and answers.
'''
allQuestionsForCurrentQuiz = []

allQuestionsByQuizName = {}

@app.route('/')
def welcome():
    """ Renders a welcome page for the user."""
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'


@app.route('/activateQuestion', methods=['POST', 'GET'])
def activateQuestion():
    """Takes the POST request containing question data and marks that question as active if there is not an active
    question. Takes the GET request and returns the active question.
     Subject to change:

     1) activeQuestion may no longer be global
     2) This may require authentication
     3) The GET request may be routed to a separate function such as active_question
     """
    global activeQuestion
    global currentQuizName
    currentQuizName = request.args['quizName']
    print('quizName should be printed below.')
    print('quizName: {}'.format(currentQuizName))

    if request.method == 'POST':
        print('received the following payload: {}'.format(request.json))
        if isinstance(activeQuestion, Question):
            return f'There is Already an Active Question!'
        data = request.json
        print('sending the json payload to the Question.create_a_question() method')
        activeQuestion = Question.create_a_question(data)
        return flaskResponse(json.dumps(activeQuestion, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})

    else:
        if activeQuestion is not None:
            return flaskResponse(json.dumps(activeQuestion, cls=ProjectJSONEncoder), 200,
                                 {'Content-Type': 'application/json'})
        else:
            return f'No Question Active!'


@app.route('/fetchResponses', methods=['GET'])
def fetchResponses():
    """Returns the list of responses to the active question as JSON."""
    global activeQuestion
    if activeQuestion is not None:
        return flaskResponse(json.dumps(activeQuestion.get_responses(), cls=ProjectJSONEncoder),
                             mimetype='application/json')
    return f'No Active Question!'


@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
    """
    Deactivates a question if it is active.
    :return:
    """
    global activeQuestion

    #If the quizName is found, simply add the currentQuestion to the quiz's list of Questions
    if currentQuizName in allQuestionsByQuizName:
        allQuestionsByQuizName[currentQuizName].append(activeQuestion)
    else:
        #create a new key entry in the dictionary with the currentQuizName
        '''
        Store the question object in the list of allQuestions.
        This is done now (when the question is being deactivated)
        in order to aggregate the student responses and present
        the question's metrics on the instructor UI.
        '''
        allQuestionsForCurrentQuiz.append(activeQuestion)
        allQuestionsByQuizName[currentQuizName] = allQuestionsForCurrentQuiz.copy()
        allQuestionsForCurrentQuiz.clear()

    if activeQuestion is not None:
        responses = activeQuestion._responses
        responses = fetchResponses()
        activeQuestion = None
        return responses
    return f'No Active Question!'


@app.route('/recordResponse', methods=['POST'])
def recordResponse():
    """
    Takes the user's POST request and records that as a response on the active question.
    :return:
    """
    global activeQuestion
    print('received the following payload: {}'.format(request.json))
    if isinstance(activeQuestion, MultipleChoiceQuestion):
        data = request.json
        response = Response.create_a_response(data, activeQuestion.object_id)
        activeQuestion.add_response(response)
        return flaskResponse(json.dumps(data, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})
    return f'No Active Question!'

#TODO flesh out logic -- what happens if not found?
def findQuestionsByQuizName(quizName):
    print('Looking for quizName: {}'.format(quizName))
    questions = allQuestionsByQuizName.get(quizName)
    return questions


'''
Returns all of the questions posed by the instructor.

TODO: These should eventually be queried by sessionId and quizName.
TODO: These should also eventually be stored in a database.
'''
@app.route('/allQuestionsByQuizName', methods=['GET'])
def retrievCounts():
    quizName = request.args['quizName']
    allQuestionsForQuiz = findQuestionsByQuizName(quizName)
    quizQuestions = QuizQuestions(allQuestionsForQuiz)

    return flaskResponse(json.dumps(quizQuestions, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})
