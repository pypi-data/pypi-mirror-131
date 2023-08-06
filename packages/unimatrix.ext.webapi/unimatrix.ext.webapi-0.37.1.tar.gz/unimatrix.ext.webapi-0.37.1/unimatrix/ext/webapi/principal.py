# pylint: disable=line-too-long
"""Declares :class:`CurrentPrincipal`."""
from fastapi import Depends
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from .auth import IPrincipal
from .dependency import inject
from .requestprincipalresolver import RequestPrincipalResolver


async def get_principal(
    request: Request,
    bearer: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(auto_error=False)
    ),
    resolver: RequestPrincipalResolver = inject(
        'RequestPrincipalResolver',
        default=RequestPrincipalResolver()
    )
) -> IPrincipal:
    """Return the current principal that was authenticated using the
    credentials attached to the HTTP request, or ``None`` if
    the credentials were missing or invalid.
    """
    if bearer is None:
        return None


BearerPrincipal = fastapi.Depends(get_principal)
