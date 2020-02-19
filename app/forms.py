import itertools
import string
from abc import abstractmethod, ABC
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# This function was taken from https://stackoverflow.com/questions/30278539/python-cycle-through-the-alphabet
def _alphabet_generator():
    """
    Meant to cycle through the alphabet so answer choices aren't duplicated -> a, b, c, d..... aa...zz....
    """
    for i in itertools.count():
        for t in itertools.product(string.ascii_lowercase, repeat=i):
            yield ''.join(t)


def form_factory(type: str, kind='question'):
    if kind.lower() == 'answer':
        pass
    if kind.lower() == 'question':
        if type == 'multiple_choice':
            return MultipleChoiceQuestionForm()
        elif type == 'fill_in_the_blank':
            return FillInTheBlankQuestionForm()
        else:
            raise ValueError()
    if kind.lower() == 'quiz':
        return NewQuizForm()
    else:
        raise ValueError()


class NewQuizForm(FlaskForm):
    name = StringField('Quiz Name', validators=[DataRequired()])
    description = StringField('Quiz Description')
    submit = SubmitField('Create Quiz and Add Questions')


class MultipleChoiceQuestionForm(FlaskForm):
    prompt = StringField('Question Prompt')
    answer = StringField('Correct Choice (Letter)')
    choiceA = StringField('Choice A', validators=[DataRequired()])
    choiceB = StringField('Choice B', validators=[DataRequired()])
    choiceC = StringField('Choice C')
    choiceD = StringField('Choice D')
    choiceE = StringField('Choice E')
    submit = SubmitField('Submit Question')

    @property
    def json_data(self):
        choices = [self.choiceA.data, self.choiceB.data, self.choiceC.data, self.choiceD.data, self.choiceE.data]
        alphabet_iterator = iter(_alphabet_generator())
        next(alphabet_iterator)
        choices = {next(alphabet_iterator): choice for choice in choices if choice}
        return {'type': 'multiple_choice', 'choices': choices, 'prompt': self.prompt.data, 'answer': self.answer.data}


class FillInTheBlankQuestionForm(FlaskForm):
    beforePrompt = StringField('Before Prompt')
    answer = StringField('Answer')
    afterPrompt = StringField('After Prompt')
    submit = SubmitField('Submit Question')

    @property
    def json_data(self):
        return {'type': 'fill_in_the_blank', 'before_prompt': self.beforePrompt.data, 'answer': self.answer.data,
                'after_prompt': self.afterPrompt.data}


class FillInTheBlankAnswerForm(FlaskForm):
    answer = StringField('Answer')
    submit = SubmitField('Submit Answer')


class MultipleChoiceAnswerForm(FlaskForm):
    answer = StringField('Answer')
    submit = SubmitField('Submit Answer')
