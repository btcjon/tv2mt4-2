import unittest
import logging
from unittest.mock import patch
from app import app, update_airtable
from business_rule_engine import RuleParser

# Set up logging
logging.basicConfig(level=logging.INFO)

class TestUpdateAirtable(unittest.TestCase):
    @patch('app.airtable_operations')
    @patch('business_rule_engine.RuleParser')
    @patch('app.yaml')
    def test_update_airtable(self, mock_yaml, mock_parser, mock_airtable_operations):
        # Mock the yaml.safe_load function to return a specific set of rules
        mock_yaml.safe_load.return_value = {
            'rules': [
                {
                    'name': 'Test Rule',
                    'condition': 'keyword == "test"',
                    'action': 'update_airtable("Test", True)'
                }
            ]
        }
        # Mock the RuleParser.execute function to return True
        mock_parser_instance = mock_parser.return_value
        mock_parser_instance.execute.return_value = True

        # Call the function with test data
        update_airtable('Test', 'test')

        # Verify that the update_by_field function was called with the correct arguments
        mock_airtable_operations.update_by_field.assert_called_once_with('Symbol', 'Test', {'Trend': 'test'})
if __name__ == '__main__':
    unittest.main()
