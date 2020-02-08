multiple_choice_response_schema = {
    "type": "object",
    "properties": {
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "choice": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

matching_response_schema = {
    "type": "object",
    "properties": {
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "answer_mapping": {"type": "object"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

short_answer_response_schema = {
    "type": "object",
    "properties": {
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "short_answer": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}

fill_in_the_blank_response_schema = {
    "type": "object",
    "properties": {
        'kind': {"type": "string"},
        "type": {"type": "string"},
        "blank_answer": {"type": "string"},
        "user_id": {"type": "string"},
        "nickname": {"type": "string"}
    },
}
