from flask import Blueprint, jsonify
from .dao.offer_dao import OfferDao

offers_blueprint = Blueprint('offers', __name__, url_prefix='/api/v1/offers')
offer_dao = OfferDao()


@offers_blueprint.route('/')
def get_offers():
    users = offer_dao.get_offers()

    return jsonify(users)


@offers_blueprint.route('/<int:id>/')
def get_offer(id: int):
    user = offer_dao.get_offer(id)

    if not user:
        return jsonify({'message': 'Offer not found'}), 404

    return jsonify(user)
