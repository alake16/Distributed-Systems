from Questions import Question, MultipleChoiceQuestion, MatchingQuestion

def render_question(question: Question, is_quiz=True):
    if isinstance(question, Question):
        if is_quiz is True:
            print(question.quiz_view())
        else:
            print(question)
    else:
        raise TypeError("The question parameter is of an invalid type.")
