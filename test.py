import json


with open('config.json') as jsonFile:
    data = json.load(jsonFile)
print(data['prefix'])
data['prefix'] = '!'

with open("config.json", "w") as jsonFile:
    json.dump(data, jsonFile)

with open('config.json') as jsonFile:
    data = json.load(jsonFile)

print(data['prefix'])