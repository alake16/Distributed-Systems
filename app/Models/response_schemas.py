"""
This module is a work in progress and is subject to change.

The intention of the response_scehmas module is to ensure that JSON data received over the Network is appropriate.

Intended changes:
1) Consolidating shared data into a base response_schema.
2) Using the required syntax to ensure certain properties are always present.
3) Auto-generating these schemas using data from Question objects and how they're represented.

"""

multiple_choice_response_schema = {
    "type": "object",
    "properties": {
        "question_id": {"type": "string"},
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "answer": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

matching_response_schema = {
    "type": "object",
    "properties": {
        "question_id": {"type": "string"},
        'kind': {"type": "string"},
        "answer": {"type": "object"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

short_answer_response_schema = {
    "type": "object",
    "properties": {
        "question_id": {"type": "string"},
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "answer": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

fill_in_the_blank_response_schema = {
    "type": "object",
    "properties": {
        "question_id": {"type": "string"},
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "answer": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}
