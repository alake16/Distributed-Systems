import unittest
from unittest.mock import patch, call
from io import StringIO
from CommandLineQuizApp import CommandLineApplication
from Questions import MultipleChoiceQuestion
from typing import List
import sys

class TestReadingXML(unittest.TestCase):

    # Integration test. Ideally, this is the functional testing. However, we will add separate unit tests that more throughly test each function for increased code coverage.
    @patch('builtins.input')
    @patch('builtins.print')
    def test_quiz_app_cli(self, mocked_print, mocked_input):
        # User is greeted with name of Quiz App and a short description when using the CLI
        mocked_input.side_effect = ['2', '1', "Who is a good boy?", "Hachi the Dog", "Jerry from Tom and Jerry", "Rudolph", "Michael Jordan", 'finished', 'A']
        command_line_app = CommandLineApplication("Welcome to Quizilicious, the open-source distributed quiz application!")
        command_line_app.run()
        calls_to_print = []
        calls_to_print.append(call("Welcome to Quizilicious, the open-source distributed quiz application!"))
        mocked_print.assert_has_calls(calls_to_print, any_order=False)

        # User is asked what kind of question they would like to enter.
        # A: Multiple Choice, B: Matching, C: Short Answer, D: Fill in the Blank.
        # They choose A: multiple choice and ultimately creates two multiple choice questions and a matching question.

        # Instructor adds choices and their text for a multiple choice question

        # Check that the output to the terminal is as it should be

        # Questions are persisted(Right now to a list

        # Quiz is persisted.

        # User gives Quiz. Next Person comes in and takes it on command prompt.

        # Each question is displayed. The questions are in random order.

        # The user gives an answer to each question.

        # The user is given a partial score.

if __name__ == '__main__':
    unittest.main()
