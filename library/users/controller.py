from flask import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import LoginManager
from functools import wraps
from library.model import Users

from .services import (delete_User_data_by_id_service, get_all_users_service, get_all_users_status_service,
                       get_user_by_id_service, update_user_by_id_service, login, logout, register, verify_otp, update_user_by_username_service,)

users = Blueprint("users", __name__)


def is_admin(user_id):
    user = Users.query.get(user_id)
    return 'admin' in [role.name for role in user.roles]

def admin_required(fn):
    @wraps(fn)  # Sử dụng wraps ở đây
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        if not is_admin(user_id):
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

# Áp dụng admin_required cho route
@users.route('/user/status')
@admin_required
def get_users_status():
    return get_all_users_status_service()



@users.route("/user/verify_otp", methods=['POST'])
def verify_otp_user():
    return verify_otp()

@users.route("/user/login", methods=['POST'])
def login_user():
    return login()


@users.route("/user/<string:username>/logout", methods=['POST'])
def logout_user(username):
    return logout(username)


@users.route("/user/register", methods=["POST"])
def add_user():
    return register()


@users.route("/user/all", methods=["GET"])
def get_all_users():
    return get_all_users_service()


@users.route("/user/<int:id>", methods=["GET"])
def get_user_by_email(id):
    return get_user_by_id_service(id)


@users.route("/user/<int:id>", methods=["PUT"])
def update_user_by_id(id):
    return update_user_by_id_service(id)


@users.route("/user/<string:username>", methods=["PUT"])
def update_user_by_username(username):
    return update_user_by_username_service(username)

@users.route("/user/<int:id>", methods=["DELETE"])
def delete_user_by_id(id):
    return delete_User_data_by_id_service(id)

