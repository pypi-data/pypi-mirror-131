def fmap(fn, data):
    """Apply fn to all elements in data and construct a new object of the same type.

    >>> fmap(lambda x: x*2, data=dict(a=1, b=2))
    {'a': 2, 'b': 4}

    Raises `TypeError` if the type of `data` has not been registered with `register_functor`
    """
    try:
        functor = _fmap_vtable[type(data)]
    except KeyError as e:
        raise TypeError(f"{type(data)} is not registered as a Functor") from e
    return functor(fn, data)


global _fmap_vtable
_fmap_vtable = {}

def register_functor(type_, func):
    """Register a type_ to be a Functor with fmap=`func`.

    From hereon, it is legit to use `fmap` for objects of that type.
    """
    _fmap_vtable[type_] = func
    return func


fmap_apply = lambda fn, data: fn(data)
"""Helper: applies fn to data"""

fmap_construct_from_mapped = lambda fn, data: type(data)(map(fn, data))
"""Helper: constructs source type with generator  (Works well for some types like tuple and list)"""

register_functor(None, lambda fn, data: None)
register_functor(int, fmap_apply)
register_functor(str, fmap_apply)
register_functor(float, fmap_apply)
register_functor(bool, fmap_apply)
register_functor(list, fmap_construct_from_mapped)
register_functor(tuple, fmap_construct_from_mapped)
register_functor(dict, lambda fn, data: {key: fn(value) for key, value in data.items()})
