import json
import uuid
from typing import List
from app.Models.Questions import Question, MultipleChoiceQuestion, Question, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion
from app.StorageHandler import write_to_file, load_file_as_json, initialize
from app.Models.Response import Response, MultipleChoiceResponse, MatchingResponse, ShortAnswerResponse, FillInTheBlankResponse
from app.JSONHandler import ProjectJSONEncoder


class Quiz:

    # I did not initialize with an empty list because doing so will result in the same list object being passed to all
    # new objects.

    @staticmethod
    def load_quiz_from_json(json_object):
        return Quiz(json_object['name'],
                    questions=[Question.create_a_question(question) for question in json_object['questions']],
                    object_id=json_object['object_id'])

    def __init__(self, name: str, questions: List[Question] = None, object_id=None):
        self.name = name
        if questions is None:
            self.questions = []
        else:
            self.questions = questions
        if object_id is None:
            self.object_id = str(uuid.uuid4())
        else:
            self.object_id = object_id

    def add_question_to_quiz(self, question: Question):
        if not isinstance(question, Question):
            raise ValueError("Only questions can be added to the instance variable questions!")
        self.questions.append(question)

    def get_question(self, question_id):
        return self.questions[question_id]

    @property
    def json_data(self):
        questions = [question.json_data for question in self.questions]
        return {'kind': 'quiz', 'object_id': self.object_id, 'name': self.name,
                'questions': questions}

    @staticmethod
    def write_quiz(quiz_object, taken: bool):
        initialize()
        if not taken:
            return write_to_file(json.dumps(quiz_object, cls=ProjectJSONEncoder, indent=4),
                                 'quizzes/untaken/' + quiz_object.name)
        else:
            return write_to_file(json.dumps(quiz_object, cls=ProjectJSONEncoder, indent=4),
                                 'quizzes/taken/' + quiz_object.name)

    @staticmethod
    def load_quiz(name_of_quiz: str, taken):
        initialize()
        if taken:
            return Quiz.load_quiz_from_json(load_file_as_json('quizzes/taken/' + name_of_quiz))
        else:
            return Quiz.load_quiz_from_json(load_file_as_json('quizzes/untaken/' + name_of_quiz))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


if __name__ == '__main__':
    quiz = Quiz("Brian's First Quiz")

    multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?", choices={"A": 'Mike', "B": 'Domingo'},
                                                      answer='A')
    quiz.add_question_to_quiz(multiple_choice_question)

    matching_question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'},
                                         right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'})
    quiz.add_question_to_quiz(matching_question)

    short_answer_question = ShortAnswerQuestion(prompt="Who is the best?", answer='YOU')
    quiz.add_question_to_quiz(short_answer_question)

    fill_in_the_blank_question = FillInTheBlankQuestion(before_prompt="", after_prompt="are the best", answer='YOU')
    quiz.add_question_to_quiz(fill_in_the_blank_question)

    Quiz.write_quiz(quiz, taken=False)

    quiz = Quiz.load_quiz("Brian's First Quiz", taken=False)

    first_question = quiz.get_question(0)
    response = MultipleChoiceResponse('B', '1345125', 'Brian')
    first_question.add_response(response)
    second_question = quiz.get_question(1)

    response_question_two = MatchingResponse({'A': 'C', 'B': 'D'}, '1345125', 'Brian')
    second_question.add_response(response_question_two)

    third_question = quiz.get_question(2)
    response_question_three = ShortAnswerResponse("YOU", '1345125', 'Brian')
    third_question.add_response(response_question_three)

    fourth_question = quiz.get_question(3)
    response_question_four = FillInTheBlankResponse("YOU", '1345125', 'Brian')
    fourth_question.add_response(response_question_four)

    Quiz.write_quiz(quiz, taken=True)
    quiz = Quiz.load_quiz("Brian's First Quiz", taken=True)
    print(json.dumps(quiz, cls=ProjectJSONEncoder))

