import unittest
from unittest.mock import patch, Mock, MagicMock
from app.Models.Questions import Question, MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, \
    FillInTheBlankQuestion
from app.Models.Response import MultipleChoiceResponse, Response
import uuid
import json


class TestQuestion(unittest.TestCase):
    def test_json_data(self):
        pass

    def test_get_type(self):
        pass

    @patch('app.Models.Questions.MultipleChoiceQuestion.__init__', return_value=None)
    def test_create_a_multiple_choice_question_from_json(self, mock_init):
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
        question = Question.create_a_question(multiple_choice_question_json)
        self.assertIsInstance(question, MultipleChoiceQuestion)
        mock_init.assert_called_once_with(answer='A', choices={'A': 'Mike', 'B': 'Domingo'},
                                          id='c777ff3a-270e-447a-ad49-12006e04cb36', prompt='Who is the best?',
                                          responses=[{'kind': 'response', 'type': 'multiple_choice', 'choice': 'B',
                                                      'user_id': '1345125', 'nickname': 'Brian'}])

    @patch('app.Models.Questions.MatchingQuestion.__init__', return_value=None)
    def test_create_a_matching_question_from_json(self, mock_init):
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
        question = Question.create_a_question(matching_json)
        self.assertIsInstance(question, MatchingQuestion)
        mock_init.assert_called_once_with(answer={'A': 'C', 'B': 'D'}, id='d3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
                                          left_choices={'A': 'Mike', 'B': 'Ike'},
                                          prompt='Match the following questions',
                                          responses=[{'kind': 'response', 'type': 'matching',
                                                      'answer_mapping': {'A': 'C', 'B': 'D'},
                                                      'user_id': '1345125', 'nickname': 'Brian'}],
                                          right_choices={'C': 'Ike', 'D': 'Mike'})

    def test_add_response(self):
        pass

    def test__initialize_responses(self):
        pass

    def test_validate_response(self):
        pass

    def test_get_responses(self):
        pass


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
        self.answered_question = MultipleChoiceQuestion(prompt="Who is the best?", id='be24d525-8904-4948-b47d'
                                                                                      '-54248586986d',
                                                        choices={"A": "Mike", "B": 'Domingo'},
                                                        answer='A', responses=self.responses)

    def test_init(self):
        """
        This makes sure the __init__ function works properly.
        :return:
        """
        self.assertEqual(self.multiple_choice_question.prompt, 'Who is the best?')
        self.assertEqual(self.multiple_choice_question.choices, {"A": 'Mike', "B": 'Domingo'})
        self.assertEqual(self.multiple_choice_question.answer, 'A')
        self.assertEqual(self.multiple_choice_question.id, 'be24d525-8904-4948-b47d-54248586986d')
        self.assertEqual(self.multiple_choice_question._responses, [])
        self.assertEqual(self.answered_question.prompt, 'Who is the best?')
        self.assertEqual(self.answered_question.choices, {"A": 'Mike', "B": 'Domingo'})
        self.assertEqual(self.answered_question.answer, 'A')
        self.assertEqual(self.answered_question._responses,
                         [Response.create_a_response(response) for response in self.responses])

    def test_json_data(self):
        self.assertEqual(self.multiple_choice_question.json_data,
                         {'answer': 'A', 'choices': {'A': 'Mike', 'B': 'Domingo'},
                          'id': 'be24d525-8904-4948-b47d-54248586986d', 'kind': 'question',
                          'prompt': 'Who is the best?', 'responses': [], 'type': 'multiple_choice'})

    def test_validate_response(self):
        pass

    def test_get_responses(self):
        pass


class TestMatchingQuestion(unittest.TestCase):
    def test_validate_response(self):
        self.fail()

    def test_json_data(self):
        self.fail()


class TestShortAnswerQuestion(unittest.TestCase):
    def test_validate_response(self):
        self.fail()

    def test_json_data(self):
        self.fail()


class TestFillInTheBlankQuestion(unittest.TestCase):
    def test_validate_response(self):
        self.fail()

    def test_json_data(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
