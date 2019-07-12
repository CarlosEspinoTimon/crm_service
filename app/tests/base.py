#!/usr/bin/env python
# coding=utf-8

import pathmagic
import unittest
from unittest import mock
import json


import pathmagic

from server import create_app

import requests


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        '''
        Setup function
        '''
        self.app = create_app('config.Test')
        self.tester_app = self.app.test_client()
