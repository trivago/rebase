from pykrait.core import Model, Validator


class NestedValidator(Validator):
    def properties(self):
        return {
            **super().properties(),
            'required': True,
        }

    def validate(self, value):
        if not super().validate(value):
            return False

        is_valid = True

        if isinstance(value, Model) and not value.validate():
            is_valid = False
            self.errors.append(value.get_errors())
        elif isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, Model) and not v.validate():
                    is_valid = False
                    self.errors.append({k: v.get_errors()})
        elif isinstance(value, list) or isinstance(value, set):
            for v in value:
                if isinstance(v, Model) and not v.validate():
                    is_valid = False
                    self.errors.append({v.get_id(): v.get_errors()})

        return is_valid
