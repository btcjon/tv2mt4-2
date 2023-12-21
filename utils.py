# utils.py
def parse_message(message):
    if isinstance(message, ImmutableMultiDict) and message:
        data = message.to_dict()
    else:
        data = dict(x.split('=') for x in message.split(','))
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
