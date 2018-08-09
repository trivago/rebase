"""This file is part of the trivago/rebase library.

# Copyright (c) 2018 trivago N.V.
# License: Apache 2.0
# Source: https://github.com/trivago/rebase
# Version: 1.2.2
# Python Version: 3.6
# Author: Yuv Joodhisty <yuvrajsingh.joodhisty@trivago.com>
"""

from rebase.core import Object


class Validator(Object):
    def __init__(self, **attributes):
        super().__init__(**attributes)

    def properties(self):
        return {
            'errors': [],
            'required': False,
            'message': lambda: f'{{value}} failed to comply with {self.classname} rules.'
        }

    def validate(self, value):
        is_valid = True
        self.errors.clear()

        for validator in self.depends_on():
            is_valid &= validator.validate(value)
            self.errors += validator.errors

        return is_valid

    def depends_on(self):
        return {}
