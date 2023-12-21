# utils.py
def parse_message(message):
    data = dict(item.split("=") for item in message.split(","))
    # Ensure all required keys are present
    required_keys = {'type', 'symbol', 'keyword'}
    if not required_keys.issubset(data):
        missing_keys = required_keys - set(data.keys())
        raise ValueError(f"Missing required keys in message data: {missing_keys}")
    if data['type'] == 'update':
        return {
            'type': 'update',
            'symbol': data.get('symbol'),
            'keyword': data.get('keyword')
        }
    elif data['type'] == 'delete':
        return {
            'type': 'delete',
            'symbol': data.get('symbol')
        }
