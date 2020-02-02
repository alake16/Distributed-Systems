from abc import ABC, abstractmethod, abstractproperty
from lxml import etree
from enum import Enum
import string
import itertools
from typing import Dict
from Questions import MultipleChoiceQuestion, MatchingQuestion, ShortAnswerQuestion, FillInTheBlankQuestion

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

class QuestionType(Enum):

    MULTIPLE_CHOICE = 1
    MATCHING = 2
    SHORT_ANSWER = 3
    FILL_IN_THE_BLANK = 4
    PLAINTEXT = 5


class DirectorOfCreation(ABC):

    def __init__(self, type_of_builder, builder=None):
        if builder is None:
            builder = XMLQuizBuilder(type_of_builder)
        self.__builder = builder

    def get_multiple_choice_question_object(self, prompt: str, choices: Dict[str, str], correct_answer: str):
        return MultipleChoiceQuestion(prompt, choices, correct_answer)

    def get_matching_question_object(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str], correct_mapping: Dict[str, str]):
        return MatchingQuestion(prompt, left_choices, right_choices, correct_mapping)

    def get_short_answer_question_object(self, prompt: str, correct_answer: str):
        return ShortAnswerQuestion(prompt, correct_answer)

    def get_fill_in_the_blank_question_object(self, before_prompt: str, after_prompt: str, correct_answer: str):
        return FillInTheBlankQuestion(before_prompt, after_prompt, correct_answer)


class CLIDirectorOfCreation(DirectorOfCreation):
     
    def __init__(self, type_of_builder, builder=None):
        if builder is None:
            builder = XMLQuizBuilder(type_of_builder)
        self.__builder = builder

    def __get_type_of_question_from_user(self):
        option_string = "\nPlease select one of the following types of questions: \n\n" + "\n".join([member.name + ": \t" + str(member._value_) for name, member in QuestionType.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in QuestionType.__members__.items()]:
            option_input = input(option_string)
        type_of_question = QuestionType(int(option_input))
        return type_of_question

    def make_a_simple_question(self, return_xml=True):
        type_of_question = self.__get_type_of_question_from_user()
        if type_of_question == QuestionType.MULTIPLE_CHOICE:
            print("You have selected to create a multiple choice question!\n\n")
            return self.create_multiple_choice_question(return_xml)
        elif type_of_question == QuestionType.MATCHING:
            print("You have selected to create a matching question!\n\n")
            return self.create_matching_question(return_xml)
        elif type_of_question == QuestionType.SHORT_ANSWER:
            print("You have selected to create a short_answer question!\n\n")
            return self.create_short_answer_question(return_xml)
        elif type_of_question == QuestionType.FILL_IN_THE_BLANK:
            print("You have selected to create a fill in the blank question!\n\n")
            return self.create_fill_in_the_blank_question(return_xml)
        elif type_of_question == QuestionType.PLAINTEXT:
            print("You have selected to create a plaintext question!\n\n")
            return self.create_plain_text_question(return_xml)

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

    # TODO change finished input to be something more robust
    def create_multiple_choice_question(self, return_xml=True):
        prompt, choices, potential_answer = self._get_multiple_choice_data()
        if return_xml is False:
            return MultipleChoiceQuestion(prompt, choices, potential_answer)
        else:
            multiple_choice_question = self.__builder.get_root_element()
            self.__builder.add_attribute_to_element(attribute="type", value="multiple choice",
                                                    element=multiple_choice_question)
            self.__builder.add_prompt(prompt, multiple_choice_question)
            for choice_key in choices.keys():
                choice_prompt = choices[choice_key]
                self.__builder.add_choice(choice_prompt, choice_key, multiple_choice_question)
            self.__builder.add_answer(potential_answer, multiple_choice_question)
            return multiple_choice_question

    def create_short_answer_question(self, return_xml=True):
        prompt = input("Please enter the prompt for your short answer question:")
        print("What is the answer to your question?")
        answer = input()
        if return_xml is False:
            return ShortAnswerQuestion(prompt, answer)
        else:
            short_answer_question = self.__builder.get_root_element()
            self.__builder.add_attribute_to_element(attribute="type", value="short answer question",
                                                element=short_answer_question)
            self.__builder.add_prompt(prompt, short_answer_question)
            self.__builder.add_answer(answer, short_answer_question)
            return short_answer_question

    # TODO make use of the blank element to allow to render it properly.
    def create_fill_in_the_blank_question(self, return_xml=True):
        print("Please enter the prompt before the blank: ")
        before_blank = input()
        print("Please enter the prompt after the blank: ")
        after_blank = input()
        print("What is the answer to your question?")
        answer = input()
        if return_xml is False:
            return FillInTheBlankQuestion(before_blank, after_blank, answer)
        else:
            fill_in_the_blank_question = self.__builder.get_root_element()
            self.__builder.add_attribute_to_element(attribute="type", value="fill in the blank",
                                                element=fill_in_the_blank_question)
            self.__builder.add_before_blank(before_text=before_blank, parent_element=fill_in_the_blank_question)
            self.__builder.add_blank(size_of_blank=7, parent_element=fill_in_the_blank_question)
            self.__builder.add_after_blank(after_text=after_blank, parent_element=fill_in_the_blank_question)
            self.__builder.add_answer(answer=answer, parent_element=fill_in_the_blank_question)
        return fill_in_the_blank_question

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

    def create_matching_question(self, return_xml=True):
        prompt, left_choices, right_choices, answer_mapping = self._matching_helper()
        if return_xml is False:
            return MatchingQuestion(prompt, left_choices, right_choices, answer_mapping)
        else:
            matching_question = self.__builder.get_root_element()
            self.__builder.add_attribute_to_element(attribute="type", value="matching", element=matching_question)
            for left_choice_key in left_choices:
                left_choice_text = left_choices[left_choice_key]
                self.__builder.add_left_choice(left_choice_text, left_choice_key, matching_question)
            for right_choice_key in right_choices:
                right_choice_text = right_choices[right_choice_key]
                self.__builder.add_right_choice(right_choice_text, right_choice_key, matching_question)
            for left_key, right_key in answer_mapping.items():
                self.__builder.add_left_to_right(left_key, right_key, matching_question)
        return matching_question


class XMLQuizBuilder:

    # TODO move this to a separate module where it can be insulated from changes to this module.
    # TODO redo this to not be instantiated with an element type
    def __init__(self, element_type):
        self.root_element = etree.Element(element_type)

    def add_prompt(self, prompt, parent_element):
        prompt_element = etree.SubElement(parent_element, "prompt")
        self.add_text_to_element(prompt, prompt_element)
        return prompt_element
        
    def add_text_to_element(self, text, element):
        element.text = text
        return element

    def add_attribute_to_element(self, attribute: str, value: str, element):
        element.attrib[attribute] = value
        return element

    def add_choice(self, choice_text, choice_key, parent_element):
        choice_element = etree.SubElement(parent_element, "choice")
        self.add_attribute_to_element("choice_key", choice_key, choice_element)
        self.add_text_to_element(choice_text, choice_element)
        return choice_element

    def add_left_choice(self, left_choice_text, choice_key, parent_element):
        left_choice_element = etree.SubElement(parent_element, "left_choice")
        self.add_attribute_to_element("choice_key", choice_key, left_choice_element)
        self.add_text_to_element(left_choice_text, left_choice_element)
        return left_choice_element
    
    def add_right_choice(self, right_choice_text, choice_key, parent_element):
        right_choice_element = etree.SubElement(parent_element, "right_choice")
        self.add_attribute_to_element("choice_key", choice_key, right_choice_element)
        self.add_text_to_element(right_choice_text, right_choice_element)
        return right_choice_element

    def add_answer(self, answer, parent_element):
        answer_element = etree.SubElement(parent_element, "answer")
        self.add_text_to_element(answer, answer_element)
        return answer_element

    def add_before_blank(self, before_text, parent_element):
        before_blank_element = etree.SubElement(parent_element, "before_blank")
        self.add_text_to_element(before_text, before_blank_element)
        return before_blank_element

    def add_after_blank(self, after_text, parent_element):
        after_blank_element = etree.SubElement(parent_element, "after_blank")
        self.add_text_to_element(after_text, after_blank_element)
        return after_blank_element

    def add_blank(self, size_of_blank, parent_element):
        if size_of_blank is None:
            size_of_blank = 7
        blank_element = etree.SubElement(parent_element, "blank")
        blank_text = '_' * size_of_blank
        self.add_text_to_element(blank_text, blank_element)
        return blank_element

    def add_left_to_right(self, left_key, right_key, parent_element):
        left_to_right_element = etree.SubElement(parent_element, "left_to_right")
        left_element = etree.SubElement(left_to_right_element, "left")
        self.add_text_to_element(left_key, left_element)
        right_element = etree.SubElement(left_to_right_element, "right")
        self.add_text_to_element(right_key, right_element)
        return left_to_right_element

    def get_root_element(self):
        return self.root_element









