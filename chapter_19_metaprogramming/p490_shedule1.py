# -*- coding:utf-8 -*-
import json
import warnings

"""

"""

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'


def load():
    with open('data/osconfeed.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # <2>


def load_db(db):
    raw_data = load()  # <3>
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():  # <4>
        record_type = collection[:-1]  # <5>
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])  # <6>
            record['serial'] = key  # <7>
            db[key] = Record(**record)  # <8>


if __name__ == '__main__':
    import shelve

    db = shelve.open(DB_NAME)
    if CONFERENCE not in db:
        load_db(db)

    speaker = db['speaker.3471']
    type(speaker)
    print(speaker.name, speaker.twitter)

    db.close()
