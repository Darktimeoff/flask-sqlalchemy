from models.model import User
from classes.dao import Dao

class UserDao(Dao):
    def __init__(self) -> None:
        self.__query = User.query

    def get_users(self) -> list[dict]:
        if not self.__query:
            raise TypeError('Query is not initilize')

        users = [user.serialized for user in self.__query.all() if user]

        return users

    def get_user(self, id: int) -> dict | None:
        if not self.__query:
            raise TypeError('Query is not initilize')
        
        user = User.query.get(id)

        if not user:
            return None

        return user.serialized