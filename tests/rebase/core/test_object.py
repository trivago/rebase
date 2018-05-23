import unittest
from unittest import mock
from rebase.core import Object

class TestObject(unittest.TestCase):
    def test_object_basic(self):
        obj = Object(name='Paul', age=35, gender="Male")

        self.assertIn('name', obj.attributes)
        self.assertIn('age', obj.attributes)
        self.assertIn('gender', obj.attributes)

        self.assertEqual(obj.name, 'Paul')
        self.assertEqual(obj.age, 35)
        self.assertEqual(obj.gender, 'Male')

        self.assertDictEqual(obj.attributes, obj.get('name', 'age', 'gender'))

        print(obj)
