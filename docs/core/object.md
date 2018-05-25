# `rebase.core.Object`

The `rebase.core.Object` is an improved version of the base python `object`. It offers several generic functions that you can use to build your objects. It is the core of rebase and all the rebase components are built on it.

It offers the ability to declare public and private properties as well as introducing basic types on the properties. However the way to declare arguments within a class is different from what you normally do in python.

Dependinf on the arguments that you pass to the constructor, properties will be created dynamically.

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
