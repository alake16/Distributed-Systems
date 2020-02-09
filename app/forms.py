from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MultipleChoiceQuestionForm(FlaskForm):
    prompt = StringField('Question Prompt')
    answer = StringField('Correct Choice (Letter)')
    choiceA = StringField('Choice A', validators=[DataRequired()])
    choiceB = StringField('Choice B', validators=[DataRequired()])
    choiceC = StringField('Choice C')
    choiceD = StringField('Choice D')
    choiceE = StringField('Choice E')
    submit = SubmitField('Submit Question')

class NewQuizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired()])
    description = StringField('Quiz Description')
    submit = SubmitField('Create Quiz and Add Questions')
