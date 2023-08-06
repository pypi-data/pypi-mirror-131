# pylint: skip-file
import sys

import fastapi
import ioc
from fastapi import Request

from .asgi import Application
from .decorators import action
from .dependency import inject
from .exceptions import UpstreamServiceNotAvailable
from .exceptions import UpstreamConnectionFailure
from .keytrustpolicy import KeyTrustPolicy
from .resource import resource
from .resourceendpointset import ResourceEndpointSet
from .resourceendpointset import PublicResourceEndpointSet
from .service import Service


__all__ = [
    'action',
    'inject',
    'limit',
    'offset',
    'resource',
    'Application',
    'EndpointSet',
    'PublicEndpointSet',
    'Service',
    'UpstreamConnectionFailure',
    'UpstreamServiceNotAvailable',
]


Endpoint = ResourceEndpointSet
EndpointSet = ResourceEndpointSet
PublicEndpointSet = PublicResourceEndpointSet


def singleton(cls):
    """Class decorator that indicates that a resource is a singleton."""
    cls.singleton = True
    return cls


def permission(name: str):
    """Decorate a function to require the given permission `name`."""
    def decorator_factory(func):
        if not hasattr(func, 'permissions'):
            func.permissions = set()
        func.permissions.add(name)
        return func
    return decorator_factory


def policy(tags: list) -> KeyTrustPolicy:
    """Declares a policy for an endpoint to determine which public keys
    it wants to trust.

    Args:
        tags (list): The list of tags that this policy accepts.

    Returns:
        A :class:`KeyTrustPolicy` instance.
    """
    return KeyTrustPolicy(tags)


def offset(default=0):
    """Creates the ``offset`` query parameter for request
    handlers.
    """
    return fastapi.Query(
        default,
        title='offset',
        description=(
            "The number of objects to skip from the beginning "
            "of the result set."
        )
    )


def limit(default=100, limit=None):
    """Creates the ``limit`` query parameter for request
    handlers.
    """
    limit = default * 3
    return fastapi.Query(
        default,
        title='limit',
        description=(
            "Optional limit on the number of objects to include "
            "in the response.\n\n"
            f"The default is {default}, and the maximum is {limit}."
        )
    )
