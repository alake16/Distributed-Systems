class Metric:

    def __init__(self, quiz_name, question_list): # Or as single variable (dictionary)
        self.quiz_name = quiz_name
        self.question_list = question_list



    def retrieve_metrics(self):
        '''
        This method will iteretate through the responses
        that were given from the quiz name. We will use this 
        in order to iterate & render our histogram
        '''
        all_questions = self.question_list[self.quiz_name]
        all_responses = all_questions.get_responses()

        for each_response in all_responses:
            self.append_evaluated_response(each_response)


        return 



    def append_evaluated_response(self, response):
        '''
        From here we will be able to append each response
        to our current histogram as it is being iterated
        '''
        return

    def getAllQuestionsAndResponses(self):

        all_questions = self.question_list[self.quiz_name]
        responses = all_questions.get_responses()


        return all_questions, responses