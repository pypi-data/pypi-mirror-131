"""Declares :class:`RequestPrincipalResolver`."""
import logging

from fastapi import Request
from unimatrix.ext import crypto
from unimatrix.ext import jose

from .auth import IPrincipal
from .endpointiam import EndpointIAM
from .exceptions import TrustIssues
from .exceptions import UpstreamServiceNotAvailable
from .keytrustpolicy import KeyTrustPolicy


class RequestPrincipalResolver:
    """Declares an interface to resolve requests and provided
    bearer tokens to principals.
    """
    logger = logging.getLogger('uvicorn')

    async def resolve(self,
        request: Request,
        iam: EndpointIAM,
        bearer: str,
        policy: KeyTrustPolicy
    ) -> IPrincipal:
        """Use the credentials provided with an HTTP request to
        resolve a principal.
        """
        # Get the header from the JWS. If the header does not contain the
        # `kid` claim, then we assume that the token was issued using our
        # own secret key (HS256 or similar). A JWS that specifies the `kid`
        # claim in its header, was signed by a third party. This key is
        # retrieved from the key registry and matched against the policy
        # specified by the invocation parameters.
        jws = jose.parse(str.encode(bearer))
        await self.verify(jws, iam, policy)
        jws.payload.verify(
            audience=iam.get_audience(request),
            issuers=iam.get_trusted_issuers(request),
            scope=iam.get_scope(),
            required={"iss", "aud", "iat", "exp", "sub"}
        )

        return jws.payload.claims

    async def verify(self,
        jws: jose.JSONWebSignature,
        iam: EndpointIAM,
        policy: KeyTrustPolicy
    ):
        """Verify the JSON Web Signature (JWS), or raise an exception."""
        key = await self._get_key(jws)
        await jws.verify(key)

        # Enforce policy for signatures that have the .kid claim
        # specified in the header. Signatures with .kid are
        # assumed to come from other sources, so we enforce
        # policy.
        if policy is not None and jws.kid is not None:
            await policy.enforce(key)

    async def _get_key(self, jws: jose.JSONWebSignature) -> crypto.PublicKey:
        # If there is no .kid claim, then we signed to token with our default
        # in-memory application key.
        if jws.header.kid is None:
            key = crypto.get_secret_key()
        else:
            key = await self.get_public_key(jws.kid, jws.payload)
        return key

    async def get_public_key(self, kid, jwt, attempts=0, max_attempts=5):
        """Returns the public key identified by `kid`."""
        try:
            return crypto.trust.get(kid)
        except LookupError:
            if not jwt.iss or (jwt.iss == 'self'):
                raise TrustIssues(message=f"Untrusted issuer: {jwt.iss}")
            self.logger.debug(
                "Public key unknown, trying lookup (kid: %s, issuer: %s)",
                kid, jwt.iss
            )
            if attempts >= max_attempts:
                self.logger.error(
                    "Could not retrieve key after %s attempts "
                    "(kid: %s, issuer: %s)",
                    attempts, kid, jwt.iss
                )
                raise UpstreamServiceNotAvailable
            if attempts > 0:
                self.logger.warning("Retrying JWKS lookup for %s", jwt.iss)
            await crypto.trust.jwks(jwt.iss,
                ['oauth2.sts'],
                {'oauth2/sts': jwt.iss}
            )
            self.logger.debug("Retrieved public key (kid: %s, issuer: %s)",
                kid, jwt.iss)
            return await self.get_public_key(kid, jwt, attempts+1)
