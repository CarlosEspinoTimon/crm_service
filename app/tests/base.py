#!/usr/bin/env python
# coding=utf-8

import unittest

import pathmagic

from server import create_app, db
from server.model.customer import Customer


class BaseTestClass(unittest.TestCase):

    customer = {
        'email': 'customer@email.com',
        'name': 'customer',
        'surname': 'surname',
        'photo_url': 'photo_url',
        'created_by': '1',
        'last_modified_by': '1',
        'created_at': '2019-05-24 11:29:43.432020',
        'last_modified_at': '2019-05-24 11:29:43.432020',
        'is_deleted': False,
    }

    def setUp(self):
        self.app = create_app('config.Test')
        self.tester_app = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()
        self._ctx.pop()

    def create_customer(self, data=customer):
        '''
        Function that presists a Customer in the database for the test
        '''
        customer = Customer(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            photo_url=data['photo_url'],
            created_by=data['created_by'],
            last_modified_by=data['last_modified_by'],
            created_at=data['created_at'],
            last_modified_at=data['last_modified_at'],
            is_deleted=data['is_deleted'],
        )
        db.session.add(customer)
        db.session.flush()
