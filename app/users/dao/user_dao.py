from models.model import User
from classes.dao import Dao


class UserDao(Dao):
    def set_query(self):
        self.__query = User.query

    def get_users(self) -> list[dict]:
        self.set_query()

        users = [user.serialized for user in self.__query.all()]

        return users

    def get_user(self, id: int) -> dict | None:
        self.set_query()

        user = self.__query.get(id)

        if not user:
            return None

        return user.serialized
