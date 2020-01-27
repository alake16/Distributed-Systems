import copy
from typing import List, Dict
from enum import Enum
from Builders import CLIDirectorOfCreation, XMLQuizBuilder
from lxml import etree

class CommandLineApplication:

    class Options(Enum):

        TAKE_A_QUIZ = 1
        CREATE_A_QUIZ = 2

    def __init__(self, greeting):
        self.greeting = greeting

    def __greet_user(self):
        print(self.greeting)

    def __select_option(self):
        option_string = "\nPlease select one of the following: \n\n" + "\n".join([member.name + ": \t" + str(member._value_) for name, member in CommandLineApplication.Options.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in
                                   CommandLineApplication.Options.__members__.items()]:
            option_input = input(option_string)
        option = CommandLineApplication.Options(int(option_input))
        return option
  
    def run(self):
        self.__greet_user()
        option = self.__select_option()
        if option == CommandLineApplication.Options.CREATE_A_QUIZ:
            quiz = []
            user_wants_to_make_a_question = True
            while user_wants_to_make_a_question:
                question_creator = CLIDirectorOfCreation('question')
                question = question_creator.make_a_simple_question(return_xml=False)
                quiz.append(question)
                print("\n")
                answer = ''
                while answer.lower() not in ['yes', 'no']:
                    print("Would you like to make another question? Please type 'yes' or 'no':")
                    answer = input()
                if answer == 'no':
                    user_wants_to_make_a_question = False
        elif option == CommandLineApplication.Options.TAKE_A_QUIZ:
            pass

        
if __name__ == "__main__":
    command_line_application = CommandLineApplication("Welcome to the Quiz Application!")
    command_line_application.run()



