from flask import Flask, request, render_template, redirect, url_for
from app.forms import MultipleChoiceQuestionForm, NewQuizForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

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
@app.route('/createQuiz')
def createQuiz():
    form = NewQuizForm()
    if form.validate_on_submit():
        flash("New Quiz Created")
        return redirect(url_for("addQuestions"))
    return render_template("createQuiz.html", title="Create a Quiz", form=form)

# Question Creator Landing Page
@app.route('/addQuestions/<quizName>')
def addQuestions(quizName):
    return render_template("addQuestions.html", title="Add Questions to " + quizName,
                           quizName=quizName)

# Specific Question Type Creator
@app.route('/addQuestions/<questionType>')
def addQuestionsType(questionType):
    if questionType == "multipleChoice":
        form = MultipleChoiceQuestionForm()
        if form.validate_on_submit():
            flash("New Multiple Choice Question Added")
            return redirect(url_for("addQuestions"))
        return render_template("newMultipleChoiceQuestion.html", title="Add " + questionType +
                               " Question")
    else:
        if questionType == "multipleChoice":
            form = MultipleChoiceQuestionForm()
            if form.validate_on_submit():
                flash("New Matching Question Added")
                return redirect(url_for("addQuestions"))
        return render_template("newMatchingQuestion.html", title="Add " + questionType +
                               " Question")

# ===== Quiz Administration Routes =====

# Quiz Session Creator Page
@app.route('/activateQuiz')
def activateQuiz():
    return render_template("activateQuiz.html", title="Administer a Quiz")

# Quiz Taker Landing Page
@app.route('/taker')
def taker():
    return render_template("taker.html", title="Take a Quiz")

@app.errorhandler(404)
def notfound():
    """Serve 404 template."""
    return make_response(render_template("404.html"), 404)
