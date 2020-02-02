from Questions import MultipleChoiceQuestion, Question
from typing import List
import uuid
import Questions
from StorageHandler import write_to_file, load_file_as_json
import json


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
             'questions': [json.loads(question.jsonify()) for question in self.questions]})


if __name__ == '__main__':
    quiz = Quiz("Brian's First Quiz")
    multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?", choices={"A": 'Mike', "B": 'Domingo'},
                                                      answer='A')
    quiz.add_question_to_quiz(multiple_choice_question)
    write_to_file(quiz.jsonify(), 'test.json')
    quiz = Quiz.load_quiz_from_json((load_file_as_json('test.json')))
    first_question = quiz.get_question(0)
    first_question.add_response('A')
    first_question.add_response('B')
    write_to_file(quiz.jsonify(), 'taken_quiz.json')
