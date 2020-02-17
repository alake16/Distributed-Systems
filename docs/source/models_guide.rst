======
Models
======

The app.Models package contains all of the data models for the application. These models
are top level and act to allow dependency inversion. In a dependency graph, these models
should be isolated from changes in lower-level client code. In all, these models include
the Quiz model, the Question Model, and the Response Model. Other primitives can be added here.
To avoid circular imports(and bad design) these models should not refer to client code. For example,
referring to ProjectJSONEncoder in this module would cause a circular import issue if ProjectJSONEncoder
also imported this module or client code imported that module. 


Questions
=========

The Questions Hierarchy has an abstract base class(subclasses ABC) of Question.
This class provides some default implementation for various methods such as returning 
the type of question. This method is used to ensure comptability with any dependent code.
Notably, this is used to ensure that added responses have the same type(multiple_choice == multiple_choice)

There is a static factory method called create_a_question that allows a user to

1. Clone a Question object by passing in a Question object (perhaps to create a defensive copy)
2. Create a question from a Python dict
3. Create a question from a JSON string.

Whatever representation ultimatley, a Question object with the proper type is created using 
keyword arguments. First, it is ensured that there is a type ultimately passed down to allow
dynamic creation of different types of questions. Client code should use this where different
types of questions can be created based on type.

There is also a static get_counts method that takes in a question_object and will
return a dictionary containing the unique responses given a users most recent arguments.

There is an abstract property json_data. This allows client code to get a python dictionary 
like this: question_object.json_data. This may be created using the copy.deepcopy method
to prevent inadvertent modification of the underlying data structure by client code. 
This may also become a mixin of the Question, Quiz, and Response base classes to simplify 
this code.

The add_response method is implemented in the base class to allow client code to easily add
responses without worrying about types. 

The get_responses method is currently a conveinence method that shows intention. This will
probably be made into a property using the property decorator. 

The __eq__ method is currently for testing purposes to ensure unit tests can pass.

There are currently implementations for Multiple Choice, Short Answer, Fill In The Blank,
and Matching Questions


Response
========

The Response class mirrors the Question hierarchy and it was decided to parallelize these hierarchies 
since Responses can have more data such as user_id, time_of_response, is_verified, and other metadata.

There is a static factory method that is slightly different from the Questions static factory method.
The factory method requires a question_id in addition to either JSON string, Response Object, or dict.
Responses should not exist without having an associated quiz. The validation logic will be expanded in 
a future release to ensure that all responses have associated questions.

There is a json_data property in all Response classes similar to the Questions object.

Quiz
====

The Quiz class is a concrete class that has multiple static methods to allow loading quizzes from storage.
This functionality will likely be extended to allow for the use of a database(relational or document).

Quizzes have a name, and a list of questions.

There are methods to allow getting a question based on question_id or based on question_number.
A future release may allow friendlier names to be used or a full text search based indexed.

There are static methods for writing quizzes and loading quizzes. These use functionality in the 
StorageHandler but this logic will likely be refactored into the StorageHandler to allow:

1. Use of either a database or a file store based on user configuration options
2. Separation of concerns. The Quiz object shouldn't need to be aware of how it's stored.
3. Persistence of Quizzes, Questions, and Responses in such a way they can be fetched independently.

 
