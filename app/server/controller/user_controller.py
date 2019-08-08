from flask import Blueprint, abort, jsonify, request
from flask_cors import CORS

from ..util.decorator import check_admin_token
from ..service.user_service import (
    all_users,
    get_a_user,
    create_user,
    update_user,
    modify_admin_status,
    change_password,
    delete
)

users = Blueprint('users', __name__, url_prefix='/users')
CORS(users, max_age=30 * 86400)


@users.route('/', methods=['GET'])
@check_admin_token
def get_all_users():
    """
    .. http:get:: /users/

    Function that returns all the users.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    :returns: The users.
    :rtype: list.
    :reqheader Authorization: Bearer token
    """
    return all_users()


@users.route('/<int:user_id>', methods=['GET'])
@check_admin_token
def get_user(user_id):
    """
    .. http:get:: /users/(int:user_id)

    Function that given an id it returns the user.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    :param user_id: the id of the user.
    :type user_id: int

    :returns: The user
    :rtype: User
    :reqheader Authorization: Bearer token

    """
    return get_a_user(user_id)


@users.route('', methods=['POST'])
@check_admin_token
def post_user():
    """
    .. http:post:: /users

    Function that given the user data it creates it.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'email': 'email@example.com',
            'name': 'name',
            'surname': 'surname',
            'password': '1234'
        }

    :param body: the data of the user sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token

    """
    data = request.get_json()
    return create_user(data)


@users.route('/<int:user_id>', methods=['PUT'])
@check_admin_token
def put_user(user_id):
    """
    .. http:put:: /users/(int:user_id)

    Function that given the user_id it updates it with the data sent in the
    body of the request.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'name': 'name',
            'surname': 'surname',
        }

    :param user_id: the id of the user.
    :type user_id: int
    :param body: the data of the user sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token
    """
    data = request.get_json()
    return update_user(data, user_id)


@users.route('/<int:user_id>/change-admin-status', methods=['PUT'])
@check_admin_token
def change_admin_status(user_id):
    """
    .. http:put:: /users/(int:user_id)/change-admin-status

    Function that given the user_id it updates its admin privileges with the
    information sent in the body of the request. To grant admin privileges you
    must send a 1 and to revoke the privileges, a 0.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'admin': 1
        }

    :param user_id: the id of the user.
    :type user_id: int
    :param body: the data of the user sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token
    """
    data = request.get_json()
    return modify_admin_status(data, user_id)


@users.route('/<int:user_id>/change-password', methods=['PUT'])
@check_admin_token
def change_user_password(user_id):
    """
    .. http:put:: /users/(int:user_id)/change-password


    Function that given the user_id it updates its password with the
    information sent in the body of the request.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'old_password': 'old_pass',
            'new_password': 'new_pass',
        }

    :param user_id: the id of the user.
    :type user_id: int
    :param body: the data of the user sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token
    """
    data = request.get_json()
    return change_password(data, user_id)


@users.route('/<int:user_id>', methods=['DELETE'])
@check_admin_token
def delete_user(user_id):
    """
    .. http:delete:: /users/(int:user_id)

    Function that given the user id it deletes it.

    This endpoint is protected and only admin users can use it by passing their
    authentication token through the Authorization Header.

    :param user_id: the id of the user.
    :type user_id: int
    :reqheader Authorization: Bearer token
    """
    return delete(user_id)
