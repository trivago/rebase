import unittest
from unittest import mock
from rebase.core import Validator


@mock.patch.multiple(
    Validator,
    depends_on=mock.Mock(
        return_value={
            mock.Mock(
                validate=lambda x: True,
                errors=[]
            ),
            mock.Mock(
                validate=lambda x: False,
                errors=['Error 2']
            ),
        }
    )
)
class TestObject(unittest.TestCase):
    def test_validator_basic(self):
        v = Validator()

        self.assertFalse(v.validate('123'))
        self.assertIn('Error 2', v.errors)
