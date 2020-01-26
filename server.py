from flask import Flask, escape, request

app = Flask(__name__)

multChoiceQuestionResponses = {
	'A':0,
	'B':0,
	'C':0,
	'D':0
}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    print("hello")
    return f'Hello, {escape(name)}!'

@app.route('/recordResponse/<questionType>/<response>', methods=['GET', 'POST'])
def recordResponse(questionType, response):
	if questionType == "multChoice":
		multChoiceQuestionResponses[response] += 1
	# elif questionType == "trueFalse":

	# else:

	return f'{escape(questionType)}'