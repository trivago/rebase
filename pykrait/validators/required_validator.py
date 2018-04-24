from pykrait.core import Validator
from pykrait.validators import IntegerValidator


class RequiredValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'message':
            'This is a required property and should be set.',
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if value is None:
            self.errors.append(self.message)
            is_valid &= False

        return is_valid
