import json

json_str = '{"username": "worldxdana", "password": "123qwe123"}'
json_obj = json.loads(json_str)
print(json_obj["username"])