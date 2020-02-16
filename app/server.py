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
        #return jsonify(data) # Err thrown -- "AttributeError: 'Request' object has no attribute 'is_xhr'" TODO: Needs team review 
        return flaskResponse(json.dumps(data, cls=ProjectJSONEncoder), 200,
                             {'Content-Type': 'application/json'})
    return f'No Active Question!'
