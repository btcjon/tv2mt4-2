import unittest
from unittest.mock import patch, MagicMock
import logging
import sys
import os
import yaml
from app import update_airtable
from business_rule_engine import RuleParser

# Set up logging
logging.basicConfig(level=logging.INFO)

def update_airtable(symbol, keyword):
    # Load rules from yaml file
    with open("rules.yaml", 'r') as stream:
        rules = yaml.safe_load(stream)

    # Parse the rule
    parser = RuleParser()
    rules_str = format_rules(rules['rules'])
    parser.parsestr(rules_str)

    # Update the Airtable field if the rule condition is met
    if parser.execute({"keyword": keyword}):
        airtable_operations.update_by_field('Symbol', symbol, {'Trend': keyword})
        logging.info(f"Updated Airtable: Set '{symbol}' to '{keyword}'")

def format_rules(rules):
    formatted_rules = []
    for rule in rules:
        name = rule.get('name', '')
        condition = rule.get('condition', '')
        action = rule.get('action', '')
        formatted_rules.append(f"name '{name}' condition '{condition}' action '{action}'")
    return "\n".join(formatted_rules)
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
