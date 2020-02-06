from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
import string
import itertools
from typing import Dict
from Questions import MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion, Question


# TODO DRY
# TODO Redo the implementation and design. I think the main idea is that we want to eventually allow users
# to make interesting types of questions easily. Otherwise this might be unnecessary (over-engineered)


# This is prototype code and is going to be fragile/throwaway code.
# It is more to learn the best way to approach the problem.

# Function below was taken from https://stackoverflow.com/questions/30278539/python-cycle-through-the-alphabet


def alphabet_generator():
    for n in itertools.count():
        for t in itertools.product(string.ascii_lowercase, repeat=n):
            yield ''.join(t)


class DirectorOfCreation(ABC):

    def __init__(self):
        pass

    def get_multiple_choice_question_object(self, prompt: str, choices: Dict[str, str], correct_answer: str):
        return MultipleChoiceQuestion(prompt, choices, correct_answer)

    def get_matching_question_object(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str],
                                     correct_mapping: Dict[str, str]):
        return MatchingQuestion(prompt, left_choices, right_choices, correct_mapping)

    def get_short_answer_question_object(self, prompt: str, correct_answer: str):
        return ShortAnswerQuestion(prompt, correct_answer)

    def get_fill_in_the_blank_question_object(self, before_prompt: str, after_prompt: str, correct_answer: str):
        return FillInTheBlankQuestion(before_prompt, after_prompt, correct_answer)


class CLIDirectorOfCreation(DirectorOfCreation):

    def __init__(self):
        super().__init__()

    def __get_type_of_question_from_user(self):
        option_string = "\nPlease select one of the following types of questions: \n\n" + "\n".join(
            [member.name + ": \t" + str(member._value_) for name, member in QuestionType.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in QuestionType.__members__.items()]:
            option_input = input(option_string)
        type_of_question = QuestionType(int(option_input))
        return type_of_question

    def make_a_simple_question(self):
        type_of_question = self.__get_type_of_question_from_user()
        if type_of_question == QuestionType.MULTIPLE_CHOICE:
            print("You have selected to create a multiple choice question!\n\n")
            return self.create_multiple_choice_question()
        elif type_of_question == QuestionType.MATCHING:
            print("You have selected to create a matching question!\n\n")
            return self.create_matching_question()
        elif type_of_question == QuestionType.SHORT_ANSWER:
            print("You have selected to create a short_answer question!\n\n")
            return self.create_short_answer_question()
        elif type_of_question == QuestionType.FILL_IN_THE_BLANK:
            print("You have selected to create a fill in the blank question!\n\n")
            return create_fill_in_the_blank_question()
        elif type_of_question == QuestionType.PLAINTEXT:
            print("You have selected to create a plaintext question!\n\n")
            return self.create_plain_text_question()

    def _get_multiple_choice_data(self):
        print("Please enter the prompt for your multiple choice question:")
        prompt = input()
        choice_prompt = None
        choices = {}
        answer_choice_generator = iter(alphabet_generator())
        next(answer_choice_generator)
        while choice_prompt != 'finished':
            choice_key = next(answer_choice_generator)
            print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to finish adding choices')
            choice_prompt = input()
            if choice_prompt == 'finished':
                break
            choices[choice_key] = choice_prompt
        print("What is the answer to your question : " + " or ".join(choices.keys()))
        potential_answer = input().lower()
        while potential_answer not in list(choices.keys()):
            print("Only enter one of " + " or ".join(choices.keys()))
            potential_answer = input()
        return prompt, choices, potential_answer

    def create_multiple_choice_question(self):
        prompt, choices, potential_answer = self._get_multiple_choice_data()
        return MultipleChoiceQuestion(prompt, choices, potential_answer)

    def create_short_answer_question(self):
        prompt = input("Please enter the prompt for your short answer question:")
        print("What is the answer to your question?")
        answer = input()
        return ShortAnswerQuestion(prompt, answer)

    def _matching_helper(self):
        print("Please enter the prompt for your matching question:")
        prompt = input()
        answer_choice_generator = iter(alphabet_generator())
        next(answer_choice_generator)
        choice_prompt = None
        left_choices = {}
        right_choices = {}
        while choice_prompt != 'finished':
            choice_key = next(answer_choice_generator)
            print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to '
                                                                'finish adding left side choices')
            choice_prompt = input()
            if choice_prompt == 'finished':
                break
            left_choices[choice_key] = choice_prompt
        choice_prompt = None
        while choice_prompt != 'finished':
            print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to '
                                                                'finish adding right side choices')
            choice_prompt = input()
            if choice_prompt == 'finished':
                if len(left_choices) > len(right_choices):
                    print("Cannot have more left choices than right choices!")
                    print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to '
                                                                        'finish adding right side choices')
                    choice_prompt = None
                    continue
                else:
                    break
            right_choices[choice_key] = choice_prompt
            choice_key = next(answer_choice_generator)
        answer_mapping = {}
        right_choices_keys = list(right_choices.keys())
        for left_choice_key, left_choice_answer in left_choices.items():
            print("Please select the correct answer for the following left_choice: ")
            print(left_choice_key, left_choice_answer)
            print("The options available are " + " ".join(right_choices_keys))
            selection = ''
            while selection not in right_choices_keys:
                selection = input()
                print("The options available are " + " ".join(right_choices_keys))
            answer_mapping[left_choice_key] = selection
            right_choices_keys.remove(selection)
        return prompt, left_choices, right_choices, answer_mapping

    def create_matching_question(self):
        prompt, left_choices, right_choices, answer_mapping = self._matching_helper()
        return MatchingQuestion(prompt, left_choices, right_choices, answer_mapping)

    def create_fill_in_the_blank_question(self):
        print("Please enter the prompt before the blank: ")
        before_blank = input()
        print("Please enter the prompt after the blank: ")
        after_blank = input()
        print("What is the answer to your question?")
        answer = input()
        return FillInTheBlankQuestion(before_blank, after_blank, answer)
