# rebase [![Build Status](https://travis-ci.org/trivago/rebase.svg?branch=master)](https://travis-ci.org/trivago/rebase)


## What is it?
Rebase is a small library consisting of powerful reusable components aimed at making your Data Layer more more robust. With the changes of how data is being stored in databases, it is becoming very challenging to validate data specially in NoSQL databases.

Rebase is designed in such a way that it is easier to manipulate the data and project them in different views.


## Challenges that lead to this idea
Working daily with data having different structures becomes a pain eventually. Sometimes you have to adapt or map an object to another format or apply some filters to part of the data. This occurs very often when have data coming from different sources and want to conform them.

## Getting Started

### Installation
Install via [pip](http://www.pip-installer.org/)
```bash
$ pip install rebase
```

## Documentation

### core
 - [rebase.core.Object](docs/core/object.md)
 - [rebase.core.Model](docs/core/model.md)
 - [rebase.core.Validator](docs/core/validator.md)
### validators
 - [rebase.validators.BoolValidator](docs/validators/bool_validator.md)
 - [rebase.validators.IntegerValidator](docs/validators/integer_validator.md)
 - [rebase.validators.NestedValidator](docs/validators/nested_validator.md)
 - [rebase.validators.RangeValidator](docs/validators/range_validator.md)
