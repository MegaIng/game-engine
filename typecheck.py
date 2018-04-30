from __future__ import annotations

import inspect
from functools import wraps
from typing import Dict, Tuple, Any, get_type_hints, Callable, _GenericAlias, Union, Iterable, Sequence, _SpecialForm

config = dict(
    enabled=__debug__
)


def typecheck_value(type_hint: Any, value: Any) -> bool:
    try:
        return isinstance(value, type_hint)
    except TypeError:
        if type_hint.__class__ is _SpecialForm:
            if type_hint._name == 'Any':
                return True
        elif type_hint.__class__ is _GenericAlias:
            if type_hint._name == 'Tuple':
                if not isinstance(value, tuple):
                    return False
                args = type_hint.__args__
                if len(args) == 2 and args[-1] == Ellipsis:
                    return all(typecheck_value(args[0], v) for v in value)
                else:
                    return all(typecheck_value(t, v) for t, v in zip(args, value))
            elif type_hint._name == 'Dict':
                if not isinstance(value, dict):
                    return False
                tk, tv = type_hint.__args__
                return all(typecheck_value(tk, k) and typecheck_value(tv, v) for k, v in value.items())
            elif type_hint._name == 'Iterable':
                return isinstance(value, Iterable)
            elif type_hint._name == 'Sequence':
                th, = type_hint.__args__
                return isinstance(value, Sequence) and all(typecheck_value(th, v) for v in value)
            elif type_hint._name == 'List':
                th, = type_hint.__args__
                return isinstance(value, list) and all(typecheck_value(th, v) for v in value)
            elif type_hint.__origin__ == Union:
                return any(typecheck_value(th, value) for th in type_hint.__args__)
        else:
            raise NotImplementedError
    raise TypeError(f"Can't handle type hint {type_hint}")


def typecheck_function(func: Callable, args: Tuple[Any, ...], kwargs: Dict[str, Any], type_hints: Dict[str, Any] = None, localns: Dict[str, Any] = None) -> bool:
    if type_hints is None:
        type_hints = get_type_hints(func, localns=localns)
    signature = inspect.signature(func)
    try:
        bound_args: inspect.BoundArguments = signature.bind(*args, **kwargs)
    except TypeError:
        return False
    for name, value in bound_args.arguments.items():
        if not typecheck_value(type_hints.get(name, Any), value):
            return False
    return True


def get_typechecked_function(func: Callable, type_hints: Dict[str, Any] = None, localns: Dict[str, Any] = None):
    if type_hints is None:
        type_hints = get_type_hints(func, localns=localns)
    result_type_hint = type_hints.get("return", Any)

    @wraps(func)
    def _(*args, **kwargs):
        if config["enabled"]:
            if not typecheck_function(func, args, kwargs, type_hints, localns):
                raise TypeError(f"Unallowed args or kwargs for function '{func.__qualname__}' (args:{args}, kwargs:{kwargs}) ({type_hints})")

        result = func(*args, **kwargs)
        if config["enabled"]:
            if not typecheck_value(result_type_hint, result):
                raise TypeError(f"Unexpected return value '{result}'. Expected '{result_type_hint}'")
        return result

    return _

def get_typechecked_class(cls: type, check_setattr=False):
    localns = {cls.__name__: cls}
    for n, v in cls.__dict__.items():
        if callable(v):
            setattr(cls, n, get_typechecked_function(v, localns=localns))
    if "__setattr__" not in cls.__dict__ and check_setattr:
        old_setattr = cls.__setattr__
        type_hints = get_type_hints(cls, localns=localns)

        @wraps(old_setattr)
        def __setattr__(obj, name, value):
            if config["enabled"]:
                if name not in type_hints:
                    raise TypeError(f"Can't create attribute '{name}' for class '{cls.__name__}'")
                if not typecheck_value(type_hints[name], value):
                    raise TypeError(f"Can't set attribute '{name}' of class '{cls.__name__}' to value '{value}'")
            return old_setattr(obj, name, value)

        cls.__setattr__ = __setattr__
    return cls


def typecheck(obj: Union[type, Callable] = None, *, typecheck_setattr=False):
    def _(obj: Union[type, Callable]):
        if isinstance(obj, type):
            return get_typechecked_class(obj, typecheck_setattr)
        else:
            return get_typechecked_function(obj)

    if obj is not None:
        return _(obj)
    return _
