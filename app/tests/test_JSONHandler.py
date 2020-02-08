import unittest
from unittest.mock import Mock
import json
from app.JSONHandler import ProjectJSONEncoder


class TestProjectJSONEncoder(unittest.TestCase):
    def test_json_encoder_encodes_json_data_attribute(self):
        """
        Tests that the project JSON encoder properly deals with objects that have json_data attributes
        :return:
        """
        object_with_json_data_attribute = Mock()
        object_with_json_data_attribute.json_data = {'A': '1', 'B': ['A', 'C']}
        json_string = json.dumps(object_with_json_data_attribute, cls=ProjectJSONEncoder)
        self.assertEqual(str({"A": "1", "B": ["A", "C"]}).replace('\'', '\"'), json_string)
        second_object_with_json_data_attribute = Mock()
        second_object_with_json_data_attribute.json_data = {'mike': 2}
        object_with_json_data_attribute.json_data = {'A': '1', 'B': ['A', 'C'],
                                                     'items': [second_object_with_json_data_attribute]}
        json_string = json.dumps(object_with_json_data_attribute, cls=ProjectJSONEncoder)
        self.assertEqual(str({"A": "1", "B": ["A", "C"], "items": [{"mike": 2}]}).replace('\'', '\"'), json_string)

    def test_json_encoder_does_not_encode_arbitrary_objects(self):
        """
        Tests to ensure that the encoder doesn't encode arbitrary objects.
        :return:
        """
        object_without_json_data_attribute = Mock()
        object_with_json_data_attribute = Mock()
        # Since Mock creates attributes on demand, this is the way to ensure hasattr calls are False
        del object_without_json_data_attribute.json_data
        object_with_json_data_attribute.json_data = {'A': '1', 'B': ['A', 'C']}
        object_without_json_data_attribute.dog = object_with_json_data_attribute
        with self.assertRaises(TypeError):
            json_string = json.dumps(object_without_json_data_attribute, cls=ProjectJSONEncoder)


if __name__ == '__main__':
    unittest.main()
