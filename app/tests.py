import unittest
from unittest.mock import patch, call
from io import StringIO
from CommandLineQuizApp import QuizBuilder
from Questions import MultipleChoiceQuestion
from typing import List
import sys

class TestReadingXML(unittest.TestCase):

    # Integration test. Ideally, this is the functional testing. However, we will add separate unit tests that more throughly test each function for increased code coverage.
    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_app_cli(self, mocked_print, mocked_input):
        # User is greeted with name of Quiz App and a short description when using the CLI
        quiz_builder = QuizBuilder('cli')
        quiz_builder.greet()
        calls_to_print = []
        calls_to_print.append(call("Welcome to Quizilicious, the open-source distributed quiz application!"))
        mocked_print.assert_has_calls(calls_to_print, any_order=False)

        # User is asked what kind of question they would like to enter.
        # A: Multiple Choice, B: Matching, C: Short Answer, D: Fill in the Blank.
        # They choose A: multiple choice and ultimately creates two multiple choice questions and a matching question.
        mocked_input.side_effect = ['A', "Who is a good boy?", "Hachi the Dog", "Jerry from Tom and Jerry", "Rudolph", "Michael Jordan", 'finished', 'A']
        question = quiz_builder.accept_question()
        calls_to_print.append(call('Please choose one of the following types of questions: A: Multiple Choice, B: Matching, C: Short Answer, D: Fill in the Blank'))
        calls_to_print.append(call('You have selected to create a multiple choice question. Please enter the multiple choice prompt:'))

        # Instructor adds choices and their text for a multiple choice question
        for letter in ['A', 'B', 'C', 'D', 'E']:
            calls_to_print.append(call('Please enter choice ' + letter + ' or type \'finished\' to finish adding choices'))

        # User is asked to enter the result of their question
        calls_to_print.append(call('What is the answer to your question: a or b or c or d'))
        # Question is displayed to user
        calls_to_print.append(call("Here is your question:\n"))
        calls_to_print.append(call(MultipleChoiceQuestion(prompt='Who is a good boy?', choices={'a': 'Hachi the Dog', 'b': 'Jerry from Tom and Jerry', 'c': 'Rudolph', 'd': 'Michael Jordan'}, answer='a')))
        # Check that the output to the terminal is as it should be

        # Questions are persisted(Right now to a list)
        questions: List = quiz_builder.get_questions()

        assert MultipleChoiceQuestion(prompt='Who is a good boy?', choices={'a': 'Hachi the Dog', 'b': 'Jerry from Tom and Jerry', 'c': 'Rudolph', 'd': 'Michael Jordan'}, answer='a') in questions

        # User is asked if they would like to add another multiple choice question
        calls_to_print.append(call('Please choose one of the following types of questions: A: Multiple Choice, B: Matching, C: Short Answer, D: Fill in the Blank or type \'finished\''))
        mocked_print.assert_has_calls(calls_to_print, any_order=False)

        # Quiz is persisted.

        # User gives Quiz. Next Person comes in and takes it on command prompt.

        # Each question is displayed. The questions are in random order.

        # The user gives an answer to each question.

        # The user is given a partial score.

if __name__ == '__main__':
    unittest.main()
