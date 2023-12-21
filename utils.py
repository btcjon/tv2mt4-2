# utils.py
def parse_message(message):
    if isinstance(message, ImmutableMultiDict):
        data = message.to_dict()
    else:
        data = dict(x.split('=') for x in message.split(','))
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
