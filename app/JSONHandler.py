import json


# With great thanks to https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json

class ProjectJSONEncoder(json.JSONEncoder):
    """
    Used by json.dumps
    """

    def default(self, obj):
        if hasattr(obj, 'json_data'):
            return obj.json_data
        else:
            return json.JSONEncoder.default(self, obj)
