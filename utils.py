# utils.py
def parse_message(raw_data):
    data = {}
    pairs = raw_data.split(',')
    for pair in pairs:
        key, value = pair.split('=')
        data[key] = value
    return data

def parse_message(message):
    data = dict(item.split("=") for item in message.split(","))
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
    # Add more elif blocks here for other message types
    else:
        return data