import json
import pickle
import collections
import pandas as pd

def rec_dd():
    return collections.defaultdict(rec_dd)


def read_zurich(xls_file):
    df = pd.read_excel(xls_file)
    # avoid NaN values with ''
    df = df.fillna('')
    j = (df.groupby(['belege::stelleMMSSSRR', 'belege::pada'])
         .apply(lambda x: x.to_dict('records')))
    d = rec_dd()
    for i, r in j.iteritems():
        verse_id = i[0].split('.')
        d[verse_id[0]][verse_id[1]][verse_id[2]][i[1]] = r
    return d


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
