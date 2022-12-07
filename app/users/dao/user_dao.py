from models.model import User, Role
from classes.dao import Dao
from classes.exception import NotFoundError

class UserDao(Dao):
    def set_query(self):
        self.__query = User.query

    def get_users(self) -> list[dict]:
        self.set_query()

        users = [user.serialized for user in self.__query.all()]

        return users

    @property
    def keys(self):
        return {'first_name', 'last_name', 'age', 'email', 'role', 'phone'}
        

    def get_user(self, id: int) -> dict | None:
        self.set_query()

        user = self.__query.get(id)

        if not user:
            return None

        return user.serialized


    def create_user(self, data: dict) -> dict | None:
        if type(data) is not dict:
            raise TypeError(f'Uncorrect type of data')
        
        data_keys =  set(data.keys())

        if data_keys != self.keys:
            raise ValueError(f'Uncorrect data for create, need to define {self.keys.difference(data_keys)}')

        user = User(
            first_name = data['first_name'],
            last_name = data['last_name'],
            age = data['age'],
            email = data['email'],
            role = Role.customer if data['role'] == Role.customer.name else Role.executor,
            phone = data['phone'],
        )

        self.add_to_db(user)

        return user
    
    def delete_user(self, id: int) -> True:
        if type(id) is not int:
            raise TypeError(f'Uncorrect type of id')
        
        self.set_query()

        user = self.__query.get(id)

        if not user:
            raise NotFoundError(f'User with this id: {id} doesn`t exist')

        self.delete_from_db(user)
        
        return True

