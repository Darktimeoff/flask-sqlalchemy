from flask import Blueprint, jsonify, request
from .dao.orders_dao import OrderDao
from classes.exception import NotFoundError, ValidationDataError
import logging

orders_blueprint = Blueprint('orders', __name__, url_prefix='/api/v1/orders')
order_dao = OrderDao()


@orders_blueprint.route('/')
def get_orders():
    try:
        orders = order_dao.get_orders()
        logging.info(f'get orders success')
        return jsonify(orders)
    except Exception as e:
        logging.exception(f'get orders unknown error')

        return jsonify({'message': str(e), "status": -1}), 500


@orders_blueprint.route('/<int:id>/')
def get_order(id: int):
    try:
        order = order_dao.get_order(id)

        if not order:
            logging.info(f'get order error id: {id}')
            return jsonify({'message': 'Order not found', "status": 1}), 404

        logging.info(f'get_order order id: {id} success')

        return jsonify(order)
    except Exception as e:
        logging.exception(f'get order unknown error')
        return jsonify({'message': str(e), "status": -1}), 500


@orders_blueprint.route('/', methods=['POST'])
def create_order():
    data = request.json

    try:
        order = order_dao.create_order(data)

        logging.info(f'create_order success')

        return jsonify(order)
    except TypeError as e:
        logging.exception(f'create order error {data}')
        return jsonify({'message': str(e), "status": 1}), 400
    except ValidationDataError as e:
        logging.exception(f'create order error {data}')
        return jsonify({'message': str(e), "status": 2}), 400
    except NotFoundError as e:
        logging.exception(f'create order error {data}')
        return jsonify({'message': str(e), "status": 3}), 400
    except Exception as e:
        logging.exception(f'creater order error unknown')
        return jsonify({'message': str(e), "status": -1}), 500


@orders_blueprint.route('/<int:id>/', methods=['PUT'])
def update_order(id):
    data = request.json

    try:
        order = order_dao.update_order(id, data)

        logging.info(f'update_order success')

        return jsonify(order)
    except TypeError as e:
        logging.exception(f'update order error id:{id}, body: {data}')
        return jsonify({'message': str(e), "status": 1}), 400
    except ValidationDataError as e:
        logging.exception(f'update order error id: {id}, body: {data}')
        return jsonify({'message': str(e), "status": 2}), 400
    except NotFoundError as e:
        logging.exception(f'update order error id:{id}, body: {data}')
        return jsonify({'message': str(e), "status": 3}), 400
    except Exception as e:
        return jsonify({'message': str(e), "status": -1}), 500


@orders_blueprint.route('/<int:id>/', methods=['DELETE'])
def delete_order(id: int):
    try:
        order_dao.delete_order(id)

        logging.info(f'delete_order success')

        return jsonify({'message': 'success'})
    except TypeError as e:
        logging.exception(f'delete order error id: {id}')

        return jsonify({'message': str(e), "status": 1}), 400
    except NotFoundError as e:
        logging.exception(f'delete order error id:{id}')

        return jsonify({'message': str(e), "status": 2}), 400
    except Exception as e:
        logging.exception(f'delete order unknown error id: {id}')

        return jsonify({'message': str(e), "status": -1}), 500
