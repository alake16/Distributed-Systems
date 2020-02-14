import unittest
from unittest.mock import patch, MagicMock, call
from app.Models.Response import Response, FillInTheBlankResponse, ShortAnswerResponse, MatchingResponse, \
    MultipleChoiceResponse
import copy
import json
import uuid


class TestResponse(unittest.TestCase):

    def helper(self, response_json, response_class, response_type):
        with patch('app.Models.Response.' + response_type + '.__init__') as mock_init:
            mock_init.return_value = None
            response = Response.create_a_response(response_json, 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756')
            self.assertIsInstance(response, response_class)
            correct_call_dictionary = copy.copy(response_json)
            # The correct call should not include the kind and type but should include the rest of the JSON.
            correct_call_dictionary.pop('kind')
            correct_call_dictionary.pop('type')
            calls = [call(**correct_call_dictionary)]
            mock_init.assert_has_calls(calls)
            json_string = json.dumps(response_json)
            response = Response.create_a_response(json_string, 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756')
            self.assertIsInstance(response, response_class)
            calls.append(call(**correct_call_dictionary))
            mock_init.assert_has_calls(calls)

    def test_create_a_response(self):
        matching_response_json = {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            "kind": "response",
            "type": "matching",
            "answer_mapping": {
                "A": "C",
                "B": "D"
            },
            "user_id": "1345125",
            "nickname": "Brian"
        }
        short_answer_response_json = {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            "kind": "response",
            "type": "short_answer",
            "short_answer": "YOU",
            "user_id": "1345125",
            "nickname": "Brian"
        }
        fill_in_the_blank_json = {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            "kind": "response",
            "type": "fill_in_the_blank",
            "blank_answer": "YOU",
            "user_id": "1345125",
            "nickname": "Brian"
        }
        multiple_choice_response_json = {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            "kind": "response",
            "type": "multiple_choice",
            "choice": "B",
            "user_id": "1345125",
            "nickname": "Brian"
        }
        self.helper(response_json=multiple_choice_response_json, response_class=MultipleChoiceResponse,
                    response_type='MultipleChoiceResponse')
        self.helper(response_json=matching_response_json, response_class=MatchingResponse,
                    response_type='MatchingResponse')
        self.helper(response_json=short_answer_response_json, response_class=ShortAnswerResponse,
                    response_type="ShortAnswerResponse")
        self.helper(response_json=fill_in_the_blank_json, response_class=FillInTheBlankResponse,
                    response_type="FillInTheBlankResponse")


class TestMultipleChoiceResponse(unittest.TestCase):
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        self.response_object = MultipleChoiceResponse(choice='A', user_id=1345125, nickname='brian',
                                                      question_id='d3d46649-4dbb-4d6b-b1fe-5f87f5b42756')

    def test_json_data(self):
        self.assertEqual(self.response_object.json_data, {'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
                                                          'choice': 'A',
                                                          'kind': 'response',
                                                          'nickname': 'brian',
                                                          'type': 'multiple_choice',
                                                          'user_id': 1345125})

    def test_get_type(self):
        self.assertEqual(self.response_object.get_type(), 'multiple_choice')


class TestMatchingResponse(unittest.TestCase):
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        self.response_object = MatchingResponse({'A': 'C', 'B': 'D'}, '1345125', 'Brian',
                                                question_id='d3d46649-4dbb-4d6b-b1fe-5f87f5b42756')

    def test_json_data(self):
        self.assertEqual(self.response_object.json_data, {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            'answer_mapping': {'A': 'C', 'B': 'D'},
            'kind': 'response',
            'nickname': 'Brian',
            'type': 'matching',
            'user_id': '1345125'})

    def test_get_type(self):
        self.assertEqual(self.response_object.get_type(), 'matching')


class TestShortAnswerResponse(unittest.TestCase):
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        self.response_object = ShortAnswerResponse("YOU", '1345125', 'Brian',
                                                   question_id='d3d46649-4dbb-4d6b-b1fe-5f87f5b42756')

    def test_json_data(self):
        self.assertEqual(self.response_object.json_data, {
            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
            'kind': 'response',
            'nickname': 'Brian',
            'short_answer': 'YOU',
            'type': 'short_answer',
            'user_id': '1345125'})

    def test_get_type(self):
        self.assertEqual(self.response_object.get_type(), 'short_answer')


class TestFillInTheBlankResponse(unittest.TestCase):
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        self.response_object = FillInTheBlankResponse("YOU", '1345125', 'Brian', question_id='d3d46649-4dbb-4d6b-b1fe-5f87f5b42756')

    def test_json_data(self):
        self.assertEqual(self.response_object.json_data, {'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
                                                          'blank_answer': 'YOU',
                                                          'kind': 'response',
                                                          'nickname': 'Brian',
                                                          'type': 'fill_in_the_blank',
                                                          'user_id': '1345125'})

    def test_get_type(self):
        self.assertEqual(self.response_object.get_type(), 'fill_in_the_blank')


if __name__ == '__main__':
    unittest.main()
