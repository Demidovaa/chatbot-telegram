import json


with open('search_result.json', 'r') as f:
    data = f.read()
    serial_info = json.loads(data)
