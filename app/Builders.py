from Questions import MultipleChoiceQuestion, MatchingQuestion
from abc import ABC, abstractmethod, abstractproperty
from typing import Any
from lxml import etree
from enum import Enum
import copy 
import string
import itertools


#### THIS WAS TAKEN FROM https://stackoverflow.com/questions/30278539/python-cycle-through-the-alphabet
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
    
    def get_multiple_choice_question(self, prompt, choices, correct_answer):
        question_xml_element = etree.Element("question")
        question_xml_element.attrib['type'] = 'multiple choice'
        for choice in choices:
            choice_element = etree.SubElement(question_xml_element, choice)
        answer_element = etree.SubElement(question_xml_element, correct_answer)
        return question_xml_element

    def get_matching_question(self, prompt, left_choices, right_choices, correct_mapping):
        pass

    def get_short_answer_question(self, prompt, correct_answer):
        pass

    def get_fill_in_the_blank_question(self, prompt, correct_answer):
        pass


class CLIDirectorOfCreation(DirectorOfCreation):
     
    def __init__(self, type_of_builder, builder=None):
        if builder is None:
            builder = XMLQuizBuilder(type_of_builder)
        self.__builder = builder

    def __get_type_of_question_from_user(self) -> str:
        option_string = "\nPlease select one of the following types of questions: \n\n" + "\n".join([member.name + ": \t" + str(member._value_) for name, member in DirectorOfCreation.QuestionType.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in DirectorOfCreation.QuestionType.__members__.items()]:
            option_input = input(option_string)
        type_of_question = DirectorOfCreation.QuestionType(int(option_input))
        return type_of_question

    def make_a_simple_question(self):
        type_of_question = self.__get_type_of_question_from_user()
        if type_of_question == DirectorOfCreation.QuestionType.MULTIPLE_CHOICE:
            return self.create_multiple_choice_question()
        elif type_of_question == DirectorOfCreation.Option.MATCHING:
            return self.create_matching_question()
        elif type_of_queston == DirectorOfCreation.Option.SHORT_ANSWER:
            return self.create_short_answer()
        elif type_of_queston == DirectorOfCreation.Option.FILL_IN_THE_BLANK:
            return self.create_fill_in_the_blank()

    def create_multiple_choice_question(self):
        multiple_choice_question = self.__builder.get_root_element()
        print("You have selected to create a multiple choice question!\n\n")
        prompt = input("Please enter the prompt for your multiple_choice_question")
        self.__builder.add_prompt(prompt, multiple_choice_question)
        answer_choice_generator = iter(alphabet_generator())
        next(answer_choice_generator)
        selection = None
        choices = {}
        while selection != 'finished':
            next_answer_choice = next(answer_choice_generator)
            print('Please enter choice ' + next_answer_choice.upper() + ' or type \'finished\' to finish adding choices')
            selection = input()
            if selection == 'finished':
                break
            choice = next_answer_choice
            self.__builder.add_choice(choice, multiple_choice_question)
            choices[choice] = selection
        #TODO Render properly
        print("What is the answer to your question : " + " or ".join(choices.keys()))
        potential_answer = input().lower()
        if potential_answer not in choices.keys():
            input("Only enter one of " + " or ".join(choices.keys()))
        return multiple_choice_question

class XMLQuizBuilder:

    def __init__(self, element_type):
        self.root_element = etree.Element(element_type)

    root_element = etree.Element("question")

    def add_prompt(self, prompt, root):
        prompt_element = etree.SubElement(root, "prompt")
        self.add_text_to_element(prompt, prompt_element)
        return prompt_element
        
    def add_text_to_element(self, text, element):
        element.text = text

    def add_attribute_to_element(self, attribute: str, value: str, element):
        element.attrib[attribute] = value
        return

    def add_choice(self, choice, root):
        choice_element = etree.SubElement(root, "choice")
        self.add_text_to_element(choice, choice_element)
        return choice_element

    def add_left_choice(self, left_choice, root):
        pass
    
    def add_right_choice(right_choice, root):
        pass

    def add_answer(self, answer, root):
        answer_element = etree.SubElement(root, "answer")
        self.add_text_to_element(answer, answer_element)
        return answer_element

    def add_blank(self):
        pass

    def get_root_element(self):
        return self.root_element


