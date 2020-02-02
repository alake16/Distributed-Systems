from typing import Dict, Tuple, List
import textwrap
import itertools
from abc import ABC, abstractmethod, abstractproperty
import json
import uuid
from StorageHandler import write_to_file


# The use of the dataclass decorator really simplifies the implementation.
class Question(ABC):

    # TODO make this generator 100% unique.
    def __init__(self, id=None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        pass

    def jsonify(self):
        pass

    @abstractmethod
    def add_response(self, response):
        pass

    @staticmethod
    def create_a_question_from_json_string(json_string):
        """
        Factory method to create a Question Object dynamically at runtime.
        :param json_string: The JSON object as a string
        :return: A Question Object representing the type of question in the json_string
        """
        json_as_dictionary = json.loads(json_string)
        question_type = json_as_dictionary.get('type')
        json_as_dictionary.pop('type')
        if question_type is None:
            raise ValueError("The value passed to create_a_question_from_json_string must be question and have a type")
        if question_type == 'multiple_choice':
            return MultipleChoiceQuestion(**json_as_dictionary)
        elif question_type == 'matching':
            return MatchingQuestion(**json_as_dictionary)
        elif question_type == 'short_answer':
            return ShortAnswerQuestion(**json_as_dictionary)
        elif question_type == 'fill_in_the_blank':
            return FillInTheBlankQuestion(**json_as_dictionary)
        else:
            raise ValueError("This question type is not supported: {}".format(question_type))


class MultipleChoiceQuestion(Question):
    """
    Represents a Multiple Choice Question object.
    """

    def __init__(self, prompt: str, choices: Dict[str, str], answer: str, responses: Dict[str, int] = None, id=None):
        """
        :param prompt: The prompt for the multiple choice question
        :param choices: Dictionary with the answer choice keys and their prompts
        :param answer: A key in the above dictionary(i.e. a, b, c, d)
        :param responses: A dictionary that keeps track of the responses on this object(i.e. {A: 0, B: 3, C:2, D:4}
        """
        super().__init__(id)
        self.prompt = prompt
        self.choices = choices
        self.answer = answer
        if responses is None:
            self.responses = {choice: 0 for choice in choices}
        if not (all(key in self.choices.keys() for key in self.responses.keys())):
            raise ValueError("Not all of the responses are reflected in the answer choices")

    def add_response(self, response: str):
        """
        Adds a response to the responses instance variable.
        :param response: A key representing a users response to a question
        :return: None
        """
        if response not in self.responses.keys():
            raise ValueError('The Response {} is not in the list of possible responses'.format(response))
        else:
            self.responses[response] += 1

    def jsonify(self):
        """
        Returns the JSON representation of this object.
        :return: The JSON representation of this object.
        """
        return json.dumps(
            {'uuid': self.id, 'type': "multiple_choice", 'prompt': self.prompt, 'choices': self.choices,
             'answer': self.answer,
             'responses': self.responses})


class MatchingQuestion(Question):

    def __init__(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str],
                 answer_mapping: Dict[str, str], responses: List[Dict[str, str]] = None, id=None):
        """

        :param prompt: The prompt for the multiple choice question
        :param left_choices: The choices on the left for the user to match to the choices on the right.
        :param right_choices: The choices on the right to be matched by the user to the choices on the right.
        :param answer_mapping: A mapping consisting of keys that are answer choices on the left with values that are answer choices on the right.
        :param responses: A list of tuples which themselves are mappings of answer choices on the left to answer choices on the right.
        """
        super().__init__(id)
        self.prompt = prompt
        self.left_choices = left_choices
        self.right_choices = right_choices
        self.answer_mapping = answer_mapping
        if responses is None:
            self.responses = []

    def jsonify(self):
        """
        Gives a JSON string representation of the object.
        :return: A JSON string representing the object.
        """
        return json.dumps(
            {'uuid': self.id, 'type': "matching", 'prompt': self.prompt, 'left_choices': self.left_choices,
             'right_choices': self.right_choices, 'answer_mapping': self.answer_mapping,
             'responses': self.responses})

    def add_response(self, response: Dict[str, str]):
        """
        Adds a response(a mapping of a answer choice on the left to an answer choice on the right)
        :param response: A dictionary object that consists of objects on the left mapping to objects on the right.
        :return: None
        """
        left_key_in_choices = response[0] in self.left_choices
        right_key_in_choices = response[1] in self.right_choices
        if left_key_in_choices and right_key_in_choices:
            self.responses.append(response)
        else:
            raise ValueError("One of the keys in the answer_mapping is not present")


class ShortAnswerQuestion(Question):
    """
    A question where a user is given a prompt and is allowed to answer with text input.
    """

    def __init__(self, prompt: str, answer: str, responses: List[str] = None, id=None):
        """
        :param prompt: The prompt for the question
        :param answer: The answer to the question.
        :param responses: A list of string responses received on this object to the question.
        """
        super().__init__(id)
        self.prompt = prompt
        self.answer = answer
        if responses is None:
            self.responses = []
        else:
            self.responses = responses

    def jsonify(self):
        """
        Returns a JSON string representation of the object.
        :return: A JSON string representation of the object.
        """
        return json.dumps({'uuid': self.id, 'type': 'short_answer_question', 'prompt': self.prompt,
                           'answer': self.answer, 'responses': self.responses})

    def add_response(self, response):
        """
        Adds a string response to the object's responses.
        :param response: A user's response to the object.
        :return: None
        """
        self.responses.append(response)


class FillInTheBlankQuestion(Question):
    """
    A question where a user is given a blank in a prompt and is required to fill it out
    """

    def __init__(self, before_prompt: str, after_prompt: str, correct_answer: str, responses: List[str] = None,
                 id=None):
        """

        :param before_prompt: The text before the blank
        :param after_prompt: The text after the blank
        :param correct_answer: The correct answer to the question
        :param responses: A list of text responses to the question
        """
        super().__init__(id)
        self.before_prompt = before_prompt
        self.after_prompt = after_prompt
        self.answer = correct_answer
        if responses is None:
            self.responses = []

    def jsonify(self):
        """
        Returns a JSON string representation of the object.
        :return: A JSON string representation of the the object.
        """
        return json.dumps({'uuid': self.id, 'type': 'fill_in_the_blank', 'before': self.before_prompt,
                           'after': self.after_prompt, 'answer': self.answer,
                           'responses': self.responses})

    def add_response(self, response: str):
        """
        Adds a text response to the list of responses
        :param response: The text response received on this object.
        :return: None
        """

        self.responses.append(response)


# Essentially all questions ever generated should be unique. This should come from a resource that is context aware.
# This should be decoupled from the storage(or not needed by the storage). Quiz id's should be unique as well. This
# logic will need to thought out a little more. I can see issues with deleting quizzes but still needing to keep them
# alive when there's a reference to it in client Code. Essentially, this could become an issue on the client side?

class Quiz:

    # I did not initialize with an empty list because doing so will result in the same list object being passed to all
    # new objects.
    def __init__(self, name: str, questions: List[Question] = None, id=None):
        self.name = name
        if questions is None:
            self.questions = []
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
            {'uuid': self.id, 'name': self.name, 'questions': [json.loads(question.jsonify()) for question in self.questions]})


if __name__ == '__main__':
    quiz = Quiz("Brian's First Quiz")
    multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?", choices={"A": 'Mike', "B": 'Domingo'},
                                                      answer='A')
    quiz.add_question_to_quiz(multiple_choice_question)
    quiz.get_question(0).add_response('A')
    quiz.get_question(0).add_response('B')
    write_to_file(quiz.jsonify(), 'test.json')
