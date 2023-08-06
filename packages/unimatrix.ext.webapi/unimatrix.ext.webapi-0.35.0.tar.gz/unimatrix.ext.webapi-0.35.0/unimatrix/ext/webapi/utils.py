# pylint: skip-file
import collections
import inspect
import itertools
import types

import fastapi


SORT_ORDER = {
    inspect.Parameter.POSITIONAL_ONLY: 1,
    inspect.Parameter.POSITIONAL_OR_KEYWORD: 2,
    inspect.Parameter.VAR_POSITIONAL: 3,
    inspect.Parameter.KEYWORD_ONLY: 4,
    inspect.Parameter.VAR_KEYWORD: 5,
}


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
