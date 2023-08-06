"""Declares :class:`BaseResource`."""
from typing import Union

from fastapi import Request
from fastapi.responses import Response

from ..resourceendpointset import ResourceEndpointSet


class BaseResource:

    @classmethod
    def as_list(cls,
        endpoint: ResourceEndpointSet,
        items: list,
        metadata: dict
    ):
        """Return a collection of the resource."""
        return cls.List(
            apiVersion=cls.List._version,
            kind=cls.List._kind,
            metadata=metadata,
            items=[
                cls.as_resource(endpoint, x)
                for x in items
            ]
        )

    @classmethod
    def as_resource(cls,
        endpoint: ResourceEndpointSet,
        spec: Union[dict, list],
        name: str = None,
        namespace: str = None,
        metadata: dict = None
    ):
        """Create a fully-qualified representation of the resource."""
        metadata = metadata or {}
        metadata.update({
            'links': endpoint.get_resource_links(spec),
            'self_link': endpoint.get_detail_url(spec)
        })
        if namespace is not None:
            metadata['namespace'] = namespace
        if name is not None:
            metadata['name'] = name
        if isinstance(spec, list):
            raise NotImplementedError
        else:
            dto = cls(
                apiVersion=cls._version,
                kind=cls.__name__,
                metadata=metadata,
                spec=spec if isinstance(spec, dict) else cls.Spec.from_orm(spec)
            )
        return dto

    @classmethod
    def render_to_response(cls,
        endpoint: ResourceEndpointSet,
        request: Request,
        result: Union[list, dict],
        total_count: int = None
    ) -> Response:
        """Renders the result to a response.

        Args:
            endpoint (EndpointSet): the endpoint that is responding.
            request (fastapi.Request): the HTTP request to which a response
                is being served.
            result (dict, list): a dictionary (for a single object) or a list
                (for a result set).
            total_count (int): total items for this resource.

        Returns:
            :class:`BaseResource` or :class:`BaseResourceList`
        """
        metadata = {}
        if isinstance(result, list):
            metadata.update({
                'nextUrl': endpoint.get_next_url(total=total_count),
                'prevUrl': endpoint.get_prev_url()
            })
            if total_count is not None:
                metadata['totalItems'] = total_count
            response = cls.as_list(endpoint, result, metadata)
        else:
            response = cls.as_resource(
                endpoint,
                spec=result,
                metadata=metadata
            )
        return response
