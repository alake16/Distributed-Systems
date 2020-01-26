from abc import ABC, abstractmethod, abstractproperty
from lxml import etree
from enum import Enum
import string
import itertools
import re

# TODO DRY
# TODO Redo the implementation and design. I think the main idea is that we want to eventually allow users
# to make interesting types of questions easily. Otherwise this might be unnecessary (over-engineered)


# This is prototype code and is going to be fragile/throwaway code.
# It is more to learn the best way to approach the problem.

# Function taken from https://stackoverflow.com/questions/30278539/python-cycle-through-the-alphabet


def alphabet_generator():
    for n in itertools.count():
        for t in itertools.product(string.ascii_lowercase, repeat=n):
            yield ''.join(t)


class DirectorOfCreation(ABC):

    class QuestionType(Enum):

        MULTIPLE_CHOICE = 1
        MATCHING = 2
        SHORT_ANSWER = 3
        FILL_IN_THE_BLANK = 4

    def __init__(self, type_of_builder, builder=None):
        if builder is None:
            builder = XMLQuizBuilder(type_of_builder)
        self.__builder = builder

    # TODO make these methods use the XMLQuizBuilder Class to provide convenience methods

    def get_multiple_choice_question(self, prompt, choices, correct_answer):
        pass

    def get_matching_question(self, prompt, left_choices, right_choices, correct_mapping):
        pass

    def get_short_answer_question(self, prompt, correct_answer):
        pass

    def get_fill_in_the_blank_question(self, prompt, correct_answer):
        pass

    def make_quiz_element(self):
        return etree.Element('quiz')

    def add_question_to_quiz_element(self, question, quiz):
        question = etree.SubElement(quiz, question)


class CLIDirectorOfCreation(DirectorOfCreation):
     
    def __init__(self, type_of_builder, builder=None):
        if builder is None:
            builder = XMLQuizBuilder(type_of_builder)
        self.__builder = builder

    def __get_type_of_question_from_user(self):
        option_string = "\nPlease select one of the following types of questions: \n\n" + "\n".join([member.name + ": \t" + str(member._value_) for name, member in DirectorOfCreation.QuestionType.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in DirectorOfCreation.QuestionType.__members__.items()]:
            option_input = input(option_string)
        type_of_question = DirectorOfCreation.QuestionType(int(option_input))
        return type_of_question

    def make_a_simple_question(self):
        type_of_question = self.__get_type_of_question_from_user()
        if type_of_question == DirectorOfCreation.QuestionType.MULTIPLE_CHOICE:
            print("You have selected to create a multiple choice question!\n\n")
            return self.create_multiple_choice_question()
        elif type_of_question == DirectorOfCreation.QuestionType.MATCHING:
            print("You have selected to create a matching question!\n\n")
            return self.create_matching_question()
        elif type_of_question == DirectorOfCreation.QuestionType.SHORT_ANSWER:
            print("You have selected to create a short_answer question!\n\n")
            return self.create_short_answer_question()
        elif type_of_question == DirectorOfCreation.QuestionType.FILL_IN_THE_BLANK:
            print("You have selected to create a fill in the blank question!")
            return self.create_fill_in_the_blank_question()

    # TODO change the way that an answer is verified from the user. Ideally, we would want to point at parent elements.
    # TODO change finished input to be something more robust
    # TODO Use helper methods to follow DRY principle
    def create_multiple_choice_question(self):
        multiple_choice_question = self.__builder.get_root_element()
        self.__builder.add_attribute_to_element(attribute="type", value="multiple choice",
                                                element=multiple_choice_question)
        print("Please enter the prompt for your multiple choice question:")
        prompt = input()
        self.__builder.add_prompt(prompt, parent_element=multiple_choice_question)
        answer_choice_generator = iter(alphabet_generator())
        next(answer_choice_generator)
        choice_prompt = None
        choices = {}
        while choice_prompt != 'finished':
            choice_key = next(answer_choice_generator)
            print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to finish adding choices')
            choice_prompt = input()
            if choice_prompt == 'finished':
                break
            self.__builder.add_choice(choice_prompt, choice_key, multiple_choice_question)
            choices[choice_key] = choice_prompt
        # TODO Render properly
        print("What is the answer to your question : " + " or ".join(choices.keys()))
        potential_answer = input().lower()
        if potential_answer not in choices.keys():
            input("Only enter one of " + " or ".join(choices.keys()))
        self.__builder.add_answer(potential_answer, multiple_choice_question)
        return multiple_choice_question

    def create_short_answer_question(self):
        short_answer_question = self.__builder.get_root_element()
        self.__builder.add_attribute_to_element(attribute="type", value="short answer question",
                                                element=short_answer_question)
        prompt = input("Please enter the prompt for your short answer question:")
        self.__builder.add_prompt(prompt, short_answer_question)
        print("What is the answer to your question?")
        answer = input()
        self.__builder.add_answer(answer, short_answer_question)
        return short_answer_question

    # TODO make use of the blank element to allow to render it properly.
    def create_fill_in_the_blank_question(self):
        fill_in_the_blank_question = self.__builder.get_root_element()
        self.__builder.add_attribute_to_element(attribute="type", value="fill in the blank",
                                                element=fill_in_the_blank_question)
        print("Please enter the prompt including the blank for your fill in the blank question:")
        prompt = input()
        print("What is the answer to your question?")
        answer = input()
        self.__builder.add_prompt(prompt=prompt, parent_element=fill_in_the_blank_question)
        self.__builder.add_answer(answer=answer, parent_element=fill_in_the_blank_question)
        return fill_in_the_blank_question

    # TODO add the answer mapping structure
    def create_matching_question(self):
        matching_question = self.__builder.get_root_element()
        self.__builder.add_attribute_to_element(attribute="type", value="matching", element=matching_question)
        print("Please enter the prompt for your matching question:")
        prompt = input()
        self.__builder.add_prompt(prompt, matching_question)
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
            self.__builder.add_left_choice(choice_prompt, choice_key, matching_question)
            left_choices[choice_key] = choice_prompt
        choice_prompt = None
        while choice_prompt != 'finished':
            choice_key = next(answer_choice_generator)
            print('Please enter choice ' + choice_key.upper() + ' or type \'finished\' to '
                                                                'finish adding right side choices')
            choice_prompt = input()
            if choice_prompt == 'finished':
                break
            self.__builder.add_right_choice(choice_prompt, choice_key, matching_question)
            right_choices[choice_key] = choice_prompt
        return matching_question


class XMLQuizBuilder:

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

    def add_blank(self, size_of_blank, parent_element):
        blank_element = etree.SubElement(parent_element, "blank")
        blank_text = '_' * size_of_blank
        self.add_text_to_element(blank_text, blank_element)
        return blank_element

    def get_root_element(self):
        return self.root_element


