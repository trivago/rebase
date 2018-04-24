from pykrait.core import Object


class Validator(Object):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.errors = []

    def properties(self):
        return {'errors': 'errors'}

    def validate(self, value):
        is_valid = True

        for validator in self.depends_on():
            is_valid &= validator.validate(value)
            self.errors += validator.errors

        return is_valid

    def depends_on(self):
        return {}
