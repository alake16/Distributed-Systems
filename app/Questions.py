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

    def quiz_view(self):
        prompt_string_wrapped = textwrap.fill(self.prompt)
        choices = [ textwrap.fill(choice_key.upper() + ': ' + choice_text) for choice_key, choice_text in self.choices.items()]
        answer = textwrap.fill(self.answer)
        return prompt_string_wrapped + '\n' + '\n'.join(choices) + '\n\n' + "Answer: " + answer.upper()

    def __str__(self):
        return self.quiz_view() + "Answer: " + answer.upper()

class MatchingQuestion(Question):
    prompt: str or None
    left_choices: Dict[str, str]
    right_choices: Dict[str, str]

    def __init__(self, prompt: str, left_choices: Dict[str, str], right_choices: Dict[str, str], answer):
        self.prompt = prompt
        self.left_choices = left_choices
        self.right_choies = right_choices
        self.answer = answer

    def quiz_view(self):
        pass

    def __str__(self):
        matching_representation = itertools.zip_longest(self.left_choices, self.right_choices, fillvalue='')
