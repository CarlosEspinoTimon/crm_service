#!/usr/bin/env python
# coding=utf-8

import unittest
import json
from datetime import datetime

import pathmagic

from base import BaseTestClass
from server.model.customer import Customer


class TestCustomer(BaseTestClass):
    'Test User'

    def test_create_a_customer(self):
        self.create_user()
        data = {
            'email': 'customer@email.com',
            'name': 'customer',
            'surname': 'surname',
        }
        res = self.tester_app.post(
            '/customers',
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.user_token
            })
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        expected_customer = dict(eval('''{'id': 1,
                                    'email': 'customer@email.com',
                                    'name': 'customer',
                                    'surname': 'surname',
                                    'photo_url': None,
                                    'created_by': 1,
                                    'last_modified_by': 1,
                                    'is_deleted': False}'''))
        customer = dict(data)
        customer.pop('last_modified_at')
        customer.pop('created_at')
        self.assertDictEqual(customer, expected_customer)

    def test_get_a_customer(self):
        self.create_user()
        self.create_customer()
        res = self.tester_app.get(
            '/customers/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.user_token
            })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        expected_customer = dict(eval('''{'id': 1,
                                    'email': 'customer@email.com',
                                    'name': 'customer',
                                    'surname': 'surname',
                                    'photo_url': 'http://photo-url.com',
                                    'created_by': 1,
                                    'last_modified_by': 1  ,
                                    'is_deleted': False}'''))
        customer = dict(data)
        customer.pop('last_modified_at')
        customer.pop('created_at')
        self.assertDictEqual(customer, expected_customer)

    def test_get_all_customers(self):
        self.create_user()
        self.create_customer()
        customer = {
            'email': 'customer@email2.com',
            'name': 'customer2',
            'surname': 'surname2',
            'photo_url': 'photo_url2',
            'created_by': 1,
            'last_modified_by': 1,
            'created_at': datetime.now(),
            'last_modified_at': datetime.now(),
            'is_deleted': False,
        }
        self.create_customer(customer)
        res = self.tester_app.get('/customers/',
                                  headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': self.user_token
                                  })
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_edit_a_customer(self):
        self.create_user()
        self.create_customer()
        data = {
            'name': 'customer2',
            'surname': 'surname2',
        }
        res = self.tester_app.put('/customers/1',
                                  data=json.dumps(data),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': self.user_token
                                   })
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        customer = Customer.query.get(1)
        self.assertEqual(customer.name, 'customer2')
        self.assertEqual(customer.surname, 'surname2')

    def test_delete_a_customer(self):
        self.create_user()
        self.create_customer()
        res = self.tester_app.delete('/customers/1',
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': self.user_token
                                            })
        self.assertEqual(res.status_code, 200)
        customer = Customer.query.get(1)
        self.assertEqual(customer.is_deleted, True)


if __name__ == '__main__':
    unittest.main()
