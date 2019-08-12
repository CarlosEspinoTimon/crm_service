from datetime import datetime
from flask import jsonify

from server import db
from ..model.user import User


def all_users():
    return jsonify([user.__str__() for user in
                    User.query.filter_by(is_deleted=False)]), 200


def get_a_user(user_id):
    user = User.query.get(user_id)
    if user and user.is_deleted is False:
        response = jsonify(user.__str__()), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_user(data):
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        user = User(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            created_at=datetime.now(),
            created_by=data.get('id'),
            modified_at=datetime.now(),
            modified_by=data.get('id')
        )
        user.set_password(data.get('password'))
        _save_user(user)
        response = jsonify(user.__str__()), 201
    else:
        response = jsonify('User already exists'), 409
    return response


def update_user(data, user_id):
    user = User.query.get(user_id)
    if user:
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.modified_by = data.get('id')
        user.modified_at = datetime.now()
        _save_user(user)
        response = jsonify('User sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete(user_id, admin_id):
    user = User.query.get(user_id)
    if user:
        user.modified_by = admin_id
        user.modified_at = datetime.now()
        user.is_deleted = True
        _save_user(user)
        response = jsonify('User deleted'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def modify_admin_status(data, user_id):
    user = User.query.get(user_id)
    if user:
        privileges = data.get('admin')
        if privileges not in [0, 1]:
            return jsonify('Unprocessable Entity, wrong input'), 422
        user.admin = privileges
        user.admin_privileges_by = data.get('id')
        user.modified_by = data.get('id')
        user.modified_at = datetime.now()
        _save_user(user)
        response = jsonify('User sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def change_password(data, user_id):
    user = User.query.get(user_id)
    if user:
        if not user.check_password(data.get('old_password')):
            return jsonify('Wrong password'), 401
        user.set_password(data.get('new_password'))
        user.modified_by = data.get('id')
        user.modified_at = datetime.now()
        _save_user(user)
        response = jsonify('Password sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def _save_user(user):
    db.session.add(user)
    db.session.commit()
