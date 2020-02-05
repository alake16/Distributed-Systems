from flask import Flask, escape, request, jsonify
from app.Questions import Question, MultipleChoiceQuestion, MatchingQuestion

app = Flask(__name__)

activeMultipleChoiceQuestion = None
activeMatchingQuestion = None

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'

@app.route('/activateQuestion', methods=['POST', 'GET'])
def activateQuestion():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion

	if request.method == 'POST':
		if activeMultipleChoiceQuestion is not None or activeMatchingQuestion is not None:
			return f'There is Already an Active Question!'
		data = request.json
		if data["type"] == "multiple_choice":
			activeMultipleChoiceQuestion = MultipleChoiceQuestion(prompt=data["prompt"], choices=data["choices"], answer=data["answer"])
		else:
			activeMatchingQuestion = MatchingQuestion(prompt=data["prompt"], left_choices=data["leftChoices"], right_choices=data["rightChoices"], answer_mapping=data["answerMapping"])
		return jsonify(data)

	else:
		if activeMultipleChoiceQuestion is not None:
			return activeMultipleChoiceQuestion.jsonify()
		elif activeMatchingQuestion is not None:
			return activeMatchingQuestion.jsonfiy()


@app.route('/fetchResponses', methods=['GET'])
def fetchResponses():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None:
		return jsonify(activeMultipleChoiceQuestion.responses)
	elif activeMatchingQuestion is not None:
		return jsonify(activeMatchingQuestion.responses)
	return f'No Active Question!'

@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None:
		responses = activeMultipleChoiceQuestion.responses
		activeMultipleChoiceQuestion = None
		return jsonify(responses)
	if activeMatchingQuestion is not None:
		responses = activeMatchingQuestion.responses
		activeMatchingQuestion = None
		return f'Matching Question Deactivated!'
	return f'No Question Was Active!'

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
	global activeMultipleChoiceQuestion
	if activeMultipleChoiceQuestion:
		activeMultipleChoiceQuestion.responses.append(request.json)
		return jsonify(request.json)
	return f'No Active Question!'
