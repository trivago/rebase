import uuid
from typing import Any, Dict, List

import simplejson as json


class Object(object):
    def __init__(self, **kwargs):
        """Initialize the object with the given attributes.
        If this method is overridden in the child, the parent implementation
        should be called in order to properly assign attributes.

        By default attributes are assigned dynamically to the object. But to get
        more control in child classes (such as remapping), it is recommended to
        override the `Object.properties()` method.

        Args:
            **kwargs: Arbitrary keyword argument which by default becomes an
            attribute of the object unless specified otherwise in
            `Object.properties()`.
            ```python
              print [i*2 for i in range(1,10)]
              ```
        """

        self._raw_attributes = kwargs
        self._attributes = {}
        self._init_attributes()


    def __getattr__(self, attr_name: str) -> Any:
        """Returns the value of an object attribute

        Do not call this method directly as it is a python magic function that
        will be implicitly called when executing `value = object.attribute` or
        `value = getattr(object, 'attribute')`

        Args:
            attr_name (string): the attribute name

        Returns:
            Any: the value of the attribute

        Raises:
            AttributeError: If the attribute is not definied in `Object.properties()`
        """

        if attr_name in self._properties():
            return super().__getattr__(attr_name)
        elif attr_name not in self.properties():
            raise AttributeError(f'Getting unknown property: `{self.classname()}.{attr_name}`.')
        return self._attributes.get(attr_name)


    def __setattr__(self, attr_name: str, value: Any):
        """Sets the value of an object attribute

        Do not call this method directly as it is a python magic function that
        will be implicitly called when executing `object.attribute = value` or
        `setattr(object, 'attribute', value)`

        Args:
            attr_name (string): the attribute name
            value (Any): the attribute value

        Raises:
            AttributeError: If the attribute is not definied in `Object.properties()`
        """

        if attr_name in self._properties() and not hasattr(self, attr_name):
            super().__setattr__(attr_name, value)
        elif attr_name not in self.properties():
            raise AttributeError(f'Setting unknown property: `{self.classname()}.{attr_name}`.')
        else:
            attr = self.properties().get(attr_name)
            if isinstance(attr, tuple) and value is not None:
                k, v = attr
                if type(value) != v:
                    raise AttributeError(f'`Value for {self.classname()}.{attr_name}` should be of type {v}; {type(value)} provided.')

            self._attributes.update({attr_name: value})


    def __str__(self) -> str:
        return json.dumps(self.attributes, use_decimal=True)


    def __repr__(self) -> str:
        return '{classname}(**{args})'.format(
            classname=self.classname(),
            args=self._raw_attributes
        )


    def _enforce_data_type(self, data: Any, data_type: type) -> Any:
        if data:
            if data_type in (str, int, float, complex, list, tuple, range, set, dict) or callable(data_type):
                return data_type(data)
        return data


    def _init_attributes(self):
        """Performs the mapping of the object's attributes based on the return
        value of `Object.properties()`
        """

        for k, v in self.properties().items():
            if isinstance(v, str) and v in self._raw_attributes:
                self._attributes.setdefault(k, self._raw_attributes.get(v))
            elif callable(v):
                self._attributes.setdefault(k, v())
            elif isinstance(v, tuple):
                attribute, data_type = v
                data = None
                if isinstance(attribute, str) and attribute in self._raw_attributes:
                    data = self._raw_attributes.get(attribute)
                elif callable(attribute):
                    data = attribute()
                self._attributes.setdefault(k,
                                            self._enforce_data_type(
                                                data, data_type))
            else:
                if v != k:
                    self._attributes.setdefault(k, self._raw_attributes.get(k, v))
                else:
                    self._attributes.setdefault(k, None)


    def _properties(self) -> List[str]:
        return ['_attributes', '_raw_attributes']


    @property
    def attributes(self) -> Dict[str, Any]:
        return self.get(*self.properties())


    def classname(self) -> str:
        """Returns the qualified name of this class.
        Returns:
            string: the qualified name of this class
        """

        return self.__class__.__name__


    def get(self, *attrs) -> Dict[str, Any]:
        return {
            k: v.get(*v.attributes)
            if isinstance(v, Object) else [x.attributes if isinstance(x, Object) else x for x in v]
            if isinstance(v, list) else {x: y.attributes if isinstance(y, Object) else y for x, y in v.items()}
            if isinstance(v, dict) else {x.get_id(): x.attributes for x in v}
            if isinstance(v, set) else v
            for k, v in self._attributes.items() if k in attrs
        }


    def get_id(self):
        return str(uuid.uuid4())


    def properties(self) -> Dict[str, Any]:
        return self._raw_attributes.get('properties') or {
            k: k for k,v in self._raw_attributes.items()
        }
