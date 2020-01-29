from __future__ import print_function
import lxml
import Serializer
from lxml import etree


# TODO: The validator needs work.
def isProperlyFormattedXML():
    parser = etree.XMLParser(dtd_validation=True)
    schema_root = etree.XML('''\
        <Exam>
            <Question type="Short Response">
                What does OOP stand for?
            </Question>
            <Answer type="Short Response">
                "Object Oriented programming"
            </Answer>
        </Exam>
        ''')
    schema = etree.XMLSchema(schema_root)

    # Good xml
    parser = etree.XMLParser(schema=schema)
    try:
        root = etree.fromstring("<a>5</a>", parser)
        print("Finished validating good xml")

        return True
    except lxml.etree.XMLSyntaxError as err:
        print(err)

    # Bad xml
    parser = etree.XMLParser(schema=schema)
    try:
        root = etree.fromstring("<a>5<b>foobar</b></a>", parser)
    except lxml.etree.XMLSyntaxError as err:
        print(err)
        return False


def consumeNewQuestions():
    # Two lists for holding questions and their corresponding answers
    questions = []
    answers = []

    # Wait for input indefinitely
    while (True):
        newQuestion = input("enter a new question!: ")

        if (newQuestion == '#Done'):
            print('Termination signal received.')
            break

        newAnswer = input("enter the answer: ")
        print('new question is: ' + newQuestion)
        print('new answer is: ' + newAnswer)

        # store the question and answer
        questions.append(newQuestion)
        answers.append(newAnswer)

    Serializer.generateSerializedOutputFile(questions, answers)