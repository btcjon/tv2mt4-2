from flask import Flask, request
from utils import parse_message
from airtable_operations import AirtableOperations
from dotenv import load_dotenv
import os
from business_rule_engine import RuleParser
import yaml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')

app = Flask(__name__)
airtable_operations = AirtableOperations()

@app.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    logging.info(f"Received {request.method} request to /webhook")
    # The 'GET' method is no longer supported, so the check is removed
    data = parse_message(request.form)
    if data['type'] == 'update':
        update_airtable(data['symbol'], data['keyword'])
    elif data['type'] == 'delete':
        delete_from_airtable(data['symbol'])
    # Add more elif blocks here for other message types
    return '', 200

def update_airtable(symbol, keyword):
    # Load and format rules from yaml file
    with open("rules.yaml", 'r') as stream:
        rules = yaml.safe_load(stream)

    # Parse the rule
    parser = RuleParser()
    rules_str = AirtableOperations.format_rules(rules['rules'])
    parser.parsestr(rules_str)

    # Update the Airtable field if the rule condition is met
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
    parser.register_function(update_resistance, 'update_resistance')
    parser.register_function(update_support, 'update_support')
    parser.register_function(update_td9buy, 'update_td9buy')
    parser.register_function(update_td9sell, 'update_td9sell')
    parser.register_function(update_trend, 'update_trend')

    # Execute the rules
    parser.execute({"type": "update", "keyword": keyword, "symbol": symbol})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
