from flask import Blueprint, jsonify
from models.model import User
from .dao.user_dao import UserDao

users_blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_blueprint.route('/')
def get_users():
    user_dao = UserDao()
    users = user_dao.get_users()

    return jsonify(users)

@users_blueprint.route('/<int:id>/')
def get_user(id: int):
    user_dao = UserDao()
    user = user_dao.get_user(id)

    if not user:
        return 'User not Found', 404

    return jsonify(user)