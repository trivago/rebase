from rebase.core import Validator


class BoolValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'message': '`{}` is not a boolean'
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if type(value) is not bool:
            self.errors.append(self.message.format(str(value)))
            is_valid &= False

        return is_valid
