"""This file is part of the trivago/rebase library.

# Copyright (c) 2018 trivago N.V.
# License: Apache 2.0
# Source: https://github.com/trivago/rebase
# Version: 1.2.0
# Python Version: 3.6
# Author: Yuv Joodhisty <yuvrajsingh.joodhisty@trivago.com>
"""

import unittest
from unittest import mock
from rebase.core import Model
from rebase.validators import RangeValidator


@mock.patch.multiple(
    Model,
    scenarios=mock.Mock(
        return_value={
            'personal': ['name', 'age', 'gender']
        }
    ),
    rules=mock.Mock(
        return_value={
            'age': [RangeValidator(min=20, max=30)]
        }
    ),
    properties=mock.Mock(
        return_value={
            'name': 'name',
            'age': 'age',
            'gender': ('gender', lambda x: int(x == 'Male')),
            'location': ('location', lambda x: x.upper()),
        }
    )
)
class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = Model(
            context='personal',
            name='Paul',
            age=35,
            gender="Male",
            location="Germany")

    def test_model_scenario(self):
        self.assertIn('name', self.model.attributes)
        self.assertIn('age', self.model.attributes)
        self.assertIn('gender', self.model.attributes)
        self.assertNotIn('location', self.model.attributes)

    def test_model_rules(self):
        self.assertFalse(self.model.validate())
        self.model.age = 25
        self.assertTrue(self.model.validate())
        self.model.age = '25'
        self.assertFalse(self.model.validate())
        self.assertEqual(len(self.model.get_errors()), 1)

    def test_model_context(self):
        self.model.set_context(None)
        self.assertIn('location', self.model.attributes)

        self.model.set_context('undefined_scenario')
        self.assertEqual(self.model.attributes, self.model.get(
            'name', 'age', 'gender', 'location'))

        self.model.set_context('personal')
        self.assertNotEqual(self.model.attributes, self.model.get(
            'name', 'age', 'gender', 'location'))
