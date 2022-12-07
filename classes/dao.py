from typing import TypeVar, Generic
T = TypeVar('T')

class Dao(Generic[T]):
    __query: T | None

    def get_query(self):
        return self.__query
    
    def clear_query(self):
        self.__query = None