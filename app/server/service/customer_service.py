from datetime import datetime
from flask import jsonify

from server import db
from ..model.customer import Customer


def all_customers():
    return jsonify([customer.__str__() for customer in
                    Customer.query.filter_by(is_deleted=False)]), 200


def get_a_customer(id):
    customer = Customer.query.get(id)
    if customer:
        response = jsonify(customer.__str__()), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_customer(data):
    customer = Customer.query.filter_by(email=data['email']).first()
    if not customer:
        customer = Customer(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            photo_url="http://photo-url.com",
            created_by=data.get('id'),
            last_modified_by=data.get('id'),
            created_at=datetime.now(),
            last_modified_at=datetime.now()
        )
        _save_customer(customer)
        response = jsonify(customer.__str__()), 201
    else:
        response = jsonify('User already exists'), 409
    return response


def update_customer(data, customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        data['photo_url'] = "http://photo-url.com"
        if data.get('name'):
            customer.name = data['name']
        if data.get('surname'):
            customer.surname = data['surname']
        if data.get('photo_url'):
            customer.photo_url = data['photo_url']
        customer.last_modified_by = data.get('id')
        customer.last_modified_at = datetime.now()
        _save_customer(customer)
        response = jsonify('Customer sucessfully updated'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def delete(customer_id, user_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.last_modified_by = user_id
        customer.last_modified_at = datetime.now()
        customer.is_deleted = True
        _save_customer(customer)
        response = jsonify('Customer deleted'), 200
    else:
        response = jsonify('User not found'), 404
    return response


def _save_customer(customer):
    db.session.add(customer)
    db.session.commit()
