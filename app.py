from flask import Flask, request
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

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    raw_data = request.data.decode('utf-8')
    data = parse_message(raw_data)
    if data['type'] == 'update':
        update_airtable(data['symbol'], data['keyword'])
    elif data['type'] == 'delete':
        delete_from_airtable(data['symbol'])
    # Add more elif blocks here for other message types
    return '', 200

def update_airtable(symbol, keyword):
    # Load rules from yaml file
    with open("rules.yaml", 'r') as stream:
        rules = yaml.safe_load(stream)

    # Parse the rule
    parser = RuleParser()
    parser.parsestr(rules)

    # Update the Airtable field if the rule condition is met
    if parser.execute({"keyword": keyword}):
        airtable_operations.update_by_field('Symbol', symbol, {'Trend': keyword})
        logging.info(f"Updated Airtable: Set '{symbol}' to '{keyword}'")

if __name__ == '__main__':
    app.run(port=5000)