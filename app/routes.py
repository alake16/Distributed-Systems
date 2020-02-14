from flask import Flask, request, render_template, redirect, url_for, flash
from app.forms import NewQuizForm, MultipleChoiceQuestionForm, FillInTheBlankQuestionForm, FillInTheBlankAnswerForm, MultipleChoiceAnswerForm, form_factory
from app.Models.Quiz import Quiz
from app.Models.Questions import Question, MultipleChoiceQuestion, FillInTheBlankQuestion
from app.Models.Response import MultipleChoiceResponse, FillInTheBlankResponse
from app.helpers import fetchAllUntakenQuizNames, loadQuizFromName
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

createdQuiz = None
activeQuiz = None
activeQuestion = None
activeQuestionNumber = -1

# General Landing Page
@app.route('/')
def index():
    return render_template("index.html", title="Home")

# Admin Landing Page
@app.route('/admin')
def admin():
    return render_template("admin.html", title="Administrator")

# ===== Quiz Creation Routes =====

# Quiz Creator Page
@app.route('/createQuiz', methods=['GET', 'POST'])
def createQuiz():
    global createdQuiz
    form = NewQuizForm()
    if form.validate_on_submit():
        flash("New Quiz Created")
        createdQuiz = Quiz(name=form.name.data)
        return redirect(url_for("addQuestions", quizName=createdQuiz.name))
    return render_template("createQuiz.html", title="Create a Quiz", form=form)

# Question Creator Landing Page
@app.route('/addQuestions/<quizName>')
def addQuestions(quizName):
    return render_template("addQuestions.html", title="Add Questions to " + quizName,
                           quizName=quizName, quiz=createdQuiz)

# Specific Question Type Creator
@app.route('/addQuestion/<questionType>', methods=['GET', 'POST'])
def addQuestion(questionType):
    global createdQuiz
    if createdQuiz is not None:
        if questionType in ['multiple_choice', 'fill_in_the_blank']:
            form = form_factory(questionType)
            if form.validate_on_submit():
                question_data = form.json_data
                question = Question.create_a_question(question_data)
                createdQuiz.add_question_to_quiz(question=question)
                return redirect(url_for("addQuestions", quizName=createdQuiz.name))
            return render_template('new_' + questionType + '_question.html', title="Add " + questionType +
                                   " Question", quizName=createdQuiz.name, form=form)

# Quiz Session Creator Page
@app.route('/writeQuiz', methods=['GET', 'POST'])
def writeQuiz():
    global createdQuiz
    Quiz.write_quiz(createdQuiz, taken=False)
    return redirect(url_for('admin'))

# ===== Quiz Administration Routes =====

# Quiz Session Creator Page
@app.route('/activateQuiz', methods=['GET', 'POST'])
def activateQuiz():
    quizNames = fetchAllUntakenQuizNames()
    return render_template("activateQuiz.html", title="Administer a Quiz", quizNames=quizNames)

# Quiz Session Creator Page
@app.route('/activateQuiz/<quizName>', methods=['GET', 'POST'])
def activateQuizName(quizName):
    global activeQuiz
    global activeQuestion
    global activeQuestionNumber
    if activeQuiz is None:
        activeQuiz = loadQuizFromName(quizName)
        activeQuestionNumber = 0
    elif len(activeQuiz.questions) == activeQuestionNumber:
        requests.post("http://127.0.0.1:5000/deactivateQuestion")
        activeQuiz = None
        activeQuestionNumber = -1
        return redirect(url_for('admin'))
    if activeQuestion is not None:
        requests.post("http://127.0.0.1:5000/deactivateQuestion")
    activeQuestion = activeQuiz.get_question_number(activeQuestionNumber)
    activeQuestionNumber += 1
    requests.post("http://127.0.0.1:5000/activateQuestion", json=activeQuestion.json_data)
    return render_template("activeQuiz.html", title="Active Quiz", quizName=quizName,
                           question=activeQuestion)

# Quiz Taker Landing Page
@app.route('/takeQuiz')
def takeQuiz():
    form = None
    if activeQuestion.type == "multiple_choice":
        form = MultipleChoiceResponseForm()
        response = None
        if form.validate_on_submit():
            response = MultipleChoiceResponse(answer=form.answer.data, user_id=1, nickname="Test", question_id=activeQuestion.object_id)
            requests.post("http://127.0.0.1:5000/recordResponse", json=response.json_data)
    elif activeQuestion.type == "fill_in_the_blank":
        form = FillInTheBlankAnswerForm()
        if form.validate_on_submit():
            response = FillInTheBlankResponse(answer=form.answer.data, user_id=1, nickname="Test", question_id=activeQuestion.object_id)
            requests.post("http://127.0.0.1:5000/recordResponse", json=response.json_data)
    return render_template("takeQuiz.html", title="Take a Quiz", question=activeQuestion)

# @app.errorhandler(404)
# def notfound():
#     """Serve 404 template."""
#     return make_response(render_template("404.html"), 404)
