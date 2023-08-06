# PyLib - General

This is a package that will be updated whenever I get an idea that I like and write it.

So far, I have:
- Properties


## Properties

This can be used like:

`from pylib_general import properties`

This loads the Property class, which can be used like:

`varname = properties.Property()`

The property class's functions are:

- `varname.add(name, val)`

`name` being the name of the new value (cannot contain spaces), and `val` being the value.

- `varname.remove(name)`
`name` being the name of the value to remove

- `varname.get(name)`
returns the value of `name`

The difference between Property and other sets is that you can get a property in a much easier way:

`varname.attr`

Obviously, you can also get a value through `varname.get(name)` but you could also do `varname.name`

Ex:

```
varname = Property().add("somenamenotcontainingnumbersorspaces", "12233090")
print(varname.somenamenotcontainingnumbersorspaces)
```
prints `12233090`
