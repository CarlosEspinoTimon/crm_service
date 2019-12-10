from datetime import datetime
from flask import jsonify

from server import db
from ..model.customer import (
    Customer,
    CustomerSchema,
    UpdateCustomerSchema,
    CreateCustomerSchema
)
from ..util.image_upload import upload_image
from ..util.check_schema import check_schema


def all_customers():
    customer_schema = CustomerSchema(many=True)
    customers = Customer.query.filter_by(is_deleted=False)
    response = customer_schema.dump(customers)
    return jsonify(response), 200


def get_a_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer and customer.is_deleted is False:
        customer_schema = CustomerSchema()
        response = customer_schema.dump(customer), 200
    else:
        response = jsonify('User not found'), 404
    return response


def create_customer(data):
    check_schema(data, CreateCustomerSchema())
    customer = Customer.query.filter_by(email=data['email']).first()
    if not customer:
        photo_url = get_photo_url(data)
        customer = Customer(
            email=data.get('email'),
            name=data.get('name'),
            surname=data.get('surname'),
            photo_url=photo_url,
            created_by=data.get('id'),
            last_modified_by=data.get('id'),
            created_at=datetime.now(),
            last_modified_at=datetime.now()
        )
        _save_customer(customer)
        customer_schema = CustomerSchema()
        response = customer_schema.dump(customer), 201
    else:
        response = jsonify('User already exists'), 409
    return response


def update_customer(data, customer_id):
    check_schema(data, UpdateCustomerSchema())
    customer = Customer.query.get(customer_id)
    if customer:
        photo_url = get_photo_url(data)
        if data.get('name'):
            customer.name = data['name']
        if data.get('surname'):
            customer.surname = data['surname']
        if photo_url:
            customer.photo_url = photo_url
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


def get_photo_url(data):
    photo_url = None
    if data.get('photo'):
        image = data['photo'].get('str_image')
        extension = data['photo'].get('extension')
        content_type = 'image/{}'.format(extension[1:])
        photo_url = upload_image(image, content_type, extension)
    return photo_url


def _save_customer(customer):
    db.session.add(customer)
    db.session.commit()
