import unittest
from unittest.mock import patch, call, MagicMock, Mock
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, \
    FillInTheBlankQuestion
from app.Models.Response import MultipleChoiceResponse, MatchingResponse, ShortAnswerResponse, FillInTheBlankResponse, \
    Response
import uuid
import json
import copy


class TestQuestion(unittest.TestCase):

    def helper(self, question_json, question_class, question_type):
        with patch('app.Models.Questions.' + question_type + '.__init__') as mock_init:
            mock_init.return_value = None
            question = Question.create_a_question(question_json)
            self.assertIsInstance(question, question_class)
            correct_call_dictionary = copy.copy(question_json)
            # The correct call should not include the kind and type but should include the rest of the JSON.
            correct_call_dictionary.pop('kind')
            correct_call_dictionary.pop('type')
            calls = [call(**correct_call_dictionary)]
            mock_init.assert_has_calls(calls)
            json_string = json.dumps(question_json)
            question = Question.create_a_question(json_string)
            self.assertIsInstance(question, question_class)
            calls.append(call(**correct_call_dictionary))
            mock_init.assert_has_calls(calls)

    def test_create_a_multiple_choice_question(self):
        """
        Tests the static factory method of Question and ensures it returns the appropriate objects
        by calling the appropriate constructor with the appropriate arguments once.
        :return:
        """
        multiple_choice_question_json = {
            "kind": "question",
            "id": "c777ff3a-270e-447a-ad49-12006e04cb36",
            "type": "multiple_choice",
            "prompt": "Who is the best?",
            "choices": {
                "A": "Mike",
                "B": "Domingo"
            },
            "answer": "A",
            "responses": [
                {
                    "kind": "response",
                    "type": "multiple_choice",
                    "choice": "B",
                    "user_id": "1345125",
                    "nickname": "Brian"
                }
            ]
        }
        matching_json = {
            "kind": "question",
            "id": "d3d46649-4dbb-4d6b-b1fe-5f87f5b42756",
            "type": "matching",
            "prompt": "Match the following questions",
            "left_choices": {
                "A": "Mike",
                "B": "Ike"
            },
            "right_choices": {
                "C": "Ike",
                "D": "Mike"
            },
            "answer": {
                "A": "C",
                "B": "D"
            },
            "responses": [
                {
                    "kind": "response",
                    "type": "matching",
                    "answer_mapping": {
                        "A": "C",
                        "B": "D"
                    },
                    "user_id": "1345125",
                    "nickname": "Brian"
                }
            ]
        }
        short_answer_json = {
            "kind": "question",
            "id": "e00a3f6d-3ab7-4cb4-8441-6584a785f50d",
            "type": "short_answer",
            "prompt": "Who is the best?",
            "answer": "YOU",
            "responses": [
                {
                    "kind": "response",
                    "type": "short_answer",
                    "short_answer": "YOU",
                    "user_id": "1345125",
                    "nickname": "Brian"
                }
            ]
        }
        fill_in_the_blank_json = {
            "kind": "question",
            "id": "ab2cc19d-3d31-4ba9-8b90-ae1c8e035884",
            "type": "fill_in_the_blank",
            "before_prompt": "",
            "after_prompt": "are the best",
            "answer": "YOU",
            "responses": [
                {
                    "kind": "response",
                    "type": "fill_in_the_blank",
                    "blank_answer": "YOU",
                    "user_id": "1345125",
                    "nickname": "Brian"
                }
            ]
        }
        self.helper(question_json=multiple_choice_question_json, question_class=MultipleChoiceQuestion,
                    question_type='MultipleChoiceQuestion')
        self.helper(question_json=matching_json, question_class=MatchingQuestion, question_type='MatchingQuestion')
        self.helper(question_json=short_answer_json, question_class=ShortAnswerQuestion,
                    question_type="ShortAnswerQuestion")
        self.helper(question_json=fill_in_the_blank_json, question_class=FillInTheBlankQuestion,
                    question_type="FillInTheBlankQuestion")

    @patch('app.Models.Questions.MultipleChoiceQuestion.validate_response', return_value=None)
    def test_add_response(self, mock_validate):
        # Not using the spec will not allow the isinstance method to work since it'll see MagicMock
        multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?",
                                                          choices={"A": 'Mike', "B": 'Domingo'},
                                                          answer='A')
        response = MagicMock(spec=MultipleChoiceResponse)
        response.get_type.return_value = 'multiple_choice'
        response.json_data = {'choice': 'A'}
        multiple_choice_question.add_response(response)
        mock_validate.assert_called()
        response = MagicMock(spec=MultipleChoiceResponse)
        response.get_type.return_value = 'matching'
        response.json_data = {'choice': 'A'}
        with self.assertRaises(ValueError):
            multiple_choice_question.add_response(response)


class TestMultipleChoiceQuestion(unittest.TestCase):

    # Patch since uuid4 gives random id every run.
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        response_object = MultipleChoiceResponse(choice='A', user_id=1345125, nickname='brian')
        self.responses = [
            {'kind': 'response', 'type': 'multiple_choice', 'choice': 'B', 'user_id': '1345125', 'nickname': 'Brian'},
            response_object]
        self.multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?",
                                                               choices={"A": 'Mike', "B": 'Domingo'},
                                                               answer='A')
        self.answered_question = MultipleChoiceQuestion(prompt="Who is the best?", object_id='be24d525-8904-4948-b47d'
                                                                                             '-54248586986d',
                                                        choices={"A": "Mike", "B": 'Domingo'},
                                                        answer='A', responses=self.responses)

    def test_get_responses(self):
        self.assertEqual(len(self.answered_question.get_responses()), 2)
        self.assertTrue(
            all(isinstance(response, MultipleChoiceResponse) for response in self.answered_question.get_responses()))
        self.assertEqual(self.answered_question.get_responses(),
                         [Response.create_a_response(response) for response in self.responses])

    def test_json_data(self):
        self.assertEqual(self.multiple_choice_question.json_data,
                         {'answer': 'A', 'choices': {'A': 'Mike', 'B': 'Domingo'},
                          'object_id': 'be24d525-8904-4948-b47d-54248586986d', 'kind': 'question',
                          'prompt': 'Who is the best?', 'responses': [], 'type': 'multiple_choice'})

    def test_validate_response(self):
        response = MagicMock()
        self.multiple_choice_question = MultipleChoiceQuestion(prompt="Who is the best?",
                                                               choices={"A": 'Mike', "B": 'Domingo'},
                                                               answer='A')
        response.json_data = {'choice': 'A'}
        self.multiple_choice_question.validate_response(response)
        invalid_response_one = MagicMock()
        invalid_response_one.json_data = {'dog': 'A'}
        with self.assertRaises(ValueError):
            self.multiple_choice_question.validate_response(invalid_response_one)

    def test_get_type(self):
        self.assertEqual(self.multiple_choice_question.get_type(), 'multiple_choice')


class TestMatchingQuestion(unittest.TestCase):

    # Patch since uuid4 gives random id every run.
    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        response_object = MatchingResponse({'A': 'C', 'B': 'D'}, '1345125', 'Brian')
        self.responses = [
            {
                "kind": "response",
                "type": "matching",
                "answer_mapping": {
                    "A": "C",
                    "B": "D"
                },
                "user_id": "1345125",
                "nickname": "Brian"
            }
            ,
            response_object]
        self.question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'},
                                         right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'})
        self.answered_question = MatchingQuestion(prompt="Match the following questions",
                                                  left_choices={"A": 'Mike', "B": 'Ike'},
                                                  right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'},
                                                  responses=self.responses,
                                                  object_id='be24d525-8904-4948-b47d-54248586986d')

    def test_json_data(self):
        self.assertEqual(self.question.json_data,
                         {'answer': {'A': 'C', 'B': 'D'},
                          'object_id': 'be24d525-8904-4948-b47d-54248586986d',
                          'kind': 'question',
                          'left_choices': {'A': 'Mike', 'B': 'Ike'},
                          'prompt': 'Match the following questions',
                          'responses': [],
                          'right_choices': {'C': 'Ike', 'D': 'Mike'},
                          'type': 'matching'}
                         )

    def test_validate_response(self):
        response = MagicMock()
        self.question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'},
                                         right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'})
        response.json_data = {'answer_mapping': {'A': 'C'}}
        self.question.validate_response(response)
        invalid_response_one = MagicMock()
        invalid_response_one.json_data = {'dog': 'A'}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_one)
        invalid_response_two = MagicMock()
        invalid_response_two.json_data = {'answer_mapping': {'F': 'C'}}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_two)

    def test_get_type(self):
        self.assertEqual(self.question.get_type(), 'matching')


class TestShortAnswerQuestion(unittest.TestCase):

    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        response = ShortAnswerResponse("YOU", '1345125', 'Brian')
        self.responses = [response]
        self.question = ShortAnswerQuestion(prompt="Who is the best?", answer='YOU')
        self.answered_question = ShortAnswerQuestion("Who is the best?",
                                                     object_id='be24d525-8904-4948-b47d-54248586986d',
                                                     answer='YOU', responses=self.responses)

    def test_json_data(self):
        self.assertEqual(self.question.json_data,
                         {'answer': 'YOU',
                          'object_id': 'be24d525-8904-4948-b47d-54248586986d',
                          'kind': 'question',
                          'prompt': 'Who is the best?',
                          'responses': [],
                          'type': 'short_answer'}
                         )

    def test_validate_response(self):
        response = MagicMock()
        self.question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'},
                                         right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'})
        response.json_data = {'answer_mapping': {'A': 'C'}}
        self.question.validate_response(response)
        invalid_response_one = MagicMock()
        invalid_response_one.json_data = {'dog': 'A'}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_one)
        invalid_response_two = MagicMock()
        invalid_response_two.json_data = {'answer_mapping': {'F': 'C'}}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_two)

    def test_get_type(self):
        self.assertEqual(self.question.get_type(), 'short_answer')


class TestFillInTheBlankQuestion(unittest.TestCase):

    @patch('uuid.uuid4', side_effect=[uuid.UUID('be24d525-8904-4948-b47d-54248586986d'), uuid.UUID('ce24d525-8904'
                                                                                                   '-4948-b47d'
                                                                                                   '-54248586986e')])
    def setUp(self, uuid_mock) -> None:
        response = FillInTheBlankResponse("YOU",  '1345125', 'Brian')
        self.responses = [response]
        self.question = FillInTheBlankQuestion(before_prompt="", after_prompt="are the best", answer='YOU')
        self.answered_question = FillInTheBlankQuestion(before_prompt='', after_prompt="are the best",
                                                        object_id='be24d525'
                                                                  '-8904-4948-b47d-54248586986d',
                                                        answer='YOU', responses=self.responses)

    def test_json_data(self):
        self.assertEqual(self.question.json_data,
                         {'after_prompt': 'are the best',
                          'answer': 'YOU',
                          'before_prompt': '',
                          'object_id': 'be24d525-8904-4948-b47d-54248586986d',
                          'kind': 'question',
                          'responses': [],
                          'type': 'fill_in_the_blank'})

    def test_get_type(self):
        self.assertEqual(self.question.get_type(), 'fill_in_the_blank')

    def test_validate_response(self):
        response = MagicMock()
        self.question = MatchingQuestion(prompt="Match the following questions", left_choices={"A": 'Mike', "B": 'Ike'},
                                         right_choices={'C': 'Ike', 'D': 'Mike'}, answer={'A': 'C', 'B': 'D'})
        response.json_data = {'answer_mapping': {'A': 'C'}}
        self.question.validate_response(response)
        invalid_response_one = MagicMock()
        invalid_response_one.json_data = {'dog': 'A'}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_one)
        invalid_response_two = MagicMock()
        invalid_response_two.json_data = {'answer_mapping': {'F': 'C'}}
        with self.assertRaises(ValueError):
            self.question.validate_response(invalid_response_two)


if __name__ == '__main__':
    unittest.main()
