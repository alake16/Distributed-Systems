from flask import Flask, escape, request, jsonify
from app.Questions import Question, MultipleChoiceQuestion, MatchingQuestion

app = Flask(__name__)

activeMultipleChoiceQuestion = None
activeMatchingQuestion = None

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    print("hello")
    return f'Welcome to Quiz API v1!'

@app.route('/activateQuestion', methods=['POST'])
def activateQuestion():
	data = request.json
	if data["questionType"] == "multChoice":
		global activeMultipleChoiceQuestion
		activeMultipleChoiceQuestion = MultipleChoiceQuestion(prompt=data["prompt"], choices=data["choices"], answer=data["answer"])
	else:
		global activeMatchingQuestion
		activeMatchingQuestion = MatchingQuestion(prompt=data["prompt"], left_choices=data["leftChoices"], right_choices=data["rightChoices"], answer=data["answer"])
	return jsonify(data)

@app.route('/fetchResponses', methods=['GET'])
def fetchResponses():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None:
		return activeMultipleChoiceQuestion.responses
	elif activeMatchingQuestion is not None:
		return activeMatchingQuestion.responses
	return f'No Active Question!'

@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	questionType = ""
	if activeMultipleChoiceQuestion is not None:
		activeMultipleChoiceQuestion = None
		return f'Multiple Choice Question Deactivated!'
	elif activeMatchingQuestion is not None:
		activeMatchingQuestion = None
		questionType = "Matching Question Deactivated!"
	return f'No Question Was Active!'

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
	global activeMultipleChoiceQuestion
	if activeMultipleChoiceQuestion:
		activeMultipleChoiceQuestion.responses[request.json["response"]] += 1
		return jsonify(activeMultipleChoiceQuestion.responses)
	return f'No Active Question!'
