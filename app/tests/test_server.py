#!/usr/bin/env python
# coding=utf-8

import unittest
import json

import pathmagic

from base import BaseTestClass


class Server(BaseTestClass):
    'Test server'

    def test_server_running(self):
        '''
        Check if the server is running.
        '''
        res = self.tester_app.get('/')

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data, 'The server is running!!')


if __name__ == '__main__':
    unittest.main()
