import collections
import json
import pickle





def read_json(filename):
    with open(filename) as json_data:
        d = json.load(json_data)
        return d


def write_json(data, filename):
    with open(filename, mode='w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=3, ensure_ascii=False)


def serialize(data, filename):
    with open(filename, mode='wb') as outfile:
        pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)


def deserialize(filename):
    with open(filename, mode='rb') as input:
        return pickle.load(input, encoding='utf-8')
