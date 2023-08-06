"""Declares :class:`EndpointIAM`."""
from fastapi import Request
from unimatrix.conf import settings


class EndpointIAM:
    """Provides an interface to authenticate and authorize
    HTTP requests.
    """

    #: The list of audiences of which a bearer token must specify at least one
    #: (through the ``aud`` claim).
    audiences: set = set()

    #: The permission scope that an authenticated request must have.
    scope: set = set()

    #: The list of bearer token issuers that are trusted by this endpoint.
    #: This is also the return value of the default implementation of
    #: :meth:`get_trusted_issuers`.
    issuers: set = set()

    #: Indicate if the application default secret key is trusted by this
    #: endpoint.
    trust_local: bool = False

    def __init__(self, issuers: set, audiences: set, scope: set, local: bool):
        self.audiences = audiences
        self.issuers = issuers
        self.scope = scope
        self.trust_local = local

    def get_audience(self, request: Request) -> set:
        """Return the audience for this endpoint that is used to verify
        the ``aud`` claim of bearer tokens. The default implementation returns
        an empty list.
        """
        audiences = list(self.audiences)\
            + [f"https://{request.url.netloc}", "self"]\
            + list(settings.OAUTH2_AUDIENCES)
        return list(sorted(set(audiences)))

    def get_scope(self) -> set:
        """Return the scope that is required for authenticated requests."""
        return self.scope

    def get_trusted_issuers(self, request: Request) -> set:
        """Return the list of trusted issuers as compared against the ``iss``
        claim.
        """
        issuers = list(self.issuers)\
            + list(settings.OAUTH2_TRUSTED_STS)\
            + [f"https://{request.url.netloc}", "self"]
        return set(sorted(issuers))
