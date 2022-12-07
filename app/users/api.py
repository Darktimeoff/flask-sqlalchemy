from flask import Blueprint, jsonify
from .dao.user_dao import UserDao

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
