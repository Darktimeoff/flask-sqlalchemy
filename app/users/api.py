from flask import Blueprint, jsonify, request
from .dao.user_dao import UserDao
import logging
from classes.exception import NotFoundError

users_blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')
user_dao = UserDao()


@users_blueprint.route('/')
def get_users():
    try:
        users = user_dao.get_users()

        return jsonify(users)
    except Exception as e:
        logging.exception(f'get users unknown error')
        return jsonify({'message': str(e), "status": -1}), 500


@users_blueprint.route('/<int:id>/')
def get_user(id: int):
    try:
        user = user_dao.get_user(id)

        if not user:
            logging.error(f'User with id {id} not found')
            return jsonify({'message': 'User not found', "status": 1}), 404

        logging.info(f'User with id {id} found')

        return jsonify(user)
    except Exception as e:
        logging.exception('get_user unknown error')
        return jsonify({'message': str(e), "status": -1}), 500


@users_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.json
    print('data', type(data))
    try:
        user = user_dao.create_user(data)

        logging.info(f'succesfully create_user {user}')

        return jsonify(user.serialized)
    except TypeError as e:
        logging.exception('create_user failed')
        return jsonify({'message': str(e), "status": 1}), 400
    except ValueError as e:
        logging.exception('create_user failed')
        return jsonify({'message': str(e), "status": 2}), 400
    except Exception as e:
        logging.exception(f'create_user unknown')
        return jsonify({'message': str(e), "status": -1}), 500


@users_blueprint.route('/<int:id>/', methods=['DELETE'])
def delete_user(id: int):
    try:
        user_dao.delete_user(id)
        logging.info(f'succesfully delete_user id:{id}')

        return jsonify({'message': 'success'})
    except TypeError as e:
        logging.exception(f'delete user failed id:{id}')

        return jsonify({'message': str(e), "status": 1}), 400
    except NotFoundError as e:
        logging.exception(f'delete user failed not found id: {id}')

        return jsonify({'message': str(e), "status": 2}), 404
    except Exception as e:
        logging.exception('delete user unknown error id: {id}')
        return jsonify({'message': str(e), "status": -1}), 500


@users_blueprint.route('/<int:id>/', methods=['PUT'])
def update_user(id: int):
    try:
        data = request.json

        user = user_dao.update_user(id, data)
        logging.info(f'succesfully update user id:{id} user: {user}')

        return jsonify(user)
    except ValueError as e:
        logging.exception(f'update user failed id:{id}')

        return jsonify({'message': str(e), "status": 1}), 400
    except TypeError as e:
        logging.exception(f'update user failed id:{id}')

        return jsonify({'message': str(e), "status": 2}), 400
    except NotFoundError as e:
        logging.exception(f'delete user failed not found id: {id}')

        return jsonify({'message': str(e), "status": 3}), 404
    except Exception as e:
        logging.exception(f'delete user uknown error')
        return jsonify({'message': str(e), "status": -1}), 500
