from flask import Blueprint, jsonify, request
from flask_cors import CORS

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
def get_all_customers():
    """
    Function that returns all the customers.

    :returns: The Customers.
    :rtype: list.
    """
    return all_customers()


@customers.route('/<int:id>', methods=['GET'])
def get_customer(id):
    """
    Function that given an id it returns the customer.

    :param id: the id of the customer.
    :type id: int

    :returns: The customer
    :rtype: Customer

    """
    return get_a_customer(id)


@customers.route('', methods=['POST'])
def post_customer():
    """
    Function that given the customer data it creates it.

    Example::

        data = {
            'email': 'email@example.com',
            'name': 'name',
            'surname': 'surname',
        }

    :param data: the data of the customer sent in the body of the request.
    :type data: dict

    """
    data = request.get_json()
    return create_customer(data)


@customers.route('/<int:customer_id>', methods=['PUT'])
def put_customer(customer_id):
    """
    Function that given the customer_id it updates it with the data sent in the
    body of the request.

    Example::

        data = {
            'name': 'name',
            'surname': 'surname',
        }

    :param customer_id: the id of the customer.
    :type customer_id: int
    :param data: the data of the customer sent in the body of the request.
    :type data: dict
    """
    data = request.get_json()
    return update_customer(data, customer_id)


@customers.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    Function that given the customer id it deletes it.

    :param id: the id of the customer.
    :type id: int
    """
    return delete(id)
