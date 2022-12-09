from models.model import Order, User
from classes.dao import Dao
from classes.exception import NotFoundError,  ValidationDataError
from utils.main import str_date_to_python


class OrderDao(Dao):
    def set_query(self):
        self.__query = Order.query

    def get_orders(self) -> list[dict]:
        self.set_query()

        orders = [order.serialized for order in self.__query.all()]

        return orders

    @property
    def order_create_keys(self):
        return {
            'name',
            'description',
            'start_date',
            'end_date',
            'address',
            'price',
            'customer_id',
            'executor_id',
        }

    def get_order(self, id: int) -> dict | None:
        self.set_query()

        order = self.__query.get(id)

        if not order:
            return None

        return order.serialized

    def create_order(self, data: dict) -> dict:
        if type(data) is not dict:
            raise TypeError(f'Uncorrect type of data must be dict')

        data_keys = set(data.keys())

        if data_keys != self.order_create_keys:
            raise ValidationDataError(
                f'Uncorrect data for create, need to define {self.order_create_keys.difference(data_keys)}')

        if User.query.get(data['customer_id']) is None or User.query.get(data['executor_id']) is None:
            raise NotFoundError(f'User {data["customer_id"]}-{data["executor_id"]} not found')

        self.set_query()

        order = Order(
            customer_id=data['customer_id'],
            executor_id=data['executor_id'],
            name=data['name'],
            description=data['description'],
            start_date=str_date_to_python(data['start_date']),
            end_date=str_date_to_python(data['end_date']),
            address=data['address'],
            price=data['price'],
        )

        self.add_to_db(order)

        return order.serialized

    def update_order(self, id: int, data: dict) -> dict:
        if type(id) is not int:
            raise TypeError("id type must be int")

        if type(data) is not dict:
            raise TypeError(f'Uncorrect type of data must be dict')

        data_keys = set(data.keys())

        if data_keys != self.order_create_keys:
            raise ValidationDataError(
                f'Uncorrect data for create, need to define {self.order_create_keys.difference(data_keys)}')

        if User.query.get(data['customer_id']) is None or User.query.get(data['executor_id']) is None:
            raise NotFoundError(f'User {data["customer_id"]}-{data["executor_id"]} not found')

        self.set_query()

        order = self.__query.get(id)

        if not order:
            raise NotFoundError(f'Order with id {id} not found')

        for key, value in order.items():
            setattr(order, key, value)

        self.update_data_in_db(order)

        return order.serialized

    def delete_order(self, id: int) -> True:
        if type(id) is not int:
            raise TypeError(f'Uncorrect type of id must be int')

        self.set_query()

        order = self.__query.get(id)

        if not order:
            raise NotFoundError(f'Order with id unexist')

        self.delete_from_db(order)

        return True
