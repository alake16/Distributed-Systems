from typing import Dict
import textwrap
import itertools
from abc import ABC, abstractmethod


# The use of the dataclass decorator really simplifies the implementation.
class Question(ABC):
    
    @abstractmethod
    def quiz_view(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass


class MultipleChoiceQuestion(Question):

    def __init__(self, prompt: str, choices: Dict[str, str], answer: str):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer
        self.response = {choice: 0 for choice in choices}

    def quiz_view(self):
        prompt_string_wrapped = textwrap.fill(self.prompt)
        choices = [ textwrap.fill(choice_key.upper() + ': ' + choice_text) for choice_key, choice_text in self.choices.items()]
        answer = textwrap.fill(self.answer)
        return prompt_string_wrapped + '\n' + '\n'.join(choices) + '\n\n' 

    def __str__(self):
        return self.quiz_view() + "Answer: " + self.answer.upper()


class MatchingQuestion(Question):

    def __init__(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str], answer_mapping: Dict[str, str]):
        self.prompt = prompt
        self.left_choices = left_choices
        self.right_choices = right_choices
        self.answer_mapping = answer_mapping

    def quiz_view(self):
        pass

    def __str__(self):
        matching_representation = itertools.zip_longest(self.left_choices, self.right_choices, fillvalue='')
        pass


class ShortAnswerQuestion(Question):
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

    def quiz_view(self):
        pass

    def __str__(self):
        pass


class FillInTheBlankQuestion(Question):

    def __init__(self, before_prompt: str, after_prompt: str, correct_answer: str):
        self.before_prompt = before_prompt
        self.after_prompt = after_prompt
        self.answer = correct_answer

    def quiz_view(self):
        pass

    def __str__(self):
        pass



