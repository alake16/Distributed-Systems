from bs4 import BeautifulSoup
from time import sleep
html = open("xml_test.xml", 'r')
exam = BeautifulSoup(html, 'xml')

all_questions_on_exam = exam.find_all('Question')
all_answers_on_exam = exam.find_all('Answer')
for question_num, (each_question, each_answer) in enumerate(zip(all_questions_on_exam, all_answers_on_exam)):
    question_as_text = each_question.text
    answer_as_text = each_answer.text
    print("Question# {}\n{}\nANSWER: {}".format(question_num, question_as_text, answer_as_text))
    print("----------------")
    sleep(1)



