import json


def open(table):
    file_content = open(f"./{table}.json")
    return json.load(file_content)
