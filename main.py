from flask import Flask, request
from utils import parse_message
from airtable_operations import AirtableOperations
from dotenv import load_dotenv
import os
from business_rule_engine import RuleParser
import yaml
import logging
from werkzeug.datastructures import ImmutableMultiDict

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
    if request.method == 'POST':
        data = parse_message(request.form)
        if data['type'] == 'update':
            update_airtable(data['symbol'], data['keyword'])
        elif data['type'] == 'delete':
            delete_from_airtable(data['symbol'])
        # Add more elif blocks here for other message types
    elif request.method == 'GET':
        data = parse_message(request.args)
        return "Webhook endpoint", 200
    return '', 200

def update_airtable(symbol, keyword):
    # Load and format rules from yaml file
    with open("rules.yaml", 'r') as stream:
        rules = yaml.safe_load(stream)
    logging.info(f"Loaded rules: {rules}")

    # Parse the rule
    parser = RuleParser()
    rules_str = AirtableOperations.format_rules(rules['rules'])
    logging.info(f"Formatted rules: {rules_str}")
    parser.parsestr(rules_str)

    # Update the Airtable field if the rule condition is met
    # Define the action functions
    def update_resistance(value):
        logging.info(f"Called update_resistance with value: {value}")
        airtable_operations.update_by_field('Symbol', symbol, {'Resistance': value})

    def update_support(value):
        logging.info(f"Called update_support with value: {value}")
        airtable_operations.update_by_field('Symbol', symbol, {'Support': value})

    def update_td9buy(value):
        logging.info(f"Called update_td9buy with value: {value}")
        airtable_operations.update_by_field('Symbol', symbol, {'TD9buy': value})

    def update_td9sell(value):
        logging.info(f"Called update_td9sell with value: {value}")
        airtable_operations.update_by_field('Symbol', symbol, {'TD9sell': value})

    def update_trend(value):
        logging.info(f"Called update_trend with value: {value}")
        airtable_operations.update_by_field('Symbol', symbol, {'Trend': value})

    # Register the action functions
    parser.register_function(update_resistance, 'update_resistance')
    parser.register_function(update_support, 'update_support')
    parser.register_function(update_td9buy, 'update_td9buy')
    parser.register_function(update_td9sell, 'update_td9sell')
    parser.register_function(update_trend, 'update_trend')

    # Execute the rules
    logging.info(f"Executing rules with data: {{'type': 'update', 'keyword': {keyword}, 'symbol': {symbol}}}")
    parser.execute({"type": "update", "keyword": keyword, "symbol": symbol})

def parse_message(message):
    if isinstance(message, ImmutableMultiDict):
        data = message.to_dict()
    else:
        data = dict(item.split("=") for item in message.split(","))
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
