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
from rebase.core import Object


class TestObject(unittest.TestCase):
    def setUp(self):
        self.obj = Object(
            name='Paul',
            age='35',
            gender="Male",
            location=dict(
                city='Paris',
                country='France'
            ),
            is_admin=False,
            user='user',
            status='inactive',
            mother={'name': 'Lucie', 'age':46}
        )


    def test_object_basic(self):
        self.assertIn('name', self.obj.attributes)
        self.assertIn('age', self.obj.attributes)
        self.assertIn('gender', self.obj.attributes)

        self.assertEqual(self.obj.name, 'Paul')
        self.assertEqual(self.obj.age, '35')
        self.assertEqual(self.obj.gender, 'Male')

        self.assertDictEqual(self.obj.attributes, self.obj.get(
            'name', 'age', 'gender', 'location', 'is_admin', 'user', 'status', 'mother'))

    @mock.patch.multiple(
        Object,
        properties=mock.Mock(
            return_value={
                'firstname': 'name',
                'age': ('age', int),
                'gender': ('gender', lambda x: int(x == 'Male')),
                'city': 'location.city',
                'country': ('location.country', lambda x: x.upper()),
                'occupation': ('occupation', lambda x: x),
                'user': ('user', lambda x: x),
                'admin': 'not admin',
                'status': lambda: 'active',
                'date_joined': (lambda: 'today', str),
                'mother': ('mother', Object)
            }
        )
    )
    def test_object_init(self):
        self.setUp()

        self.assertEqual(self.obj.firstname, 'Paul')
        self.assertEqual(self.obj.age, 35)
        self.assertEqual(self.obj.gender, 1)
        self.assertEqual(self.obj.city, 'Paris')
        self.assertEqual(self.obj.country, 'FRANCE')
        self.assertEqual(self.obj.occupation, None)
        self.assertEqual(self.obj.user, 'user')
        self.assertEqual(self.obj.admin, None)
        self.assertEqual(self.obj.status, 'active')
        self.assertEqual(self.obj.date_joined, 'today')
        self.assertTrue(isinstance(self.obj.mother, Object))

        self.assertRaises(AttributeError, getattr, self.obj, 'qwerty')
        self.assertRaises(AttributeError, setattr, self.obj, 'qwerty', 'asd')
        self.assertIsNone(setattr(self.obj, 'age', 25))
        self.assertIs(getattr(self.obj, 'age'), 25)
        self.assertRaises(AttributeError, setattr, self.obj, 'age', '25')
