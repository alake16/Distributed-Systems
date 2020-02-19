class Metric:

    def __init__(self, quiz_name, question_list): # Or as single variable (dictionary)

        ''' Initialize quiz name to open all data given from active question '''
        self.quiz_name = quiz_name
        self.question_list = question_list # Temp ?


    def retrieve_metrics(self):
        '''
        This method will iteretate through the responses
        that were given from the quiz name. We will use this 
        in order to iterate & render our histogram
        '''
        all_questions = self.question_list[self.quiz_name]
        all_responses = all_questions.get_responses()

        metrics = self.calculate_metrics_from(all_responses)
        return metrics # String vesrion of percentage of selected question from each student


    def calculate_metrics_from(self, all_responses):
        ''' Count responses given in list and calcualte
        decision metrics based on the recieved responses '''
        return

    def append_evaluated_response(self, response):
        '''
        From here we will be able to append each response
        to our current histogram as it is being iterated
        '''
        student_metrics = self.caluclate_current_question_metric(resonse)
        return student_metrics


    def getAllQuestionsAndResponses(self):

        ''' Retrieve all data that was given in the dictionary by searching 
        quiz by name to retrieve data '''

        all_questions = self.question_list[self.quiz_name]
        responses = all_questions.get_responses()


        return all_questions, responses