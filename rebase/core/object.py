import uuid
from typing import Any, Dict, List

import simplejson as json


class Object(object):
    def __init__(self, **kwargs):
        """Initialize the object with the given attributes.

        If this method is overridden in the child, the parent implementation
        should be called in order to properly assign attributes.

        By default attributes are assigned dynamically to the object. But to
        have more control in child classes (such as remapping), it is
        recommended to override the `Object.properties()` method.

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
        self._id = None
        self._init_attributes()

    def __getattr__(self, attr_name: str) -> Any:
        """Return the value of an object attribute.

        Do not call this method directly as it is a python magic function that
        will be implicitly called when executing `value = object.attribute` or
        `value = getattr(object, 'attribute')`

        Args:
            attr_name (string): the attribute name

        Returns:
            Any: the value of the attribute

        Raises:
            AttributeError: If attribute is undefinied in `Object.properties()`

        """
        if attr_name in self._properties():
            return super().__getattr__(attr_name)
        elif attr_name not in self.properties():
            raise AttributeError(
                f'Getting unknown property: `{self.classname()}.{attr_name}`.')
        return self._attributes.get(attr_name)

    def __setattr__(self, attr_name: str, value: Any):
        """Set the value of an object attribute.

        Do not call this method directly as it is a python magic function that
        will be implicitly called when executing `object.attribute = value` or
        `setattr(object, 'attribute', value)`

        Args:
            attr_name (string): the attribute name
            value (Any): the attribute value

        Raises:
            AttributeError: If attribute is undefinied in `Object.properties()`

        """
        if attr_name in self._properties():
            super().__setattr__(attr_name, value)
        elif attr_name not in self.properties():
            raise AttributeError(
                f'Setting unknown property: `{self.classname()}.{attr_name}`.')
        else:
            attr = self.properties().get(attr_name)
            if isinstance(attr, tuple) and value is not None:
                k, v = attr
                if type(value) != v:
                    raise AttributeError(
                        f'`Value for {self.classname()}.{attr_name}` should be of type {v}; {type(value)} provided.')

            self._attributes.update({attr_name: value})

    def __str__(self) -> str:
        return json.dumps({
            '_id': self.get_id(),
            'attributes': self.attributes
        }, use_decimal=True)

    def __repr__(self) -> str:
        return '{classname}(**{args})'.format(
            classname=self.classname(),
            args=self._raw_attributes
        )

    def _enforce_data_type(self, data: Any, data_type: type) -> Any:
        try:
            if data:
                if data_type in (bool, str, int, float, complex, list, tuple, range, set, dict) or callable(data_type):
                    return data_type(data)
        except TypeError:
            return data

        return data

    def _init_attributes(self):
        """Perform the mapping of attributes based `Object.properties()`.

        Returns:
            void

        """
        for k, v in self.properties().items():
            if isinstance(v, str) and v in self._raw_attributes:
                self._attributes.setdefault(
                    k, self._get_attr_recurse(v, self._raw_attributes))
            elif callable(v):
                self._attributes.setdefault(k, v())
            elif isinstance(v, tuple):
                attribute, data_type = v
                data = attribute
                if isinstance(attribute, str) and attribute in self._raw_attributes:
                    data = self._get_attr_recurse(
                        attribute, self._raw_attributes)
                elif callable(attribute):
                    data = attribute()

                self._attributes.setdefault(k,
                                            self.enforce_data_type(
                                                data, data_type))
            else:
                if v != k:
                    self._attributes.setdefault(
                        k, self._raw_attributes.get(k, v))
                else:
                    self._attributes.setdefault(k, None)

    def _get_attr_recurse(self, attr, obj):
        if isinstance(obj, Object):
            return self._get_attr_recurse(attr, obj.attributes)
        elif obj is None:
            return None

        attr_list = attr.split('.')
        key = attr_list.pop(0)
        if key not in obj:
            return None

        if len(attr_list) == 0:
            return obj.get(key)
        else:
            return self._get_attr_recurse('.'.join(attr_list), obj.get(key))

    def _properties(self) -> List[str]:
        return ['_id', '_attributes', '_raw_attributes']

    @property
    def attributes(self) -> Dict[str, Any]:
        return self.get(*self.properties())

    def classname(self) -> str:
        """Return the qualified name of this class.

        Returns:
            string: the qualified name of this class

        """
        return self.__class__.__name__

    def get(self, *attrs) -> Dict[str, Any]:
        """Return a dict of the attribute names passed as arguments.

        Args:
            attrs (list): comma separated name of attributes for the object

        Returns:
            dict: the attributes of the object if set

        """
        return {
            k: v.get(*v.attributes)
            if isinstance(v, Object) else [
                x.attributes
                if isinstance(x, Object) else x
                for x in v
            ]
            if isinstance(v, list) else {
                x: y.attributes
                if isinstance(y, Object) else y
                for x, y in v.items()
            }
            if isinstance(v, dict) else {
                x.get_id(): x.attributes
                for x in v
            }
            if isinstance(v, set) else v
            for k, v in self._attributes.items() if k in attrs
        }

    def get_id(self):
        if not self._id:
            self._id = str(uuid.uuid4())
        return self._id

    def properties(self) -> Dict[str, Any]:
        return self._raw_attributes.get('properties') or {
            k: k for k, v in self._raw_attributes.items()
        }