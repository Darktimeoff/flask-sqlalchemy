from models.model import Offer
from classes.dao import Dao


class OfferDao(Dao):
    def set_query(self):
        self.__query = Offer.query

    def get_offers(self) -> list[dict]:
        self.set_query()

        offers = [offer.serialized for offer in self.__query.all()]

        return offers

    def get_offer(self, id: int) -> dict | None:
        self.set_query()

        offer = self.__query.get(id)

        if not offer:
            return None

        return offer.serialized
