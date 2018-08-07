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
class TestValidator(unittest.TestCase):
    def test_validator_basic(self):
        v = Validator()

        self.assertFalse(v.validate('123'))
        self.assertIn('Error 2', v.errors)
