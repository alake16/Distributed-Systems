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
                            'question_id': '5fd59f54-ba3d-4045-8db6-b7487103e3e1',
                            "kind": "response",
                            "type": "multiple_choice",
                            "answer": "B",
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
                    "left_choices": [
                        "Mike",
                        "Ike"
                    ],
                    "right_choices": [
                        "Ike",
                        "Mike"
                    ],
                    "answer": {
                        "Ike": "Mike",
                        "Mike": "Ike"
                    },
                    "responses": [
                        {
                            'question_id': 'd3d46649-4dbb-4d6b-b1fe-5f87f5b42756',
                            "kind": "response",
                            "type": "matching",
                            "answer": {
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
                            'question_id': "e00a3f6d-3ab7-4cb4-8441-6584a785f50d",
                            "kind": "response",
                            "type": "short_answer",
                            "answer": "YOU",
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
                            'question_id': "ab2cc19d-3d31-4ba9-8b90-ae1c8e035884",
                            "kind": "response",
                            "type": "fill_in_the_blank",
                            "answer": "YOU",
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
        """
        Ensures that the quiz object can have questions added to it.
        The question is mocked to prevent changes to the question interface affecting the quiz tests.
        :return:
        """
        question = MagicMock(spec=MatchingQuestion)
        quiz = Quiz.load_quiz_from_json(self.quiz_json)
        quiz.add_question_to_quiz(question)
        self.assertIsInstance(quiz.get_question(4), MatchingQuestion)

    def test_get_question(self):
        """
        Ensures that all questions can be retrieved using quiz.get_question(index_of_question)
        :return:
        """
        self.assertIsInstance(self.quiz.get_question(0), MultipleChoiceQuestion)
        self.assertIsInstance(self.quiz.get_question(1), MatchingQuestion)
        self.assertIsInstance(self.quiz.get_question(2), ShortAnswerQuestion)
        self.assertIsInstance(self.quiz.get_question(3), FillInTheBlankQuestion)

    def test_json_data(self):
        """
        Ensures that the json_data property returns an accurate representation of the Quiz object.
        :return:
        """
        self.assertEqual(self.quiz.json_data, self.quiz_json)


if __name__ == '__main__':
    unittest.main()