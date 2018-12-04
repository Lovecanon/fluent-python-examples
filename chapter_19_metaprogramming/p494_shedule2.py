# -*- coding:utf-8 -*-
import json
import warnings
import inspect


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class MissingDatabaseError(RuntimeError):
    """需要数据库但没有指定数据库时抛出"""


class DBRecord(Record):
    __db = None

    @staticmethod
    def set_db(db):
        DBRecord.__db = db

    @staticmethod
    def get_db():
        return DBRecord.__db

    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = 'database not set; call "{}.set_db(my_db)"'
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()


class Event(DBRecord):
    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speak_objs'):
            spkr_serial = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self._speaker_objes = [fetch('speaker.{}'.format(key) for key in spkr_serial)]
        return self._speaker_objes

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


DB_NAME = 'data/schedule2_db'
CONFERENCE = 'conference.115'



def load_db(db):
    with open('data/osconfeed.json', 'r', encoding='utf-8') as f:
        raw_data = json.loads(f.read())
        warnings.warn('loading ' + DB_NAME)
        for collection, rec_list in raw_data['Schedule'].items():
            record_type = collection[:-1]
            cls_name = record_type.capitalize()
            cls = globals().get(cls_name, DBRecord)
            if inspect.isclass(cls) and issubclass(cls, DBRecord):
                factory = cls
            else:
                factory = DBRecord
            for record in rec_list:
                key = '{}.{}'.format(record_type, record['serial'])
                record['serial'] = key
                db[key] = factory(**record)

if __name__ == '__main__':
    import shelve

    db = shelve.open(DB_NAME)
    if CONFERENCE not in db:
        load_db(db)

    speaker = db['speaker.3471']
    type(speaker)
    print(speaker.name, speaker.twitter)

    db.close()