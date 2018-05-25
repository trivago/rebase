# [`rebase.core.Object`](/rebase/core/object.py)

The `rebase.core.Object` is an improved version of the base python `object`. It offers several generic functions that you can use to build your objects. It is the core of rebase and all the rebase components are built on it.

It offers the ability to declare public and private properties as well as introducing basic types on the properties. However the way to declare arguments within a class is different from what you normally do in python.

Depending on the arguments that you pass to the constructor, properties will be created dynamically.


## Documentation


### class rebase.core.Object


#### Public Properties

| Property  | Type          | Description                                                        | Defined By                             |
|-----------|---------------|--------------------------------------------------------------------|----------------------------------------|
| attributes | dictionary {string: Any} | The object attributes that can be publicly accessed and modified | [`rebase.core.Object`](#rebasecoreobject) |
| classname | string | The fully qualified name of the class | [`rebase.core.Object`](#rebasecoreobject) |


#### Public Methods

| Method    | Type          | Description                                                        | Defined By                             |
|-----------|---------------|--------------------------------------------------------------------|----------------------------------------|
| `__init__(self, **kwargs)` | void | Initialize the object based on arguments passed. If `properties()` method is not overridden, all arguments will be a property of the object. | [`rebase.core.Object`](#rebasecoreobject) |
| `__getattr__(self, attr_name: str) -> Any` | Any | Returns the value of the specified attribute. | [`rebase.core.Object`](#rebasecoreobject) |
| `__setattr__(self, attr_name: str, value: Any)` | void | Sets the value of the specified attribute. | [`rebase.core.Object`](#rebasecoreobject) |
| `__str__(self) -> str` | string | Returns a representation of the object in json. | [`rebase.core.Object`](#rebasecoreobject) |
| `__repr__(self) -> str` | string | Returns a representation of the object with initialized arguments. | [`rebase.core.Object`](#rebasecoreobject) |
| `get(self, *attrs) -> Dict[str, Any]` | dictionary {string: Any} | Returns all the object attributesm specified in the arguments, if they exist | [`rebase.core.Object`](#rebasecoreobject) |
| `get_id(self)` | string | Returns a unique uuid4. | [`rebase.core.Object`](#rebasecoreobject) |
| `properties(self) -> Dict[str, Any]` | dictionary {string: Any} | Returns the mapping of properties to argument of the object. | [`rebase.core.Object`](#rebasecoreobject) |


## How to use `rebase.core.Object`?
 - [Basic usage without inheriting](#basic-usage-without-inheriting)
 - [Extending and customizing an object](#extending-and-customizing-an-object)


### Basic usage without inheriting
You can create dynamic objects and use the arguments passed as properties.

```py
from rebase.core import Object

obj = Object(name='Paul', age=35, location='France')

print(obj.name) # Paul
print(obj.age) # 35
print(obj.location) # France
print(obj.attributes) # {'name': 'Paul', 'age': 35, 'location': 'France'}
print(obj.get('name', 'age')) # {'name': 'Paul', 'age': 35}
```

### Extending and customizing an object
You can also extend the object and create customized objects with specific properties. Mappings of the properties to the constructor arguments can be done easily and types of the property can be enforced.

```py
from rebase.core import Object

class Person(Object):
    def properties(self):
        return {
            'firstname': 'name',
            'age': ('age', int),
            'gender': ('gender', lambda x: int(x=='Male')),
            'city': 'location.city',
            'country': ('location.country', lambda x: x.upper()),
        }


obj = Person(
    name='Paul',
    age='35',
    gender="Male",
    location=dict(
        city='Paris',
        country='France'
    ),
    is_admin=False,
)

print(obj.attributes)
# {'firstname': 'Paul', 'age': 35, 'gender': 1, 'city': 'Paris', 'Country': France}
```
