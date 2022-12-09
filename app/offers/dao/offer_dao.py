from models.model import Offer, User, Order
from classes.dao import Dao
from classes.exception import NotFoundError,  ValidationDataError


class OfferDao(Dao):
    def set_query(self):
        self.__query = Offer.query

    def get_offers(self) -> list[dict]:
        self.set_query()

        offers = [offer.serialized for offer in self.__query.all()]

        return offers

    @property
    def create_offer_keys(self):
        return {"executor_id", 'order_id'}

    def get_offer(self, id: int) -> dict | None:
        self.set_query()

        offer = self.__query.get(id)

        if not offer:
            return None

        return offer.serialized

    def create_offer(self, data: dict) -> dict:
        if type(data) is not dict:
            raise TypeError(f'Uncorrect type of data')

        data_keys = set(data.keys())

        if data_keys != self.create_offer_keys:
            raise ValidationDataError(
                f'Uncorrect data for create, need to define {self.offer_create_keys.difference(data_keys)}')

        if User.query.get(data['executor_id']) is None:
            raise NotFoundError(
                f'Executor id:{data["executor_id"]} does not exist')

        if Order.query.get(data['order_id']) is None:
            raise NotFoundError(f'Order id:{data["order_id"]} does not exist')

        offer = Offer(
            executor_id=data['executor_id'], order_id=data['order_id'])

        self.add_to_db(data)

        return offer.serialized

    def update_order(self, id: int, data: dict) -> dict:
        if type(id) is not int:
            raise TypeError(f'Uncorrect type of id, must be integer')

        if type(data) is not dict:
            raise TypeError(f'Uncorrect type of data, must be dictionary')

        data_keys = set(data.keys())

        if data_keys != self.create_offer_keys:
            raise ValidationDataError(
                f'Uncorrect data for update, need to define {self.create_offer_key.difference(data_keys)}')

        if User.query.get(data['executor_id']) is None:
            raise NotFoundError(
                f'Executor id:{data["executor_id"]} does not exist')

        if Order.query.get(data['order_id']) is None:
            raise NotFoundError(f'Order id:{data["order_id"]} does not exist')

        self.set_query()

        offer = self.__query.get(id)

        for k, v in data.items():
            setattr(offer, k, v)

        self.update_data_in_db(offer)

        return offer.serialized

    def delete_offer(self, id: int) -> True:
        if type(id) is not int:
            raise TypeError('id must be an integer')

        self.set_query()

        offer = self.__query.get(id)

        if not offer:
            raise NotFoundError(f'Offer not found id: {id}')

        self.delete_from_db(offer)

        return True
