import json


# The intention of this method of storage handling is to keep things dead simple in the beginning
# before committing to a particular method of storage.
# MongoDB and document databases are added complexity. But designing a schema too early might constrain
# us. If we go ahead and make this dead simple functionality. We can build out later.

# This is prototype code.

def write_to_file(json_string_object, file_path):
    with open(file_path, 'w') as outfile:
        outfile.write(json_string_object)


def load_file_as_json(file_path):
    with open(file_path, 'r') as infile:
        json = infile.read()
    return json

# Questions File -> Storage bank for questions/answer json objects(Just append questions here if they don't exist)
# Quiz Directory -> Quiz References Questions File -> A quiz is essentially a concrete object representing something
# users will respond to. Responses should go here and go into the question of interest. To get at a particular
# question we need some sort of unique identifier. Should these be locally unique or globally unique(in terms of the
# live program for a particular context)

# If the questions are locally unique and not globally unique. We can't easily reuse them(like a question bank) in
# other quizzes. If they are globally unique, We can easily reuse them, but then we have to Check if a question with
# a particular id has already been created. The real issue is if we can really be certain if a question is truly
# unique.

# How will we distribute this? -> Ideally, distribution will entail each context receiving it's own local storage
# engine(file or db)
