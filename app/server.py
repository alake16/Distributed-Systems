from typing import Dict
from flask import Flask, request, jsonify
from flask import Response as flaskResponse
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion
from app.Models.Response import Response, MultipleChoiceResponse
import json
from app.JSONHandler import ProjectJSONEncoder


app = Flask(__name__)

activeQuestion = None
responses_tracker = 0

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'


# Starting route to receive responses
@app.route('/activateQuestion', methods=['POST', 'GET'])
def activateQuestion():
    global activeQuestion, responses_tracker

    if request.method == 'POST':
        if isinstance(activeQuestion, Question):
            return f'There is Already an Active Question!'
        data = request.json
        if data["type"] == "multiple_choice":
            
            activeQuestion = MultipleChoiceQuestion(prompt=data["prompt"], choices=data["choices"],
                                                    answer=data["answer"])
        else:
            activeQuestion = MatchingQuestion(prompt=data["prompt"],
                                              left_choices=data["leftChoices"],
                                              right_choices=data["rightChoices"],
                                              answer_mapping=data["answerMapping"])
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
    global activeQuestion, responses_tracker
    if activeQuestion is not None:
        responses = flaskResponse(json.dumps(activeQuestion.get_responses(), cls=ProjectJSONEncoder), mimetype='application/json')
        return "NUMBER OF RESPONSES: {}\n\n{}".format(responses_tracker, responses)
    return f'No Active '


@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
    global activeQuestion
    if activeQuestion is not None:
        responses = activeQuestion.responses
        responses = fetchResponses()
        activeQuestion = None
        return responses
    return f'No Active Question!'

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
    global activeQuestion, responses_tracker
    if isinstance(activeQuestion, MultipleChoiceQuestion):
        data = request.json
        responses_tracker +=1
        activeQuestion.add_response(
            MultipleChoiceResponse(user_id=data["user_id"], nickname=data["nickname"], choice=data["choice"]))
        return jsonify(data)
    return f'No Active Question!'


