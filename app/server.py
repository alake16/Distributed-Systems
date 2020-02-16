from typing import Dict
from flask import Flask, request, jsonify
from flask import Response as flaskResponse
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion, FillInTheBlankQuestion
from app.Models.Response import Response, MultipleChoiceResponse, FillInTheBlankResponse
import json
from app.JSONHandler import ProjectJSONEncoder

app = Flask(__name__)

activeQuestion = None

'''
Will store all of the instructor's posed questions
-- which, in turn, also provides a list of all the
answer choices and answers.
'''
allQuestions = []

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'


@app.route('/activateQuestion', methods=['POST', 'GET'])
def activateQuestion():
    global activeQuestion

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
    global activeQuestion
    if activeQuestion is not None:
        return flaskResponse(json.dumps(activeQuestion.get_responses(), cls=ProjectJSONEncoder),
                             mimetype='application/json')
    return f'No Active Question!'


@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
    global activeQuestion

    '''
    Store the question object in the list of allQuestions.
    This is done now (when the question is being deactivated)
    in order to aggregate the student responses and present
    the question's metrics on the instructor UI.
    '''
    allQuestions.append(activeQuestion)

    if activeQuestion is not None:
        responses = activeQuestion._responses
        responses = fetchResponses()
        activeQuestion = None
        return responses
    return f'No Active Question!'


@app.route('/recordResponse', methods=['POST'])
def recordResponse():
    global activeQuestion
    print('received the following payload: {}'.format(request.json))
    if isinstance(activeQuestion, MultipleChoiceQuestion):
        data = request.json
        response = Response.create_a_response(data, activeQuestion.object_id)
        activeQuestion.add_response(response)
        return flaskResponse(json.dumps(data, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})
    return f'No Active Question!'

'''
Returns all of the questions posed by the instructor.

TODO: These should eventually be queried by sessionId and quizName.
TODO: These should also eventually be stored in a database.
'''
@app.route('/allQuestion', methods=['GET'])
def retrievCounts():
    return flaskResponse(json.dumps(allQuestions, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})
