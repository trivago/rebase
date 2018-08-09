"""This file is part of the trivago/rebase library.

# Copyright (c) 2018 trivago N.V.
# License: Apache 2.0
# Source: https://github.com/trivago/rebase
# Version: 1.2.2
# Python Version: 3.6
# Author: Yuv Joodhisty <yuvrajsingh.joodhisty@trivago.com>
"""

from rebase.core import Validator
from rebase.validators import IntegerValidator


class RangeValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'min': None,
            'max': None,
            'message': lambda: '{value} is not within the range {min} and {max}'
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if not (int(value) >= self.min and int(value) <= self.max):
            self.errors.append(
                self.message.format(
                    value=str(value),
                    min=str(self.min),
                    max=str(self.max)
                )
            )
            is_valid &= False

        return is_valid

    def depends_on(self):
        return {IntegerValidator(required=self.required)}
