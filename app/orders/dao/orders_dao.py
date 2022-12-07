from models.model import Order
from classes.dao import Dao


class OrderDao(Dao):
    def set_query(self):
        self.__query = Order.query

    def get_orders(self) -> list[dict]:
        self.set_query()

        orders = [order.serialized for order in self.__query.all()]

        return orders

    def get_order(self, id: int) -> dict | None:
        self.set_query()

        order = self.__query.get(id)

        if not order:
            return None

        return order.serialized
