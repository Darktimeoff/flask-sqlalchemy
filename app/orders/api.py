from flask import Blueprint, jsonify
from .dao.orders_dao import OrderDao

orders_blueprint = Blueprint('orders', __name__, url_prefix='/api/v1/orders')
order_dao = OrderDao()


@orders_blueprint.route('/')
def get_orders():
    orders = order_dao.get_orders()

    return jsonify(orders)


@orders_blueprint.route('/<int:id>/')
def get_order(id: int):
    order = order_dao.get_order(id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    return jsonify(order)
