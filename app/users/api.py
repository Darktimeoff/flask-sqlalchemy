from flask import Blueprint, jsonify
from models.model import User

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

@users_blueprint.route('/')
def get_users():
    users = [user.serialized for user in User.query.all() if user]

    return jsonify(users)