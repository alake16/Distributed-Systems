import json
import uuid
from typing import List
from app.Models.Questions import Question, MultipleChoiceQuestion, Question, MatchingQuestion, ShortAnswerQuestion, \
    FillInTheBlankQuestion
from app.StorageHandler import write_to_file, load_file_as_json, initialize
from app.Models.Response import Response, MultipleChoiceResponse, MatchingResponse, ShortAnswerResponse, \
    FillInTheBlankResponse
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

    def get_question_number(self, number):
        return self.questions[number]

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
                                 '../quizzes/untaken/' + quiz_object.name + '.json')
        else:
            return write_to_file(json.dumps(quiz_object, cls=ProjectJSONEncoder, indent=4),
                                 '../quizzes/taken/' + quiz_object.name + '.json')

    @staticmethod
    def load_quiz(name_of_quiz: str, taken):
        initialize()
        if taken:
            return Quiz.load_quiz_from_json(load_file_as_json('../quizzes/taken/' + name_of_quiz + '.json'))
        else:
            return Quiz.load_quiz_from_json(load_file_as_json('../quizzes/untaken/' + name_of_quiz + '.json'))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
