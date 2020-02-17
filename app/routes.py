from flask import Flask, request, render_template, redirect, url_for, flash
from flask import Response as flaskResponse
from app.forms import NewQuizForm, MultipleChoiceQuestionForm, FillInTheBlankQuestionForm, FillInTheBlankAnswerForm, MultipleChoiceAnswerForm, form_factory
from app.Models.Quiz import Quiz
from app.Models.Questions import Question, MultipleChoiceQuestion, FillInTheBlankQuestion
from app.Models.Response import MultipleChoiceResponse, FillInTheBlankResponse
from app.helpers import fetchAllUntakenQuizNames, loadQuizFromName
import requests
import json
from app.JSONHandler import ProjectJSONEncoder


import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template

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
    #TODO URL param args should be added dynamically
    requests.post("http://127.0.0.1:5000/activateQuestion?quizName={}".format(quizName), json=activeQuestion.json_data)
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

def retrieveQuestionsByQuizName(quizName):
    #TODO Clean this url up -- url args should be added via variable or method
    #TODO Should return a status code, etc
    returnedResponse = requests.get("http://127.0.0.1:5000/allQuestionsByQuizName?quizName={}".format(quizName))
    print('the data returned is: {}'.format(returnedResponse.text))
    return returnedResponse.text

@app.route('/retrieveQuestionsForQuiz')
def retrieveQuestionsForQuiz():
    quizName = request.args['quizName']
    quizQuestions = retrieveQuestionsByQuizName(quizName)
    return quizQuestions


# @app.errorhandler(404)
# def notfound():
#     """Serve 404 template."""
#     return make_response(render_template("404.html"), 404)

# ----------------Histograms------------------


def create_hover_tool():
    # we'll code this function in a moment
    return None


def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Student Response Count"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "Question Answer Choices"
    plot.xaxis.major_label_orientation = 1
    return plot

#/histogram/quiz_name
@app.route("/<string:quiz_name>/<int:bars_count>/")
def chart(quiz_name, bars_count):
    if bars_count <= 0:
        bars_count = 1

    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['bugs'].append(random.randint(1,100))
        data['costs'].append(random.uniform(1.00, 1000.00))

    data["days"] = ['A', 'B', 'C', 'D', 'E']

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Student response count", "days",
                            "bugs", hover)
    script, div = components(plot)

    return render_template("chart.html", bars_count=bars_count, quiz_name=quiz_name,
                           the_div=div, the_script=script)