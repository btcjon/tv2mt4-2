# airtable_operations.py
from business_rule_engine import RuleParser
import yaml
from airtable import Airtable
from dotenv import load_dotenv
import os

load_dotenv()

AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')

class AirtableOperations:
    def __init__(self):
        self.airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)

    def update_by_field(self, field_name, field_value, new_data):
        self.airtable.update_by_field(field_name, field_value, new_data)

def format_rules(rules):
    formatted_rules = []
    for rule in rules:
        name = rule.get('name', '')
        condition = rule.get('condition', '')
        action = rule.get('action', '')
        formatted_rules.append(f"name '{name}' condition '{condition}' action '{action}'")
    return "\n".join(formatted_rules)

airtable_operations = AirtableOperations()

def update_airtable(symbol, keyword):
    # Load rules from yaml file
    with open("rules.yaml", 'r') as stream:
        rules = yaml.safe_load(stream)

    # Parse the rule
    parser = RuleParser()
    rules_str = format_rules(rules['rules'])
    parser.parsestr(rules_str)

    # Define the action functions
    def update_resistance(value):
        airtable_operations.update_by_field('Symbol', symbol, {'Resistance': value})

    def update_support(value):
        airtable_operations.update_by_field('Symbol', symbol, {'Support': value})

    def update_td9buy(value):
        airtable_operations.update_by_field('Symbol', symbol, {'TD9buy': value})

    def update_td9sell(value):
        airtable_operations.update_by_field('Symbol', symbol, {'TD9sell': value})

    def update_trend(value):
        airtable_operations.update_by_field('Symbol', symbol, {'Trend': value})

    # Register the action functions
    parser.register_function(update_resistance)
    parser.register_function(update_support)
    parser.register_function(update_td9buy)
    parser.register_function(update_td9sell)
    parser.register_function(update_trend)

    # Execute the rules
    parser.execute({"type": "update", "keyword": keyword})
