"""This file is part of the trivago/rebase library.

# Copyright (c) 2018 trivago N.V.
# License: Apache 2.0
# Source: https://github.com/trivago/rebase
# Version: 1.2.2
# Python Version: 3.6
# Author: Yuv Joodhisty <yuvrajsingh.joodhisty@trivago.com>
"""

from typing import Any, Dict, List
from rebase.core import Object, Validator


class Model(Object):
    def __init__(self, context=None, **attributes):
        self._errors = {}
        self._context = context
        super().__init__(**attributes)

    def _debug(self) -> Dict[str, Any]:
        return {
            **super()._debug(),
            **{
                '_errors': self._errors,
                '_context': self._context
            }
        }

    def _properties(self) -> List[str]:
        return [*super()._properties(), '_errors', '_context']

    @property
    def attributes(self) -> Dict[str, Any]:
        context_attributes = self.scenarios().get(self._context)
        return super().attributes if not context_attributes else {
            k: v
            for k, v in super().attributes.items()
            if context_attributes and k in context_attributes
        }

    def rules(self) -> Dict[str, List[Validator]]:
        return {}

    def scenarios(self) -> Dict[str, List[str]]:
        return {}

    def validate(self, attribute = None) -> bool:
        is_valid = True
        if not attribute:
            self._errors.clear()
        else:
            self._errors.update({attribute: []})

        for attr, ruleset in self.rules().items():
            if attribute and attr != attribute:
                continue
            for rule in ruleset:
                value = getattr(self, attr, None)
                if rule.required and value is None:
                    self.add_errors(attr, [f'`{attr}` is a required field.'])
                    is_valid = False
                    continue
                is_valid &= rule.validate(value)
                self.add_errors(attr, rule.errors)

        return is_valid

    def add_errors(self, attribute, messages):
        attribute_errors = self._errors.get(attribute, [])
        self._errors[attribute] = attribute_errors + messages

    def get_errors(self, attribute=None) -> Dict[str, List[str]]:
        return self._errors.get(attribute) if attribute else self._errors

    def get_context(self):
        return self._context

    def set_context(self, value):
        self._context = value
