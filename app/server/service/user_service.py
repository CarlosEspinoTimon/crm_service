from datetime import datetime
from flask import jsonify

from server import db
from ..model.user import User


def all_users():
    return jsonify([user.__str__() for user in
                    User.query.filter_by(is_deleted=False)]), 200


def get_a_user(id):
    user = User.query.get(id)
    if user:
        response = jsonify(user.__str__()), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        admin_id = 1  # TODO use admin id
        user = User(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            created_at=datetime.now(),
            created_by=admin_id,
            modified_at=datetime.now(),
            modified_by=admin_id
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
        admin_id = 1
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.last_modified_by = admin_id
        user.last_modified_at = datetime.now()
        _save_user(user)
        response = jsonify('User sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete(id):
    user = User.query.get(id)
    if user:
        admin_id = 1
        user.last_modified_by = admin_id
        user.last_modified_at = datetime.now()
        user.is_deleted = True
        _save_user(user)
        response = jsonify('User deleted'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def modify_admin_status(data, user_id):
    user = User.query.get(user_id)
    if user:
        admin_id = 1
        user.admin = data.get('admin')
        user.admin_privileges_by = admin_id
        user.last_modified_by = admin_id
        user.last_modified_at = datetime.now()
        _save_user(user)
        response = jsonify('User sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def change_password(data, user_id):
    user = User.query.get(user_id)
    if user:
        admin_id = 1
        if not user.check_password(data.get('old_password')):
            return jsonify('Wrong password'), 401
        user.set_password(data.get('new_password'))
        user.last_modified_by = admin_id
        user.last_modified_at = datetime.now()
        _save_user(user)
        response = jsonify('Password sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def _save_user(user):
    db.session.add(user)
    db.session.commit()
