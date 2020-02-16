import json
import uuid
import copy
from typing import Dict, List
from abc import ABC, abstractmethod
from app.Models.Response import Response


class Question(ABC):
    """
    Represent the abstract base class for a Question.
    """

    def __init__(self, object_id=None, responses: List[Response] = None, type: str = None):
        self.type = type
        if object_id is None:
            self.object_id = str(uuid.uuid4())
        else:
            self.object_id = object_id
        self._responses: List[Response] = []

    @property
    @abstractmethod
    def json_data(self) -> Dict:
        """
        This function represents all of the public data of a question as a JSON object (Python Dictionary).
        :return: Python dictionary representing the Question.
        """
        return {}

    def get_type(self) -> str:
        """
        Polymorphic function that returns the type of the question -> multiple_choice, short_answer, matching, fill_in_the_blank
        :return:
        """
        return self.type

    @staticmethod
    def create_a_question(question_representation):
        """
        Factory method to create a Question Object dynamically at runtime.
        :param question_representation: The JSON object as a dictionary, Question object, or JSON string.
        :return: A Question Object representing the type of question in the json_string
        """
        question_representation = copy.deepcopy(question_representation)
        if isinstance(question_representation, Question):
            return question_representation
        if isinstance(question_representation, dict):
            json_as_dictionary = question_representation
            del question_representation
        elif isinstance(question_representation, str):
            json_as_dictionary = json.loads(question_representation)
            del question_representation
        else:
            raise TypeError("The json representation must be a dictionary")
        question_type = json_as_dictionary.get('type')
        json_as_dictionary.pop('type')
        if 'kind' in json_as_dictionary: json_as_dictionary.pop('kind')
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
        """
        Adds a response to the private instance variable responses.
        :param response: An Object that has a Response type (with the same type as this)
        :return: None
        """
        if not isinstance(response, Response):
            raise ValueError("Only Response objects are allowed")
        if response.get_type() != self.get_type():
            raise ValueError("Invalid response type: {} for a question of type: {}")
        self.validate_response(response)
        self._responses.append(response)

    def _initialize_responses(self, responses: List[Dict or Response]):
        """
        Polymorphic method called in the __init__ method after call to super().__init__
        that takes a list of responses in either dictionary or Response object reprsentation
        and calls Response.create_a_response to populate the private instance variable _responses.
        :param responses:
        :return:
        """
        if responses is not None and len(responses) > 0:
            response_objects = [
                Response.create_a_response(response, self.object_id) if isinstance(response, dict) else response for
                response in responses]
            for response_object in response_objects:
                self.add_response(response_object)

    @abstractmethod
    def validate_response(self, response: Response):
        """
        Subject to removal or change: Polymorphic method that validates the response object. A defensive method.
        :param response: A response object to be validated
        :return:
        """
        pass

    # TODO Team Decision -> copy.deepcopy or not
    def get_responses(self):
        """
        Returns the list of the private responses variable.
        :return:
        """
        return self._responses

    def __eq__(self, other) -> bool:
        """
        Subject to change/update: A polymorphic method to test equality of questions.
        :param other: Another object to test for equality.
        :return: bool
        """
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    # TODO MapReduce Model with Coroutines, Make More Efficient -> will come naturally with Streaming Arch
    @staticmethod
    def get_counts(question_object):
        """
        Returns a dictionary of unique responses to count for that response.
        This method only takes into account the most recent response for each user.

        For example, if three users answered like this:

        Mike: A, Mike: B, Doug: A, Louis: A then the following will result for a multiple choice question:
        get_counts(question_object) -> {A: 2, B: 1}

        Similiarly:
        Mike: 'Cat', Mike: 'Dog', Doug: 'Cat', Louis: 'Dog'
        get_counts(short_answer_question_object) -> {'Dog': 2, 'Cat': 1}

        :param question_object: An object to get counts for
        :return: Dictionary representing the counts for each unique response.
        """


        def user_to_most_recent_responses(stream_of_responses):
            user_to_most_recent_response_dict = {}
            for response in stream_of_responses:
                user_to_most_recent_response_dict[response.user_id] = str(response.answer)
            return user_to_most_recent_response_dict

        def reduce_to_counts_dictionary(user_to_most_recent_responses_dict):
            response_to_counts = {}
            for response in user_to_most_recent_responses_dict.values():
                if response not in user_to_most_recent_responses_dict:
                    response_to_counts[response] = 1
                else:
                    response_to_counts[response] += 1
            return response_to_counts

        return reduce_to_counts_dictionary(user_to_most_recent_responses(question_object.get_responses()))


class MultipleChoiceQuestion(Question):
    """
    Represents a Multiple Choice Question object.
    """

    def __init__(self, prompt: str, choices: Dict[str, str], answer: str, responses: List[Dict or Response] = None,
                 object_id=None):
        """
        :param prompt: The prompt for the multiple choice question
        :param choices: Dictionary with the answer choice keys and their prompts
        :param answer: A key in the above dictionary(i.e. a, b, c, d)
        :param responses: A response object represented as a dictionary or an actual response object. This will be internally turned into a list of Responses.
        """
        super().__init__(object_id, responses, 'multiple_choice')
        self.prompt = prompt
        self.choices = choices
        self.answer = answer
        self._initialize_responses(responses)

    @property
    def json_data(self) -> Dict:
        return {'kind': 'question', 'object_id': self.object_id, 'type': "multiple_choice", 'prompt': self.prompt,
                'choices': self.choices,
                'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}

    def validate_response(self, response: Response):
        response_json = response.json_data
        print('response_json is: {}'.format(response_json))
        print('possible choices for the question: {}'.format(self.choices))
        if 'answer' not in response_json:
            raise ValueError("The key choice is not in the representation of this response {}".format(response_json))
        choice = response_json['answer']
        if choice not in self.choices:
            raise ValueError("Response choice present but not reflected in question choices")


class MatchingQuestion(Question):

    """
    A question where a user is able to map choices on the left to choices on the right.

    Internally, Responses will be scored by seeing how many key-value pairs
    in a user's response are equal to the answer's key_value pairs.

    If the user correctly matched two items they will get 2/3 points for example.
    This will be configurable.
    """

    def __init__(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str],
                 answer: Dict[str, str], responses: List[Dict or Response] = None, object_id=None):
        """

        :param prompt: The prompt for the multiple choice question :param left_choices: The choices on the left for
        the user to match to the choices on the right. :param right_choices: The choices on the right to be matched
        by the user to the choices on the right. :param answer: A mapping consisting of keys that are answer choices
        on the left with values that are answer choices on the right. :param responses: A list of tuples which
        themselves are mappings of answer choices on the left to answer choices on the right.

        INTENDED changes: left_choices and right_choices refactored to lists -> ['Dog', 'Cat', 'Mike', 'Doug']

        Internally, it will be ensured that the left_choices and right_choices consist of unique items.

        For example:

        ['Cat', 'Cat'] -> ['Cat']

        """
        super().__init__(object_id, responses, 'matching')
        self.prompt = prompt
        self.left_choices = left_choices
        self.right_choices = right_choices
        self.answer = answer
        self._initialize_responses(responses)

    def validate_response(self, response: Response):
        response_json = response.json_data
        if 'answer' not in response_json.keys():
            raise ValueError("There is no answer present in the response {}".format(response_json))
        left = response_json['answer'].keys()
        right = response_json['answer'].values()
        if not all([left_choice in self.left_choices for left_choice in left]) and all(
                [right_choice in self.right_choices for right_choice in right]):
            raise ValueError("Left choices and/or right_choices for this question object does not contain the key's "
                             "specified in the response")
        return

    @property
    def json_data(self) -> Dict:
        return {'kind': 'question', 'object_id': self.object_id, 'type': "matching", 'prompt': self.prompt,
                'left_choices': self.left_choices,
                'right_choices': self.right_choices, 'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}


class ShortAnswerQuestion(Question):
    """
    A question where a user is given a prompt and is allowed to answer with text input.
    """

    def __init__(self, prompt: str, answer: str, responses: List[Dict or Response] = None, object_id=None):
        """
        :param prompt: The prompt for the question
        :param answer: The answer to the question.
        :param responses: A list of Responses received on this object to the question represented as either Response Objects or dictionaries representing those objects.
        """
        super().__init__(object_id, responses, 'short_answer')
        self.prompt = prompt
        self.answer = answer
        self._initialize_responses(responses)

    def validate_response(self, response: Response):
        response_json = response.json_data
        return

    @property
    def json_data(self) -> Dict:
        return {'kind': 'question', 'object_id': self.object_id, 'type': 'short_answer', 'prompt': self.prompt,
                'answer': self.answer, 'responses': [response.json_data for response in self._responses]}


class FillInTheBlankQuestion(Question):
    """
    A question where a user is given a blank in a prompt and is required to fill it out
    """

    def __init__(self, before_prompt: str, after_prompt: str, answer: str, responses: List[Dict or Response] = None,
                 object_id=None):
        """

        :param before_prompt: The text before the blank
        :param after_prompt: The text after the blank
        :param correct_answer: The correct answer to the question
        :param responses: A list of responses to the question represented as either Response objects or dictionaries representing those objects.
        """
        super().__init__(object_id, responses, 'fill_in_the_blank')
        self.before_prompt = before_prompt
        self.after_prompt = after_prompt
        self.answer = answer
        self._initialize_responses(responses)

    def validate_response(self, response: Response):
        response_json = response.json_data
        return

    @property
    def json_data(self) -> Dict:
        return {'kind': 'question', 'object_id': self.object_id, 'type': 'fill_in_the_blank',
                'before_prompt': self.before_prompt,
                'after_prompt': self.after_prompt, 'answer': self.answer,
                'responses': [response.json_data for response in self._responses]}

# Essentially all questions ever generated should be unique. This should come from a resource that is context aware.
# This should be decoupled from the storage(or not needed by the storage). Quiz id's should be unique as well. This
# logic will need to thought out a little more. I can see issues with deleting quizzes but still needing to keep them
# alive when there's a reference to it in client Code. Essentially, this could become an issue on the client side?
