from typing import Dict
from flask import Flask, request, jsonify
from flask import Response as flaskResponse
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion, FillInTheBlankQuestion
from app.Models.Response import Response, MultipleChoiceResponse, FillInTheBlankResponse
import json
from app.JSONHandler import ProjectJSONEncoder

app = Flask(__name__)

activeQuestion = None

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'

@app.route('/activateQuestion', methods=['POST', 'GET'])
def activateQuestion():
    global activeQuestion

    if request.method == 'POST':
        if isinstance(activeQuestion, Question):
            return f'There is Already an Active Question!'
        data = request.json
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
    if activeQuestion is not None:
        responses = activeQuestion._responses
        responses = fetchResponses()
        activeQuestion = None
        return responses
    return f'No Active Question!'

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
    global activeQuestion
    if isinstance(activeQuestion, MultipleChoiceQuestion):
        data = request.json
        response = Response.create_a_response(data)
        activeQuestion.add_response(response)
        return jsonify(data)
    return f'No Active Question!'
