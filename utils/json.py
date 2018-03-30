import os
import json

def load_json(file):
    """Loads a JSON file and returns it as a dict"""
    with open(file) as f:
        return json.load(f)


def dump_json(file, array):
    """Dumps a dict to a JSON file"""
    with open(file, 'w') as f:
        return json.dump(array, f)