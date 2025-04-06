import json
def dict_to_json(data, filename = "data.json"):
    with open(filename, "w") as file:
      json.dump(data, file, indent=4)

data = {"name": "Alice", "age" : 25, "city": "New York"}
dict_to_json(data)
