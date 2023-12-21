# utils.py
def parse_message(message):
    if 'type' not in message:
        raise ValueError("Missing 'type' in message data")
    data = message.to_dict()
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
