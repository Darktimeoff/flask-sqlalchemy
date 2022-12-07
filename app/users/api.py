from flask import Blueprint, jsonify, request
from .dao.user_dao import UserDao
import logging

users_blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')
user_dao = UserDao()


@users_blueprint.route('/')
def get_users():
    users = user_dao.get_users()

    return jsonify(users)


@users_blueprint.route('/<int:id>/')
def get_user(id: int):
    user = user_dao.get_user(id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)

@users_blueprint.route('/', methods=['POST'])
def create_user():
    data = request.json
    print('data', type(data))
    try:
        user = user_dao.create_user(data)

        logging.info(f'succesfulle create_user {user}')
        
        return jsonify(user.serialized)
    except TypeError as e:
        logging.exception('create_user failed')
        return jsonify({'message': str(e)})
    except ValueError as e:
        logging.exception('create_user failed')
        return jsonify({'message': str(e)})