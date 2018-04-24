from typing import Dict, List

import simplejson as json
from pykrait.core import Object, Validator


class Model(Object):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self._errors = {}

    def __str__(self) -> str:
        return json.dumps({**self.attributes, **{'_errors': self._errors}})

    def _properties(self) -> List[str]:
        return [*super()._properties(), '_errors']

    def rules(self) -> Dict[str, List[Validator]]:
        return {}

    def validate(self) -> bool:
        is_valid = True

        for attr, ruleset in self.rules().items():
            for rule in ruleset:
                value = getattr(self, attr, None)
                if rule.required or value is not None:
                    is_valid &= rule.validate(value)
                    self.add_errors(attr, rule.errors)

        return is_valid

    def add_errors(self, attribute, messages):
        attribute_errors = self._errors.get(attribute, [])
        self._errors[attribute] = attribute_errors + messages

    def get_errors(self, attribute=None) -> Dict[str, List[str]]:
        return self._errors.get(attribute) if attribute else self._errors
