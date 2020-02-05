import json
from typing import Dict, Tuple, List
from abc import ABC, abstractmethod, abstractproperty
import inspect


class Response(ABC):
    """
    Represents a Users response to a Question. Users should have a unique user_id and a nickname
    """

    def __init__(self, user_id: int, nickname: str):
        self.user_id = user_id
        self.nickname = nickname

    @staticmethod
    def create_a_response_from_json(json_representation):
        """
        Factory method to create a Response Object dynamically at runtime.
        :param json_representation: The JSON object as a string or dictionary
        :return: A Response Object representing the type of question in the json_string
        """
        if isinstance(json_representation, str):
            json_as_dictionary = json.loads(json_representation)
        elif isinstance(json_representation, dict):
            json_as_dictionary = json_representation
        else:
            raise ValueError("The json representation must either be a string or a dictionary")
        response_type = json_as_dictionary.get('type')
        json_as_dictionary.pop('type')
        if response_type is None:
            raise ValueError("The value passed to create_a_response_from_json must be question and have a type")
        if question_type == 'multiple_choice':
            return MultipleChoiceResponse(**json_as_dictionary)
        elif question_type == 'matching':
            return MatchingResponse(**json_as_dictionary)
        elif question_type == 'short_answer':
            return ShortAnswerResponse(**json_as_dictionary)
        elif question_type == 'fill_in_the_blank':
            return FillInTheBlankResponse(**json_as_dictionary)
        else:
            raise ValueError("This response type is not supported: {}".format(question_type))

    @abstractproperty
    def json_data(self):
        return

    def jsonify(self):
        return json.dumps(self.json_data)

    def get_type(self):
        return self.type


class MultipleChoiceResponse(Response):

    def __init__(self, choice: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname)
        self.type = 'multiple_choice'
        self.choice = choice

    @property
    def json_data(self):
        return {'type': self.type, 'choice': self.choice, 'user_id': self.user_id, 'nickname': self.nickname}


class MatchingResponse(Response):

    def __init__(self, answer_mapping: Dict[str, str], user_id: int, nickname: str):
        super().__init__(user_id, nickname)
        self.type = 'matching'
        self.answer_mapping = answer_mapping

    @property
    def json_data(self):
        return {'type': self.type, 'answer_mapping': self.answer_mapping, 'user_id': self.user_id,
                'nickname': self.nickname}


class ShortAnswerResponse(Response):

    def __init__(self, short_answer: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname)
        self.type = 'short_answer'
        self.short_answer = short_answer

    @property
    def json_data(self):
        return {'type': self.type, 'short_answer': self.short_answer, 'user_id': self.user_id,
                'nickname': self.nickname}


class FillInTheBlankResponse(Response):

    def __init__(self, blank_answer: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname)
        self.type = 'fill_in_the_blank'
        self.blank_answer = blank_answer

    @property
    def json_data(self):
        return {'type': self.type, 'blank_answer': self.blank_answer, 'user_id': self.user_id,
                'nickname': self.nickname}
