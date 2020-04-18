import json
import pathlib
import os


def read(table):
    file_content = open(os.path.join(pathlib.Path(__file__).parent.absolute(), f"{table}.json"))
    return json.load(file_content)
