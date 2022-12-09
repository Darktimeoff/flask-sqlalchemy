from flask import Blueprint, jsonify, request
from .dao.offer_dao import OfferDao
from classes.exception import ValidationDataError, NotFoundError
import logging

offers_blueprint = Blueprint('offers', __name__, url_prefix='/api/v1/offers')
offer_dao = OfferDao()


@offers_blueprint.route('/')
def get_offers():
    try:
        offers = offer_dao.get_offers()
        logging.info(f'get_offers success')
        return jsonify(offers)
    except Exception as e:
        logging.exception(f'get_offers unknown error')

        return jsonify({"message": str(e), "status": -1})


@offers_blueprint.route('/<int:id>/')
def get_offer(id: int):
    try:
        offer = offer_dao.get_offer(id)

        if not offer:
            logging.error(f'get_offer error id: {id}')
            return jsonify({'message': 'Offer not found', "status": 1}), 404

        logging.info(f'get_offer id: {id} success')

        return jsonify(offer)
    except Exception as e:
        logging.exception(f'get_offer unknown error id: {id}')
        return jsonify({'message': str(e), "status": -1})


@offers_blueprint.route('/', methods=['POST'])
def create_offer():
    data = request.json()

    try:
        offer = offer_dao.create_offer(data)

        logging.info(f'create_offer success')

        return jsonify(offer)
    except TypeError as e:
        logging.exception(f'create offer error data: {data}')
        return jsonify({'message': str(e), "status": 1})
    except ValidationDataError as e:
        logging.exception(f'validation data error: {data}')
        return jsonify({'message': str(e), "status": 2})
    except NotFoundError as e:
        logging.exception(f'offer not found error data: {data}')
        return jsonify({'message': str(e), "status": 3})
    except Exception as e:
        logging.exception(f'offer create unknown error data: {data}')
        return jsonify({'message': str(e), "status": -1})


@offers_blueprint.route('/<int:id>/', methods=['PUT'])
def update_offer(id: int):
    data = request.json()

    try:
        offer = offer_dao.update_offer(id, offer)

        logging.info(f'update_offer success')

        return jsonify(offer)
    except TypeError as e:
        logging.exception(f'update offer error id: {id}, data error: {data}')
        return jsonify({'message': str(e), "status": 1})
    except ValidationDataError as e:
        logging.exception(f'update offer error id: {id}, data: {data}')
        return jsonify({'message': str(e), "status": 2})
    except NotFoundError as e:
        logging.exception(f'update offer error id: {id}, data: {data}')
        return jsonify({'message': str(e), "status": 3})
    except Exception as e:
        logging.exception(f'update offer unknown error id: {id}, data: {data}')
        return jsonify({'message': str(e), "status": -1})


@offers_blueprint.route('/<int: id>/', methods=['DELETE'])
def delete_offer(id: int):
    try:
        offer_dao.delete_offer(id)

        logging.info(f'delete_offer success id: {id}')

        return jsonify({"message": "success"})
    except TypeError as e:
        logging.exception(f'delete offer error id: {id}')
        return jsonify({'message': str(e), "status": 1})
    except NotFoundError as e:
        logging.exception(f'delete offer error id: {id}')
        return jsonify({'message': str(e), "status": 2})
    except Exception as e:
        logging.exception(f'delete offer error id: {id}')
        return jsonify({'message': str(e), "status": 3})
