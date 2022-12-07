from typing import TypeVar, Generic
from database import db
import logging

T = TypeVar('T')

class Dao(Generic[T]):
    __query: T | None
    __db = db

    @property
    def db(self):
        return db
    
    @property
    def db_session(self):
        return db.session

    @property
    def query(self):
        return self.__query

    def add_to_db(self, data):
        db.session.begin()

        try:
            db.session.add(data)
        except Exception as e:
            db.session.rollback()
            logging.exception(f'Rollback transaction {data}')
            raise
        else:
            db.session.commit()
    
    def clear_query(self):
        self.__query = None