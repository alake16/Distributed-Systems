import json
import uuid
import copy
import itertools
from jsonschema import validate
from typing import Dict, Tuple, List
from abc import ABC, abstractmethod, abstractproperty
from Response import Response
from response_schemas import fill_in_the_blank_response_schema, matching_response_schema, \
    multiple_choice_response_schema, short_answer_response_schema


# The use of the dataclass decorator really simplifies the implementation.
class Question(ABC):

    def __init__(self, id=None, responses: List[Response] = None):
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        if responses is None:
            self._responses = []
        else:
            self._responses = []
            response_objects = [Response.create_a_response_from_json(response) for response in responses]
            for response_object in response_objects:
                self.add_response(response_object)

    @abstractproperty
    def json_data(self) -> Dict:
        return {}

    def jsonify(self, student_view=False) -> str:
        """
        Returns a JSON string representation of the object.
        :return: A JSON string representation of the object.
        """
        json_to_return = self.json_data
        if student_view is True:
            json_to_return.pop('answer')
        return json.dumps(json_to_return)

    def get_type(self) -> str:
        return self.type

    @staticmethod
    def create_a_question_from_json(json_representation):
        """
        Factory method to create a Question Object dynamically at runtime.
        :param json_representation: The JSON object as a string or dictionary
        :return: A Question Object representing the type of question in the json_string
        """
        if isinstance(json_representation, str):
            json_as_dictionary = json.loads(json_representation)
        elif isinstance(json_representation, dict):
            json_as_dictionary = json_representation
        else:
            raise ValueError("The json representation must either be a string or a dictionary")
        question_type = json_as_dictionary.get('type')
        json_as_dictionary.pop('type')
        if question_type is None:
            raise ValueError("The value passed to create_a_question_from_json must be question and have a type")
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

    def add_response(self, response: Response):
        if not isinstance(response, Response):
            raise ValueError("Only Response objects are allowed")
        if response.get_type() != self.get_type():
            raise ValueError("Invalid response type: {} for a question of type: {}")
        self.validate_response(response)
        self._responses.append(response)

    def _ensure_json_meets_schema(self, response_as_dictionary: Dict):
        type_of_schema = self.get_type()
        schema_name = type_of_schema + '_response_schema'
        validate(instance=response_as_dictionary, schema=globals()[schema_name])

    @abstractmethod
    def validate_response(self, response: Response):
        pass

    def get_responses(self):
        return self.responses


class MultipleChoiceQuestion(Question):
    """
    Represents a Multiple Choice Question object.
    """

    def __init__(self, prompt: str, choices: Dict[str, str], answer: str, responses: List[Response] = None, id=None):
        """
        :param prompt: The prompt for the multiple choice question
        :param choices: Dictionary with the answer choice keys and their prompts
        :param answer: A key in the above dictionary(i.e. a, b, c, d)
        :param responses: A dictionary that keeps track of the responses on this object(i.e. {A: 0, B: 3, C:2, D:4}
        """
        super().__init__(id, responses)
        self.type = 'multiple_choice'
        self.prompt = prompt
        self.choices = choices
        self.answer = answer

    @property
    def json_data(self) -> Dict:
        return {'id': self.id, 'type': "multiple_choice", 'prompt': self.prompt, 'choices': self.choices,
                'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}

    def validate_response(self, response: Response):
        response_json = response.json_data
        self._ensure_json_meets_schema(response_json)
        choice = response_json['choice']
        if choice not in self.choices.keys():
            raise ValueError("Response choice not reflected in question choices")


class MatchingQuestion(Question):

    def __init__(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str],
                 answer: Dict[str, str], responses: List[Response] = None, id=None):
        """

        :param prompt: The prompt for the multiple choice question
        :param left_choices: The choices on the left for the user to match to the choices on the right.
        :param right_choices: The choices on the right to be matched by the user to the choices on the right.
        :param answer_mapping: A mapping consisting of keys that are answer choices on the left with values that are answer choices on the right.
        :param responses: A list of tuples which themselves are mappings of answer choices on the left to answer choices on the right.
        """
        super().__init__(id, responses)
        self.type = 'matching'
        self.prompt = prompt
        self.left_choices = left_choices
        self.right_choices = right_choices
        self.answer = answer

    def validate_response(self, response: Response):
        response_json = response.json_data
        self._ensure_json_meets_schema(response_json)
        left = response_json['answer_mapping'].keys()
        right = response_json['answer_mapping'].values()
        if len(left) != len(right):
            raise ValueError("There are a different number of left and right choices")
        if not all([left_choice in self.left_choices for left_choice in left]) and all(
                [right_choice in self.right_choices for right_choice in right]):
            raise ValueError("Left choices and/or right_choices for this question object does not contain the key's "
                             "specified in the response")
        return

    @property
    def json_data(self) -> Dict:
        return {'id': self.id, 'type': "matching", 'prompt': self.prompt, 'left_choices': self.left_choices,
                'right_choices': self.right_choices, 'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}


class ShortAnswerQuestion(Question):
    """
    A question where a user is given a prompt and is allowed to answer with text input.
    """

    def __init__(self, prompt: str, answer: str, responses: List[Response] = None, id=None):
        """
        :param prompt: The prompt for the question
        :param answer: The answer to the question.
        :param responses: A list of string responses received on this object to the question.
        """
        super().__init__(id, responses)
        self.type = 'short_answer'
        self.prompt = prompt
        self.answer = answer

    def validate_response(self, response: Response):
        response_json = response.json_data
        self._ensure_json_meets_schema(response_json)
        return

    @property
    def json_data(self) -> Dict:
        return {'id': self.id, 'type': 'short_answer', 'prompt': self.prompt,
                'answer': self.answer, 'responses': [response.json_data for response in self._responses]}


class FillInTheBlankQuestion(Question):
    """
    A question where a user is given a blank in a prompt and is required to fill it out
    """

    def __init__(self, before_prompt: str, after_prompt: str, answer: str, responses: List[Response] = None,
                 id=None):
        """

        :param before_prompt: The text before the blank
        :param after_prompt: The text after the blank
        :param correct_answer: The correct answer to the question
        :param responses: A list of text responses to the question
        """
        super().__init__(id, responses)
        self.type = 'fill_in_the_blank'
        self.before_prompt = before_prompt
        self.after_prompt = after_prompt
        self.answer = answer

    def validate_response(self, response: Response):
        response_json = response.json_data
        self._ensure_json_meets_schema(response_json)
        return

    @property
    def json_data(self) -> Dict:
        return {'id': self.id, 'type': 'fill_in_the_blank', 'before_prompt': self.before_prompt,
                'after_prompt': self.after_prompt, 'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}

# Essentially all questions ever generated should be unique. This should come from a resource that is context aware.
# This should be decoupled from the storage(or not needed by the storage). Quiz id's should be unique as well. This
# logic will need to thought out a little more. I can see issues with deleting quizzes but still needing to keep them
# alive when there's a reference to it in client Code. Essentially, this could become an issue on the client side?
