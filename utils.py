# utils.py
import logging

def parse_message(message):
    data = dict(item.split("=") for item in message.split(","))
    logging.info(f"Message: {message}, Parsed data: {data}")  # Log the message and parsed data
    return data
