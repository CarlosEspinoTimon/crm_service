#!/usr/bin/env python
# coding=utf-8

import unittest
import json

import pathmagic

from base import BaseTestClass
from server.model.user import User


class TestUser(BaseTestClass):
    'Test User'

    user = {
        'email': 'user@email2.com',
        'name': 'user2',
        'surname': 'surname2',
        'admin': False,
        'admin_privileges_by': None,
        'created_by': 1,
        'modified_by': 1,
        'created_at': '2019-05-24 11:29:43.432020',
        'modified_at': '2019-05-24 11:29:43.432020',
        'password_hash': '1234',
        'is_deleted': False,
    }

    def test_create_a_user(self):
        data = {
            'email': 'user@email.com',
            'name': 'user',
            'surname': 'surname',
            'password': '1234'
        }
        res = self.tester_app.post(
            '/users',
            data=json.dumps(data),
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.admin_token
            })
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data(as_text=True))
        expected_user = dict(eval('''{'id': 1,
                                    'email': 'user@email.com',
                                    'name': 'user',
                                    'surname': 'surname',
                                    'admin': False,
                                    'admin_privileges_by': None,
                                    'created_by': 1,
                                    'modified_by': 1,
                                    'is_deleted': False}'''))
        user = dict(data)
        user.pop('modified_at')
        user.pop('created_at')
        self.assertDictEqual(user, expected_user)

    def test_get_a_user(self):
        self.create_user()
        res = self.tester_app.get(
            '/users/1',
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.admin_token
            })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        expected_user = dict(eval('''{'id': 1,
                                    'email': 'user@email.com',
                                    'name': 'user',
                                    'surname': 'surname',
                                    'admin': True,
                                    'admin_privileges_by': 1,
                                    'created_by': 1,
                                    'modified_by': 1,
                                    'is_deleted': False}'''))
        user = dict(data)
        user.pop('modified_at')
        user.pop('created_at')
        self.assertDictEqual(user, expected_user)

    def test_get_all_users(self):
        self.create_user()
        self.create_user(self.user)
        res = self.tester_app.get('/users/', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
        })
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_edit_a_user(self):
        self.create_user()
        data = {
            'name': 'user2',
            'surname': 'surname2',
        }
        res = self.tester_app.put('/users/1',
                                  data=json.dumps(data),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': self.admin_token
                                  })
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        user = User.query.get(1)
        self.assertEqual(user.name, 'user2')
        self.assertEqual(user.surname, 'surname2')

    def test_delete_a_user(self):
        self.create_user()
        res = self.tester_app.delete('/users/1',
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': self.admin_token
                                     })
        self.assertEqual(res.status_code, 200)
        user = User.query.get(1)
        self.assertEqual(user.is_deleted, True)

    def test_modify_admin_status(self):
        self.create_user()
        user = User.query.get(1)
        self.assertEqual(user.admin, True)
        data = {
            'admin': 0
        }
        res = self.tester_app.put('/users/1/change-admin-status',
                                  data=json.dumps(data),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': self.admin_token
                                  })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(user.admin, False)

    def test_change_password(self):
        self.create_user()
        user = User.query.get(1)
        self.assertTrue(user.check_password('1234'))
        data = {
            'old_password': '1234',
            'new_password': '12345',
        }
        res = self.tester_app.put('/users/1/change-password',
                                  data=json.dumps(data),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': self.admin_token
                                  })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(user.check_password('12345'))
        res = self.tester_app.put('/users/1/change-password',
                                  data=json.dumps(data),
                                  headers={
                                      'Content-Type': 'application/json',
                                      'Authorization': self.admin_token
                                  })
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
