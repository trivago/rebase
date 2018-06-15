# [`rebase.core.Model`](/rebase/core/model.py)

The `rebase.core.Model` represents an entity which can have a set of rules to be validated against. A model can have different scenarios each having different set of validation rules.

After validation has been triggered the model receives the errors from the validators if the validation failed for a specific rule. Context and scenarios can also be used to have different projection of the attributes.

## Documentation


### class rebase.core.Object


#### Public Properties

| Property  | Type          | Description                                                        | Defined By                             |
|-----------|---------------|--------------------------------------------------------------------|----------------------------------------|
| attributes | dictionary {string: Any} | The object attributes that can be publicly accessed and modified | [`rebase.core.Object`](#rebasecoreobject) |
| classname | string | The fully qualified name of the class | [`rebase.core.Object`](#rebasecoreobject) |


#### Public Methods


## How to use `rebase.core.Model`?
