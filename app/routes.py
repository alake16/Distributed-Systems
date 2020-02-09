from flask import Flask, request, render_template, redirect, url_for, flash
from app.forms import MultipleChoiceQuestionForm, NewQuizForm
from app.Models.Quiz import Quiz
from app.Models.Questions import MultipleChoiceQuestion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

createdQuiz = None

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
        if questionType == "multiple_choice":
            form = MultipleChoiceQuestionForm()
            if form.validate_on_submit():
                choices = {
                    "A": form.choiceA.data,
                    "B": form.choiceB.data,
                    "C": form.choiceC.data,
                    "D": form.choiceD.data,
                    "E": form.choiceE.data,
                }
                # get rid of any empty choices
                choices = {k: v for k, v in choices.items() if v}
                newMultChoiceQuestion = MultipleChoiceQuestion(prompt=form.prompt.data,
                                                               choices=choices,
                                                               answer=form.answer.data)
                createdQuiz.add_question_to_quiz(question=newMultChoiceQuestion)
                print(createdQuiz)
                return redirect(url_for("addQuestions", quizName=createdQuiz.name))
            return render_template("newMultipleChoiceQuestion.html", title="Add " + questionType +
                                   " Question", quizName=createdQuiz.name, form=form)
        # else:
        #     form = MatchingQuestionForm()
        #     if form.validate_on_submit():
        #         flash("New Matching Question Added")
        #         return redirect(url_for("addQuestions"))
        #     return render_template("newMatchingQuestion.html", title="Add " + questionType +
        #                            " Question")

# Quiz Session Creator Page
@app.route('/writeQuiz', methods=['GET', 'POST'])
def writeQuiz():
    global createdQuiz
    Quiz.write_quiz(createdQuiz, taken=False)
    return redirect(url_for('admin'))

# ===== Quiz Administration Routes =====

# Quiz Session Creator Page
@app.route('/activateQuiz')
def activateQuiz():
    return render_template("activateQuiz.html", title="Administer a Quiz")

# Quiz Taker Landing Page
@app.route('/taker')
def taker():
    return render_template("taker.html", title="Take a Quiz")

# @app.errorhandler(404)
# def notfound():
#     """Serve 404 template."""
#     return make_response(render_template("404.html"), 404)
