import unittest
from unittest.mock import patch, MagicMock
from app.Models.Quiz import Quiz
from app.Models.Questions import MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion
import app


class TestQuiz(unittest.TestCase):

    def setUp(self) -> None:
        self.quiz_json = {
            "kind": "quiz",
            "object_id": "e49232ba-2434-4d40-9a0a-026a5e304cd2",
            "name": "Brian's First Quiz",
            "questions": [
                {
                    "kind": "question",
                    "object_id": "5fd59f54-ba3d-4045-8db6-b7487103e3e1",
                    "type": "multiple_choice",
                    "prompt": "Who is the best?",
                    "choices": {
                        "A": "Mike",
                        "B": "Domingo"
                    },
                    "answer": "A",
                    "responses": [
                        {
                            'question_id': '5fd59f54-ba3d-4045-8db6-b7487103e3e1',
                            "kind": "response",
                            "type": "multiple_choice",
                            "choice": "B",
                            "user_id": "1345125",
                            "nickname": "Brian"
                        }
                    ]
                },
                {
                    "kind": "question",
                    "object_id": "d3d46649-4dbb-4d6b-b1fe-5f87f5b42756",
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
                    ]
                },
                {
                    "kind": "question",
                    "object_id": "e00a3f6d-3ab7-4cb4-8441-6584a785f50d",
                    "type": "short_answer",
                    "prompt": "Who is the best?",
                    "answer": "YOU",
                    "responses": [
                        {
                            'question_id': "e00a3f6d-3ab7-4cb4-8441-6584a785f50d",
                            "kind": "response",
                            "type": "short_answer",
                            "short_answer": "YOU",
                            "user_id": "1345125",
                            "nickname": "Brian"
                        }
                    ]
                },
                {
                    "kind": "question",
                    "object_id": "ab2cc19d-3d31-4ba9-8b90-ae1c8e035884",
                    "type": "fill_in_the_blank",
                    "before_prompt": "",
                    "after_prompt": "are the best",
                    "answer": "YOU",
                    "responses": [
                        {
                            'question_id': "ab2cc19d-3d31-4ba9-8b90-ae1c8e035884",
                            "kind": "response",
                            "type": "fill_in_the_blank",
                            "blank_answer": "YOU",
                            "user_id": "1345125",
                            "nickname": "Brian"
                        }
                    ]
                }
            ]
        }
        self.quiz = Quiz.load_quiz_from_json(self.quiz_json)

    def test_load_quiz_from_json(self):
        with patch('app.Models.Quiz.Quiz.__init__') as mock_init:
            mock_init.return_value = None
            Quiz.load_quiz_from_json(self.quiz_json)
            mock_init.assert_called()

    def test_add_question_to_quiz(self):
        question = MagicMock(spec=MatchingQuestion)
        quiz = Quiz.load_quiz_from_json(self.quiz_json)
        quiz.add_question_to_quiz(question)
        self.assertIsInstance(quiz.get_question(4), MatchingQuestion)

    def test_get_question(self):
        self.assertIsInstance(self.quiz.get_question(0), MultipleChoiceQuestion)
        self.assertIsInstance(self.quiz.get_question(1), MatchingQuestion)
        self.assertIsInstance(self.quiz.get_question(2), ShortAnswerQuestion)
        self.assertIsInstance(self.quiz.get_question(3), FillInTheBlankQuestion)

    def test_json_data(self):
        self.assertEqual(self.quiz.json_data, self.quiz_json)


if __name__ == '__main__':
    unittest.main()
