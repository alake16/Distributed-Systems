import json
from typing import Dict
from abc import ABC, abstractmethod
from response_schemas import multiple_choice_response_schema, matching_response_schema, short_answer_response_schema, \
    fill_in_the_blank_response_schema
from jsonschema import validate


class Response(ABC):
    """
    Represents a Users response to a Question. Users should have a unique user_id and a nickname
    """

    def __init__(self, user_id: int, nickname: str, type: str):
        self.type = type
        self.user_id = user_id
        self.nickname = nickname

    @staticmethod
    def create_a_response_from_json(json_representation):
        """
        Factory method to create a Response Object dynamically at runtime.
        :param json_representation: The JSON object a dictionary
        :return: A Response Object representing the type of question in the json_string
        """
        if not isinstance(json_representation, dict):
            raise ValueError("The json representation must be a dictionary")
        if 'type' not in json_representation:
            raise ValueError("The json representation must have a type")
        response_type = json_representation.get('type')
        schema_name = response_type + '_response_schema'
        validate(instance=json_representation, schema=globals()[schema_name])
        json_representation.pop('type')
        json_representation.pop('kind')
        if response_type is None:
            raise ValueError("The value passed to create_a_response_from_json must be question and have a type")
        if response_type == 'multiple_choice':
            return MultipleChoiceResponse(**json_representation)
        elif response_type == 'matching':
            return MatchingResponse(**json_representation)
        elif response_type == 'short_answer':
            return ShortAnswerResponse(**json_representation)
        elif response_type == 'fill_in_the_blank':
            return FillInTheBlankResponse(**json_representation)
        else:
            raise ValueError("This response type is not supported: {}".format(response_type))

    @property
    @abstractmethod
    def json_data(self):
        return

    def get_type(self):
        return self.type


class MultipleChoiceResponse(Response):

    def __init__(self, choice: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname, 'multiple_choice')
        self.choice = choice

    @property
    def json_data(self):
        return {'kind': 'response', 'type': self.type, 'choice': self.choice, 'user_id': self.user_id,
                'nickname': self.nickname}


class MatchingResponse(Response):

    def __init__(self, answer_mapping: Dict[str, str], user_id: int, nickname: str):
        super().__init__(user_id, nickname, 'matching')
        self.answer_mapping = answer_mapping

    @property
    def json_data(self):
        return {'kind': 'response', 'type': self.type, 'answer_mapping': self.answer_mapping, 'user_id': self.user_id,
                'nickname': self.nickname}


class ShortAnswerResponse(Response):

    def __init__(self, short_answer: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname, 'short_answer')
        self.short_answer = short_answer

    @property
    def json_data(self):
        return {'kind': 'response', 'type': self.type, 'short_answer': self.short_answer, 'user_id': self.user_id,
                'nickname': self.nickname}


class FillInTheBlankResponse(Response):

    def __init__(self, blank_answer: str, user_id: int, nickname: str):
        super().__init__(user_id, nickname, 'fill_in_the_blank')
        self.blank_answer = blank_answer

    @property
    def json_data(self):
        return {'kind': 'response', 'type': self.type, 'blank_answer': self.blank_answer, 'user_id': self.user_id,
                'nickname': self.nickname}
