from Questions import MultipleChoiceQuestion, Question, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion
from typing import List
import uuid
import Questions
from StorageHandler import write_to_file, load_file_as_json
import json
from Response import MultipleChoiceResponse, MatchingResponse, ShortAnswerResponse, FillInTheBlankResponse


class Quiz:

    # I did not initialize with an empty list because doing so will result in the same list object being passed to all
    # new objects.

    @staticmethod
    # TODO find a way to ensure multiple of the same quiz are not loaded.
    def load_quiz_from_json(json_object):
        return Quiz(json_object['name'],
                    questions=[Question.create_a_question_from_json(question) for question in json_object['questions']],
                    id=json_object['id'])

    def __init__(self, name: str, questions: List[Question] = None, id=None):
        self.name = name
        if questions is None:
            self.questions = []
        else:
            self.questions = questions
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def add_question_to_quiz(self, question: Question):
        if not isinstance(question, Question):
            raise ValueError("Only questions can be added to the instance variable questions!")
        self.questions.append(question)

    def get_question(self, question_id):
        return self.questions[question_id]

    def jsonify(self):
        return json.dumps(
            {'id': self.id, 'name': self.name,
             'questions': [json.loads(question.jsonify()) for question in self.questions]}, indent=4)


if __name__ == '__main__':
    quiz = Quiz("Brian's First Quiz")
    multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?", choices={"A": 'Mike', "B": 'Domingo'},
                                                      answer='A')
    quiz.add_question_to_quiz(multiple_choice_question)
    matching_question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'}, right_choices = {'C': 'Ike', 'D': 'Mike'}, answer_mapping = {'A': 'C', 'B': 'D'})
    quiz.add_question_to_quiz(matching_question)
    short_answer_question = ShortAnswerQuestion(prompt="Who is the best?", answer='YOU')
    quiz.add_question_to_quiz(short_answer_question)
    fill_in_the_blank_question = FillInTheBlankQuestion(before_prompt="", after_prompt="are the best", answer='YOU')
    quiz.add_question_to_quiz(fill_in_the_blank_question)
    write_to_file(quiz.jsonify(), 'untaken_quiz.json')
    quiz = Quiz.load_quiz_from_json((load_file_as_json('untaken_quiz.json')))
    first_question = quiz.get_question(0)
    response = MultipleChoiceResponse('B', '1345125', 'Brian')
    first_question.add_response(response)
    second_question = quiz.get_question(1)
    response_question_two = MatchingResponse({'A': 'C', 'B': 'D'}, 1345125, 'Brian')
    second_question.add_response(response_question_two)
    third_question = quiz.get_question(2)
    response_question_three = ShortAnswerResponse("YOU", 1345125, 'Brian')
    third_question.add_response(response_question_three)
    fourth_question = quiz.get_question(3)
    response_question_four = FillInTheBlankResponse("YOU", 1345125, 'Brian')
    fourth_question.add_response(response_question_four)
    write_to_file(quiz.jsonify(), 'taken_quiz.json')
