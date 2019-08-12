from flask import Blueprint, jsonify, request
from flask_cors import CORS

from ..util.decorator import check_user_token
from ..service.customer_service import (
    all_customers,
    get_a_customer,
    create_customer,
    update_customer,
    delete
)

customers = Blueprint('customers', __name__, url_prefix='/customers')
CORS(customers, max_age=30 * 86400)


@customers.route('/', methods=['GET'])
@check_user_token
def get_all_customers():
    """
    .. http:get:: /customers/

    Function that returns all the customers.

    This endpoint is protected and only users can use it by passing their
    authentication token through the Authorization Header.

    :returns: The Customers.
    :rtype: list.
    :reqheader Authorization: Bearer token
    """
    return all_customers()


@customers.route('/<int:customer_id>', methods=['GET'])
@check_user_token
def get_customer(customer_id):
    """
    .. http:get:: /customers/(int:customer_id)

    Function that given an id it returns the customer.

    This endpoint is protected and only users can use it by passing their
    authentication token through the Authorization Header.

    :param customer_id: the id of the customer.
    :type customer_id: int

    :returns: The customer
    :rtype: Customer
    :reqheader Authorization: Bearer token

    """
    return get_a_customer(customer_id)


@customers.route('', methods=['POST'])
@check_user_token
def post_customer():
    """
    .. http:post:: /customers

    Function that given the customer data it creates it.

    This endpoint is protected and only users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'email': 'email@example.com',
            'name': 'name',
            'surname': 'surname',
            'photo': {
                'str_image': 'aXk39jacml',
                'extension': 'jpg'
            }
        }

    :param body: the data of the customer sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token

    """
    data = request.get_json()
    return create_customer(data)


@customers.route('/<int:customer_id>', methods=['PUT'])
@check_user_token
def put_customer(customer_id):
    """
    .. http:put:: /customers/(int:customer_id)

    Function that given the customer_id it updates it with the data sent in the
    body of the request.

    This endpoint is protected and only users can use it by passing their
    authentication token through the Authorization Header.

    Example::

        body = {
            'name': 'name',
            'surname': 'surname',
            'photo': {
                'str_image': 'aXk39jacml',
                'extension': 'jpg'
            }
        }

    :param customer_id: the id of the customer.
    :type customer_id: int
    :param body: the data of the customer sent in the body of the request.
    :type body: dict
    :reqheader Authorization: Bearer token
    """
    data = request.get_json()
    return update_customer(data, customer_id)


@customers.route('/<int:customer_id>', methods=['DELETE'])
@check_user_token
def delete_customer(customer_id, id_obtained_from_token):
    """
    .. http:delete:: /customers/(int:customer_id)

    Function that given the customer id it deletes it.

    This endpoint is protected and only users can use it by passing their
    authentication token through the Authorization Header.

    :param customer_id: the id of the customer.
    :type customer_id: int
    :reqheader Authorization: Bearer token
    """
    return delete(customer_id, id_obtained_from_token)
