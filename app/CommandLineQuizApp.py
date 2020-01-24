from Questions import MultipleChoiceQuestion
from Renderer import render_question
import copy
from typing import List, Dict

class QuizBuilder:

    # TODO Soft-code this.
    QUIZLETTERS  = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z') 

    def __init__(self, type_of_builder: str = 'cli'):
        self.questions: List[Dict] = []

    def greet(self) -> None:
        print("Welcome to Quizilicious, the open-source distributed quiz application!")

    #TODO refactor to soft-coded question_types from a configuration.
    def __ask_for_type_of_question(self) -> str:
        print('Please choose one of the following types of questions: A: Multiple Choice, B: Matching, C: Short Answer, D: Fill in the Blank')
        question_type = input()
        if question_type.lower() == 'a':
            return 'multiple choice'
        elif question_type.lower() == 'b':
            return "matching"
        elif question_type.lower() == 'c':
            return "short answer"
        elif question_type.lower() == 'd':
            return "fill in the blank"

    #TODO Make this thread-safe if not already. Simply make a lock for now but ideally, we will use a different model.
    #TODO QUIZLETTERS is global and couples the implementation of QUIZLETTERS to this function. Ideally, we want to abstract this to a generator function that takes a callable as an argument.
    def accept_question(self) -> None:
        type_of_question = self.__ask_for_type_of_question()
        print('You have selected to create a ' + type_of_question + ' question. Please enter the multiple choice prompt:')
        prompt = input()
        selection = None
        answer_choices = iter(QuizBuilder.QUIZLETTERS)
        choices = {}
        while selection != 'finished':
            next_answer_choice = next(answer_choices)
            print('Please enter choice ' + next_answer_choice.upper() + ' or type \'finished\' to finish adding choices')
            selection = input()
            if selection == 'finished':
                break
            choices[next_answer_choice] = selection
        print("What is the answer to your question: " + " or ".join(choices.keys()))
        potential_answer = input().lower()
        if potential_answer not in choices.keys():
            input("Only enter one of " + " or ".join(choices.keys()))

        multi_choice = MultipleChoiceQuestion(prompt, choices, potential_answer)
        print("Here is your question:\n")
        render_question(multi_choice, is_quiz=False)
        self.questions.append(multi_choice)
        return

    def accept_questions(self):
        return self.accept_question()

    def get_questions(self) -> List[Dict]:
        return copy.deepcopy(self.questions)


if __name__ == '__main__':
    quiz_builder = QuizBuilder()
    quiz_builder.accept_question()
