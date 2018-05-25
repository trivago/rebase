from rebase.core import Validator


class IntegerValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'message': '`{value}` is not an integer'
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if type(value) is not int:
            self.errors.append(self.message.format(value=value))
            is_valid &= False

        return is_valid
