import json

with open('./variables.json', 'r') as f:
    data = json.load(f)

print(data)