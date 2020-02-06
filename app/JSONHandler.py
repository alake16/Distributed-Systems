import json

# With great thanks to https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json

class ProjectJSONEncoder(json.JSONEncoder):
    """
    Used by json.dumps
    """
    def default(self, object):
        if hasattr(object, 'json_data'):
            return object.json_data
        else:
            return json.JSONEncoder.default(self, object)
