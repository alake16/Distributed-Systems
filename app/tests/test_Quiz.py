import unittest
from unittest.mock import patch, MagicMock
from app.Models.Quiz import Quiz
from app.Models.Questions import MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion
import app


class TestQuiz(unittest.TestCase):

    def setUp(self) -> None:
        self.quiz_json = {
    "kind": "quiz",
    "object_id": "3945769a-9b6f-4feb-b292-f3e8958a59d3",
    "name": "Brian's First Quiz",
    "questions": [
        {
            "kind": "question",
            "object_id": "751f9e7a-cbcc-41d8-816e-d65f6fdafe23",
            "type": "multiple_choice",
            "prompt": "Who is the best?",
            "choices": [
                "Mike",
                "Domingo"
            ],
            "answer": "Mike",
            "responses": [
                {
                    "kind": "response",
                    "type": "multiple_choice",
                    "choice": "Mike",
                    "user_id": "1345125",
                    "nickname": "Brian"
                }
            ]
        },
        {
            "kind": "question",
            "object_id": "3e77b67d-0f2a-421f-8bde-c1abbc99af99",
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
        },
        {
            "kind": "question",
            "object_id": "e25a2238-544d-4581-917b-f74916b0060f",
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
        },
        {
            "kind": "question",
            "object_id": "cc4b4a25-2390-40f3-bc8c-7efe263d9212",
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
