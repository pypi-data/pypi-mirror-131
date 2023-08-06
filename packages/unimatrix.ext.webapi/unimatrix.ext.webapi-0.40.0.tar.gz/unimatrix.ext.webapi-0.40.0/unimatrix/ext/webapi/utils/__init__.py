# pylint: skip-file
import collections
import functools
import inspect
import itertools
import types

import fastapi

from .mediatypes import media_type_matches


SORT_ORDER = {
    inspect.Parameter.POSITIONAL_ONLY: 1,
    inspect.Parameter.POSITIONAL_OR_KEYWORD: 2,
    inspect.Parameter.VAR_POSITIONAL: 3,
    inspect.Parameter.KEYWORD_ONLY: 4,
    inspect.Parameter.VAR_KEYWORD: 5,
}


def class_dependency(func, dst: str = None, **requires):
    """Inject a class method as a dependency."""
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        kwargs = {k: v for k, v in dict.items(kwargs) if k in names}
        result = await func(*args, **kwargs)
        if dst is not None:
            setattr(func.__self__, dst, result)
        return result

    sig = inspect.signature(wrapped)
    names = list(sig.parameters.keys())
    params =  collections.OrderedDict([
        (k, v) for k, v in sig.parameters.items()
    ])
    for name, depends in dict.items(requires):
        params[name] = inspect.Parameter(
            name=name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=depends
        )

    wrapped.__signature__ = sig.replace(
        parameters=sorted(params.values(), key=lambda x: SORT_ORDER[x.kind])
    )

    clean_signature(wrapped)
    return fastapi.Depends(wrapped)   


def as_dependant(func, process_result=None):
    @functools.wraps(func)
    async def dependant(*args, **kwargs):
        result = await func(*args, **kwargs)
        if process_result is not None:
            process_result(result)
        return result
    clean_signature(dependant)
    return dependant


def clean_signature(func) -> None:
    """Removes unwanted parameters from the signature to prevent
    confusing FastAPI.
    """
    sig = inspect.signature(func)
    parameters = []
    for varname, param in list(sig.parameters.items()):
        if varname in ('self', 'args', 'kwargs'):
            continue
        parameters.append(param)
    func.__signature__ = sig.replace(parameters=parameters)
    return func


def get_parameters(func) -> collections.OrderedDict:
    """Return an ordered dictionary containing the function parameters."""
    sig = inspect.signature(func)
    return collections.OrderedDict(sig.parameters.items())


def clone_signature(
    src: types.FunctionType,
    dst: types.FunctionType,
    replace: dict = None,
    clean: bool = True
):
    """Clones the signature for `src` into function `dst`."""
    update_parameters(dst, {
        **get_parameters(src),
        **(replace or {})
    })
    if clean:
        clean_signature(dst)


def update_parameters(func: types.FunctionType, replace: dict = None):
    """Return the parameters of the given function `func`."""
    replace = replace or {}
    sig = inspect.signature(func)
    parameters = collections.OrderedDict(sig.parameters.items())
    for varname, param in dict.items(replace):
        parameters.pop(varname, None)
        parameters[varname] = param

    func.__signature__ = sig.replace(
        parameters=sorted(
            parameters.values(), key=lambda x: SORT_ORDER[x.kind]
        )
    )
