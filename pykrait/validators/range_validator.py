from pykrait.core import Validator
from pykrait.validators import IntegerValidator


class RangeValidator(Validator):
    def properties(self):
        return {
            **super().properties(), 'min': 'min',
            'max': 'max',
            'message': '{} is not within the range {} and {}'
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if not (int(value) >= self.min and int(value) <= self.max):
            self.errors.append(
                self.message.format(str(value), str(self.min), str(self.max)))
            is_valid &= False

        return is_valid

    def depends_on(self):
        return {IntegerValidator()}
