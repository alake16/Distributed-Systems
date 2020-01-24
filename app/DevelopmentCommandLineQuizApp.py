from Questions import MultipleChoiceQuestion
from Renderer import render_question
import copy
from typing import List, Dict
from enum import Enum
from Builders import CLIDirectorOfCreation

class CommandLineApplication:

    class Options(Enum):

        TAKE_A_QUIZ = 1
        CREATE_A_QUIZ = 2

    def __init__(self, greeting):
        self.greeting = greeting

    def __greet_user(self):
        print(self.greeting)

    def __select_option(self) -> Options:
        option_string = "\nPlease select one of the following: \n\n" + "\n".join([member.name + ": \t" + str(member._value_) for name, member in CommandLineApplication.Options.__members__.items()]) + '\n'
        option_input = input(option_string)
        while option_input not in [str(member._value_) for name, member in CommandLineApplication.Options.__members__.items()]:
            option_input = input(option_string)
        option = CommandLineApplication.Options(int(option_input))
        return option
  
    def run(self):
        self.__greet_user()
        option = self.__select_option()
        if option == CommandLineApplication.Options.CREATE_A_QUIZ:
            builder = CLIDirectorOfCreation('question')
            question = builder.make_a_simple_question()


        
if __name__ == "__main__":
    command_line_application = CommandLineApplication("Welcome")
    command_line_application.run()
