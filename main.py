import gevent.monkey
gevent.monkey.patch_all()
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit, send
from bs4 import BeautifulSoup
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('frontend.html')

@socketio.on('message')
def handle_message(message):
    print("Recieved message: "+ message)

class Parser:
    def __init__(self, document_name=None, file_type='xml'):
        """
        :param document_name --> XML file name
        :param type --> Type of file we are trying to parse
        :return: None
        """
        self.document_name = document_name
        self.type = file_type

    def OpenXMLDoc(self):
        try:
            file = open(self.document_name, 'r') # Open & Read file before feeding to bs4
            document = BeautifulSoup(file, self.type)
            return document
        except FileNotFoundError: # Debugger
            print("...Can not find file. "
                  "Make sure the file you are trying to open is "
                  "within the correct directory")
            return


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # To start, we will create a class that will handle all of our parsing tools
    # # We should continue to add upon this class for our own convenience and flexibility
    # parser = Parser(document_name='xml_test.xml', file_type='xml')
    # exam = parser.OpenXMLDoc()  # Feeding our file into bs4 for XML parsing
    # all_questions_on_exam = exam.find_all('Question') # Finding all tags in our xml doc named 'Question & Answer'
    # all_answers_on_exam = exam.find_all('Answer') # Returned: XML style output

    # # Our outputed tags are stored within a list by default, meaning, we're able to call each tag by their respected index
    # for question_num, (each_question, each_answer) in enumerate(zip(all_questions_on_exam, all_answers_on_exam)):
    #     question_as_text = each_question.text # From XML format --> string
    #     answer_as_text = each_answer.text
    #     # This is our current output. Now that we have an output and control of our document,
    #     # we will be able to apply more flexibility with our current class
    #     print("Question# {}\n{}\nANSWER: {}".format(question_num, question_as_text, answer_as_text))
    #     print("----------------")
    #     sleep(1)
