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
        if data["type"] == "multiple_choice":
            activeQuestion = MultipleChoiceQuestion(prompt=data["prompt"], choices=data["choices"],
                                                    answer=data["answer"])
        elif data["type"] == "fill_in_the_blank":
            activeQuestion = FillInTheBlankQuestion(before_prompt=data["before_prompt"],
                                                    after_prompt=data["after_prompt"],
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

'''
Implement a method that allows us to track each incoming
response for each answer

'''
@app.route('/trackResponse', methods=['POST'])
def trackResponse():
    global activeQuestion
    if activeQuestion is not None:
        pass

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
    global activeQuestion
    if isinstance(activeQuestion, MultipleChoiceQuestion):
        data = request.json
        activeQuestion.add_response(MultipleChoiceResponse(choice=data["choice"],
                                                           user_id=data["user_id"],
                                                           nickname=data["nickname"]))
        return jsonify(data)
    elif isinstance(activeQuestion, FillInTheBlankQuestion):
        data = request.json
        activeQuestion.add_response(FillInTheBlankResponse(blank_answer=data["answer"],
                                                           user_id=data["userID"],
                                                           nickname=data["nickname"]))
        return jsonify(data)
    return f'No Active Question!'
