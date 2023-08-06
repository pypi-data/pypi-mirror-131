# pylint: skip-file
import fastapi
import ioc


def inject(name, invoke=False, default=None, *args, **kwargs):
    """Injects the named dependency `name` into the :mod:`fastapi`
    dependency resolver.
    """
    async def provide():
        if not ioc.is_satisfied(name) and default is not None:
            dependency = default
        else:
            dependency = ioc.require(name)
        if not hasattr(dependency, '__aenter__'):
            yield dependency if not invoke else dependency(*args, **kwargs)
            return
        if invoke:
            dependency = dependency(*args, **kwargs)
        async with dependency:
            yield dependency
    return fastapi.Depends(provide)
