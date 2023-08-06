# pylint: skip-file
"""Declares :class:`ResourceEndpointSet`."""
import copy
import functools
import inspect
import re
import types
import typing
import urllib.parse
from collections import OrderedDict

import ioc
import fastapi
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from fastapi.dependencies.utils import solve_dependencies
from pydantic import BaseModel
from unimatrix.conf import settings
from unimatrix.lib.datastructures import ImmutableDTO, DTO

from .auth import IHTTPAuthenticationService
from .auth import IPrincipal
from .dependency import inject
from .exceptions import BearerAuthenticationRequired
from .exceptions import ParseError
from .endpointiam import EndpointIAM
from .exceptions import NotAuthorized
from .exceptions import TrustIssues
from .negotiation import DefaultContentNegotiation
from .negotiation import IContentNegotiation
from .parsers import IParser
from .parsers import JSONParser
from .requestprincipalresolver import RequestPrincipalResolver
from .resourceschema import ResourceSchema
from .utils import as_dependant
from .utils import class_dependency
from .utils import clean_signature
from .utils import clone_signature


ACTION_METHODS = {
    'apply'     : 'PATCH',
    'create'    : 'POST',
    'destroy'   : 'DELETE',
    'index'     : 'GET',
    'purge'     : 'DELETE',
    'replace'   : 'PUT',
    'retrieve'  : 'GET',
    'update'    : 'POST',
}

DEFAULT_ACTIONS = [
    'create', 'retrieve', 'update', 'destroy', 'index', 'apply', 'replace',
    'purge'
]

DETAIL_ACTIONS = {'retrieve', 'update', 'replace', 'destroy', 'apply'}


def get_return_type(handler):
    rettype = typing.get_type_hints(handler).get('return')
    if rettype and not issubclass(rettype, BaseModel): # pragma: no cover
        rettype = None
    return rettype


class ResourceEndpointSetMetaclass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        if name in ('ResourceEndpointSet', 'PublicResourceEndpointSet'):
            return super_new(cls, name, bases, attrs)

        # Instantiate the IAM handler for the endpoint.
        iam_class = attrs.pop('iam_class', EndpointIAM)
        attrs['iam'] = iam_class(
            issuers=set(attrs.pop('trusted_issuers', [])),
            audiences=set(attrs.pop('accepted_audiences', [])),
            scope=set(attrs.pop('required_scope', [])),
            local=attrs.pop('trust_local', False)
        )

        new_class = super_new(cls, name, bases, attrs)
        hints = typing.get_type_hints(new_class)

        # Add the action attribute to known actions so that we can process them
        # later on consistently with user-defined actions.
        #
        # TODO: Do not add them as action attribute because it confuses other
        # methods. Refactor the *class* actions attribute to hold all actions.
        new_class.actions = []
        for attname in new_class.__dict__:
            handler = new_class.__dict__[attname]
            if attname not in DEFAULT_ACTIONS\
            and not hasattr(handler, 'action'):
                continue
            if hasattr(handler, 'action'):
                new_class.actions.append(handler.action)
                continue

            is_detail = attname in DETAIL_ACTIONS
            action = DTO(
                name=attname,
                methods=[ ACTION_METHODS[attname] ],
                detail=is_detail,
                is_default=True,
                path=f'{new_class.path_parameter}' if is_detail else ''
            )
            new_class.actions.append(action)

        # Convert the path_parameter attribute to an inspect.Parameter
        # instance. This is later used for constructing the appropriate
        # signature. If there is no annotation, assume that it is a string.
        new_class.path_parameter = inspect.Parameter(
            new_class.path_parameter,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=hints.get('path_parameter') or str,
            default=new_class.path_parameter
        )

        #: If the class has subresources, copy them and add this class as
        #: the parent attribute.
        new_class.subresources = copy.deepcopy(new_class.subresources or [])
        for sub in new_class.subresources:
            sub.parent_class = new_class

            # Add the subresource itself as an action. Some special handling
            # is required here because the class itself is not a valid named
            # URL, so we have to do some hacking.
            new_class.actions.append(
                ImmutableDTO({
                    'detail': True,
                    'name': f'{sub.resource_name}',
                    'path': sub.resource_name,
                    'is_default': False,
                    'subresource': True
                })
            )

            # Also iterate over the actions included on the subresource
            # class, and add them as detail actions on the parent class
            # if they are *not* detail actions on the child class.
            for action in sub.actions:
                if action.detail or getattr(action, 'is_default', False):
                    continue
                new_class.actions.append(
                    ImmutableDTO({
                        'detail': True,
                        'name': f'{sub.resource_name}.{action.name}',
                        'path': f'{sub.resource_name}/{action.path}',
                        'is_default': False
                    })
                )

        return new_class


class ResourceEndpointSet(metaclass=ResourceEndpointSetMetaclass):
    """Groups a set of endpoints that allow reading, mutating and
    destroying a specific resource.
    """
    #: The content negiotiation procedure. Subclasses may override
    #: this attribute to provide their own implementation.
    #: See also :class:`~unimatrix.ext.webapi.negotiation.IContentNegotiation`.
    negotiator: IContentNegotiation = DefaultContentNegotiation()

    #: The list of request body parsers in order of preference.
    parsers: typing.List[IParser] = []

    default_parsers: typing.List[IParser] = [
        JSONParser
    ]

    parent_class = None

    #: The list of valid action names.
    valid_actions: list = DEFAULT_ACTIONS

    #: The current request that is being handled. This attribute is ``None``
    #: when initializing :class:`ResourceEndpointSet` and is set when the ASGI
    #: interface function is invoked.
    request: Request = None

    #: The schema class used to serialize and deserialize the resource.
    resource_schema: ResourceSchema = None

    #: The name of the resource identifier as a path path_parameter.
    path_parameter: str = 'resource_id'

    #: Set this to ``True`` if the path parameter may have
    #: slashes.
    path_allows_slashes: bool = False

    #: A list of :class:`ResourceEndpointSet` implementations representing
    #: subresources. Subresources always operate on a single object.
    subresources: list = []

    #: Indicates if a request must be authenticated using the ``Authorization``
    #: header.
    require_authentication: bool = True

    #: The list of audiences of which a bearer token must specify at least one
    #: (through the ``aud`` claim).
    accepted_audiences: set = []

    #: The permission scope that an authenticated request must have.
    required_scope: set = []

    #: The list of bearer token issuers that are trusted by this endpoint.
    #: This is also the return value of the default implementation of
    #: :meth:`get_trusted_issuers`.
    trusted_issuers: set = []

    #: Specifies the internal name of the resource that may be used to
    #: reverse its endpoints e.g. if :attr:`resource_name` is `foo`,
    #: then the `retrieve` method becomes reversible by the name
    #: `foo.retrieve`. If :attr:`resource_name` is not defined, then the
    #: class name is used.
    resource_name: str = None

    #: Specifies a human-readable name to group the endpoint set under.
    group_name: str = None

    #: The policy used to determine wether a key is trusted or not.
    trust_policy = None

    #: Indicate if the application default secret key is trusted by this
    #: endpoint.
    trust_local: bool = False

    #: Indicates if the resource is a singleton and detail-specific
    #: behavior must be forced.
    singleton: bool = False

    #: The maximum number of results for a list request.
    max_items: int = 100

    #: The resource class used by the standard endpoints. See also
    #: :func:`unimatrix.ext.webapi.resource`.
    resource_class = None

    #: The class used to handle IAM.
    iam_class: type = EndpointIAM

    @property
    def handler(self):
        """Return the current request handler."""
        return getattr(self, self.action)

    @functools.cached_property
    def parameters(self) -> typing.List[inspect.Parameter]:
        """Return the list of path parameters as :class:`inspect.Parameter`
        instances.
        """
        path = []
        if self.parent_class:
            path.extend([x.path_parameter for x in self.get_ancestors()])
        path.append(self.path_parameter)
        return path

    @functools.cached_property
    def qualname(self) -> str:
        """The qualified name of the endpoint, including parent classes."""
        return self.resource_name\
            if self.parent_class is None\
            else (
                f"{str.join('.', [x.resource_name for x in self.get_ancestors()])}"
                f".{self.resource_name}"
            )

    def __init__(self, action, *args, **kwargs):
        self.action = action

    @classmethod
    def add_to_router(cls,
        router: APIRouter,
        base_path: str,
        parent: 'ResourceEndpointSet' = None,
        url_params: list = None,
        base_name: str = None,
        group_name: str = None,
        path_parameters: list = None
    ) -> None:
        """Add the :class:`ResourceEndpointSet` to a router instance at the given
        `base_path`.
        """
        path_parameters = path_parameters or []
        if not cls.singleton:
            path_parameters.append(cls.path_parameter)
        cls.path_parameters = copy.deepcopy(path_parameters)
        url_params = []
        base_name = str.lower(
            base_name
            or cls.resource_name
            or re.sub('(Ctrl|EndpointSet)', '', cls.__name__)
        )
        if parent is not None:
            base_name = f'{base_name}.' + str.lower(
                cls.resource_name
                or re.sub('(Ctrl|EndpointSet)', '', cls.__name__)
            )

        group_name = group_name or cls.group_name
        if parent:
            url_params.insert(0, parent.path_parameter.default)
        if not str.startswith(base_path, '/'): # pragma: no cover
            raise ValueError("The `base_path` must begin with a slash (/).")

        # Iterate over methods that are marked as actions.
        for attname, obj in list(cls.__dict__.items()):
            if not hasattr(obj, 'action'):
                continue
            if obj.action.name == 'action': # pragma: no cover
                raise ValueError('Can not use `action` as a function name.')

            path = base_path
            if obj.action.detail:
                path = f'{base_path}/{{{cls.path_parameter.default}}}'
                if cls.path_allows_slashes:
                    path = f'{base_path}/{{{cls.path_parameter.default}:path}}'
                path = re.sub('^[/]+', '/', path) # TODO: hack

                # Check if the path parameter name is not the same as the
                # parent class
                if parent and parent.path_parameter.default\
                == cls.path_parameter.default: # pragma: no cover
                    raise ValueError(
                        "Parent path parameter name must be different from "
                        "the child."
                    )

            tags = []
            if group_name: # pragma: no cover
                tags.append(group_name)
            path = f'{path}/{obj.action.path}'
            name = f'{base_name}.{str.lower(obj.action.name)}'
            router.add_api_route(
                path,
                cls._create_annotated_handler(
                    cls, obj.action.name, obj, parent=parent,
                    detail=obj.action.detail,
                    path=path,
                    path_parameters=path_parameters,
                    logger=router.logger
                ),
                name=name,
                summary=name,
                tags=tags,
                methods=obj.action.methods,
                response_model=getattr(
                    obj,
                    'response_model',
                    get_return_type(obj)),
                response_model_exclude_defaults=True,
                response_model_exclude_none=True,
            )

        has_detail_methods = False
        has_collection_methods = False or cls.singleton
        for action in cls.valid_actions:
            # Create a fake signature to trick FastAPI in registering the
            # correct path parameters, authentication schemes, etc.
            handler = getattr(cls, action, None)
            path = base_path
            if handler is None: # pragma: no cover
                continue

            # Add the path parameter for actions that operate on a specific
            # resource.
            is_detail = (action in DETAIL_ACTIONS)
            if is_detail and not cls.singleton:
                has_detail_methods = True
                path = f'{base_path}/{{{cls.path_parameter.default}}}'
                if cls.path_allows_slashes:
                    path = f'{base_path}/{{{cls.path_parameter.default}:path}}'
                path = re.sub('^[/]+', '/', path) # TODO: hack

                # Check if the path parameter name is not the same as the
                # parent class
                if parent and parent.path_parameter.default\
                == cls.path_parameter.default: # pragma: no cover
                    raise ValueError(
                        "Parent path parameter name must be different from "
                        "the child."
                    )
            else:
                has_collection_methods = True

            name = f'{base_name}.{action}'
            summary = name
            tags = []
            if group_name: # pragma: no cover
                tags.append(group_name)
            router.add_api_route(
                path,
                cls._create_annotated_handler(
                    cls, action, handler,
                    parent=parent,
                    detail=is_detail,
                    path=path,
                    path_parameters=path_parameters,
                    logger=router.logger
                ),
                name=name,
                summary=summary,
                tags=tags,
                methods=[ ACTION_METHODS[action] ],
                response_model=getattr(
                    handler,
                    'response_model',
                    get_return_type(handler)),
                response_model_exclude_defaults=True,
                response_model_exclude_none=True,
            )

        # Iterate over subresources and add them add detail endpoints.
        for subresource_class in cls.subresources:
            subresource_class.add_to_router(
                router, f'{base_path}/{{{cls.path_parameter.default}}}/{subresource_class.resource_name}', # pylint: disable=line-too-long
                parent=cls,
                url_params=url_params,
                group_name=group_name,
                base_name=base_name,
                path_parameters=copy.deepcopy(path_parameters)
            )

        # Create the OPTIONS methods. Basically, we need to figure out what
        # the URL parameters are i.e. on subresources there are multiple URL
        # parameters.
        #
        #async def options(request: Request, *args, **kwargs):
        #    view = cls('options')
        #    view.request = request
        #    return await view.dispatch(*args, **kwargs)

        #sig = inspect.signature(options)
        #ann = OrderedDict()
        #ann['request'] = inspect.Parameter(
        #    'request',
        #    inspect.Parameter.POSITIONAL_OR_KEYWORD,
        #    annotation=Request
        #)
        #for name in url_params:
        #    ann[name] = inspect.Parameter(
        #        name,
        #        inspect.Parameter.POSITIONAL_OR_KEYWORD
        #    )
        #options.__signature__ = sig.replace(
        #    parameters=list(ann.values())
        #)
        #options.__annotations__ = ann
        #if has_collection_methods:
        #    router.add_api_route(base_path, options, methods=['OPTIONS'])

        #if has_detail_methods:
        #    ann[cls.path_parameter] = inspect.Parameter(
        #        cls.path_parameter,
        #        inspect.Parameter.POSITIONAL_OR_KEYWORD
        #    )
        #    options.__signature__ = sig.replace(
        #        parameters=list(ann.values())
        #    )
        #    options.__annotations__ = ann
        #    router.add_api_route(f'{base_path}/{{{cls.path_parameter}}}', options, methods=['OPTIONS'])


    @staticmethod
    def _update_signature(view_class, action, handler, protected=False, detail=False, path_parameters=None, singleton=False): # pylint: disable=line-too-long
        # Create an ordered dictionary containing the handlers' signature
        # parameters and add in the following order:
        #
        # 1. The request object
        #
        # This will cause FastAPI to inject the correct dependencies and
        # update the OpenAPI specification properly.
        signature = inspect.signature(handler)
        annotations = OrderedDict()
        annotations['request'] = inspect.Parameter(
            'request',
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Request
        )
        annotations['response'] = inspect.Parameter(
            'response',
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Response
        )

        if detail and path_parameters:
            for param in path_parameters:
                annotations[param.default] = inspect.Parameter(
                    param.default,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param.annotation
                )

        # Update the annotations dictionary with the remaining parameters
        # and create a new call signature. Do that before the other arguments
        # to prevent argument order errors. Remove the 'self' parameter since
        # it confuses FastAPI. Handle variable arguments after any inserted
        # arguments.
        for varname, param in list(signature.parameters.items()):
            if param.kind == inspect.Parameter.VAR_POSITIONAL: # pragma: no cover
                break
            if isinstance(param.default, fastapi.params.Depends):
                continue
            annotations[varname] = param

        # Remove the self parameter (causes incorrect rendering of the UI)
        # and add the variable positional and keyword arguments, if any. This
        # should not happen because request handlers do no accept these kind
        # of arguments, but the error raised by the inspect module if the
        # order is incorrect is quite cryptic.
        for varname, param in list(signature.parameters.items()): # pragma: no cover
            if param.kind != inspect.Parameter.VAR_POSITIONAL\
            and param.kind != inspect.Parameter.VAR_KEYWORD:
                continue
            if isinstance(param.default, fastapi.params.Depends):
                continue
            annotations[varname] = param

        if view_class.require_authentication:
            annotations['bearer'] = inspect.Parameter(
                name='bearer',
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=Depends(HTTPBearer(auto_error=False))
            )

        # Update the signature to hold the new annotations. Remove the self
        # parameter to not confuse FastAPI
        annotations.pop('self', None)
        annotations.pop('args', None)
        annotations.pop('kwargs', None)
        signature = signature.replace(
            parameters=list(annotations.values())
        )

        return signature, annotations

    @staticmethod # pylint: disable=line-too-long
    def _create_annotated_handler(view_class, action, handler, parent, detail, path, path_parameters, logger=None):
        @functools.wraps(handler)
        async def request_handler(
            request: Request,
            response: Response,
            *args, **kwargs
        ):
            """Wrapper function that ensures that the proper dependencies
            are injected when handling an incoming HTTP request.
            """
            view = view_class(action)
            view.request = request
            view.response = response
            view.logger = logger
            view.path_format = path
            return await view.dispatch(*args, **kwargs)

        request_handler.__signature__, request_handler.__annotations__ = (
            view_class._update_signature(view_class, action, handler,
                protected=view_class.require_authentication,
                detail=detail,
                path_parameters=path_parameters,
                singleton=view_class.singleton
            )
        )
        return request_handler

    def get_parsers(self) -> typing.List[IParser]:
        """Return the list of parsers used to deserialize the request body."""
        return self.parsers + self.default_parsers

    def get_permissions(self) -> set:
        """Return the set of permissions that are required to perform the
        operation the :class:`Endpoint` is currently handling.
        """
        return getattr(self.handler, 'permissions', set())

    def set_cookie(self,
        key: str,
        value: str,
        max_age: int = None,
        expires: int = None,
        path: str = None,
        domain: str = None,
        secure: bool = None,
        httponly: bool = False,
        samesite: str = 'lax',
    ) -> None:
        """Sets a cookie on the response."""
        return self.response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite
        )

    async def get_body(self) -> typing.Any:
        """Parse and return the request body."""
        # Do not parse the body for methods that do not commonly use them.
        #
        #   HTTP request bodies are theoretically allowed for all methods
        #   except TRACE, however they are not commonly used except in PUT,
        #   POST and PATCH. Because of this, they may not be supported properly
        #   by some client frameworks, and you should not allow request bodies
        #   for GET, DELETE, TRACE, OPTIONS and HEAD methods.
        #
        # (from OpenStack API Special Interest Group documentation)
        if self.request.method in {"GET", "HEAD", "TRACE", "OPTIONS", "DELETE"}:
            return None
        media_type = self.request.headers.get('Content-Type')
        content_length = self.request.headers.get('Content-Length') or ''
        if not str.isdigit(content_length) or int(content_length) == 0:
            return None
        parser = self.negotiator.select_parser(self.request, self.get_parsers())
        if parser is None:
            raise ParseError
        return await parser.parse(self.request, media_type)

    async def dispatch(self, *args, **kwargs) -> dict:
        """Dispatch the incoming HTTP request to the appropriate request
        handler.
        """
        body = await self.get_body()
        current_user = class_dependency(self.get_principal, 'principal')
        handler = as_dependant(getattr(self, self.action))
        dependant = get_dependant(path=self.path_format, call=handler)
        dependant.dependencies.extend([
            get_parameterless_sub_dependant(
               depends=current_user,
               path=self.path_format
            ),
            get_parameterless_sub_dependant(
                depends=class_dependency(
                    self.authorize,
                    dst='is_authorized',
                    principal=current_user
                ),
                path=self.path_format
            )
        ])
        values, errors, tasks, response, _ =  await solve_dependencies(
            request=self.request,
            dependant=dependant,
            body=body,
            dependency_overrides_provider=None
        )
        if errors:
            raise RequestValidationError(errors, body=None)
        if self.principal is None and self.require_authentication:
            raise BearerAuthenticationRequired
        if not self.is_authorized:
            raise NotAuthorized
        if response:
            if response.status_code is not None:
                self.response.status_code = response.status_code
            if response.headers:
                self.response.headers.update(response.headers)
        result = await dependant.call(
            **await self.preprocess_params(**values)
        )
        return result

    async def preprocess_params(self, **params) -> dict:
        """Hook to modify the parameters passed to a request handler."""
        return params

    async def authorize(self, *args, **kwargs):
        assert hasattr(self, 'principal') # nosec
        return True

    async def get_principal(self,
        request: Request,
        bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        resolver = inject(
            'RequestPrincipalResolver',
            default=RequestPrincipalResolver()
        )
    ) -> IPrincipal:
        if bearer is None:
            if self.require_authentication:
                raise BearerAuthenticationRequired
            return None
        return await resolver.resolve(
            request=request,
            iam=self.iam,
            bearer=bearer.credentials,
            policy=self.trust_policy
        )

    def render_to_response(self, *args, **kwargs) -> Response:
        """Renders a resource to a HTTP response."""
        return self.resource_class.render_to_response(
            self, self.request, *args, **kwargs
        )

    def redirect(self,
        name: str,
        params: dict,
        status_code: int = 303
    ):
        """Create a redirect response to the given named URL with the
        given parameters `params`.
        """
        return RedirectResponse(
            self.reverse(name, **params),
            status_code=status_code
        )

    def reverse(self, name: str, **params) -> str:
        """Reverses the given path relative to the current view."""
        return self.request.url_for(f'{self.qualname}.{name}', **params)

    def get_detail_url(self, *args, **params) -> str:
        """Returns the detail view URL of the endpoint."""
        path_parameter = self.path_parameter.default
        if args:
            dto = args[0]
            params = self._get_path_params_from_resource(dto)
        return self.reverse('retrieve', **params)

    def get_limit(self) -> int:
        """Return the limit for pagination from a request."""
        limit = self._get_int_query_param(self.request.query_params, 'limit', 100)
        return min(limit, self.max_items)

    def get_next_url(self, total: int = None) -> str:
        """Return the next URL for pagination, based on the current offset
        and limit.
        """
        limit = self.get_limit()
        params = {
            **self.request.query_params,
            'offset': self.get_offset() + limit,
            'limit': limit
        }

        return f"{self.reverse('index')}?{urllib.parse.urlencode(params, doseq=False)}"\
            if not (total is not None and params['offset'] >= total) else None

    def get_offset(self) -> int:
        """Return the offset for pagination from a request."""
        return self._get_int_query_param(self.request.query_params, 'offset', 0)

    def get_ancestors(self) -> list:
        """Return the list of ancestors."""
        ancestors = []
        parent = self.parent_class
        while parent:
            ancestors.append(parent)
            parent = parent.parent_class
        return ancestors

    def get_prev_url(self) -> str:
        """Return the previous URL for pagination, based on the current offset
        and limit.
        """
        limit = self.get_limit()
        params = {
            **self.request.query_params,
            'offset': self.get_offset() - limit,
            'limit': limit
        }
        return f"{self.reverse('index')}?{urllib.parse.urlencode(params, doseq=False)}"\
            if params['offset'] >= 0 else None

    def get_resource_links(self, resource) -> dict:
        """Return a dictionary containing the links for a single resource."""
        params = self._get_path_params_from_resource(resource)
        links = {}
        for action in self.actions:
            if not action.detail:
                continue
            if not getattr(action, 'subresource', False):
                links[action.name] = self.reverse(action.name, **params)
            else:
                # For subresources, the default actions are not added
                # separately, but instead the subresource is referenced
                # as a single link.
                links[action.name] = self.reverse('retrieve', **params)\
                    + '/' + action.path
        return links

    def _get_int_query_param(self, params, name, default):
        value = params.get(name) or ''
        return int(value if str.isdigit(value) else default)

    def _get_path_params_from_resource(self, resource) -> dict:
        if hasattr(resource, 'get_path_parameters'):
            params = resource.get_path_parameters()
        elif all([hasattr(resource, x.default) for x in self.path_parameters]):
            params = {
                x.default: getattr(resource, x.default)
                for x in self.path_parameters
            }
        elif isinstance(resource, dict):
            params = {
                x.default: resource[x.default]
                for x in self.path_parameters
            }
        else:
            raise TypeError("Unable to determine path parameters.")
        return params


class PublicResourceEndpointSet(ResourceEndpointSet):
    """A :class:`ResourceEndpointSet` implementation that is public i.e.
    no authentication or authorization is performed.
    """
    require_authentication = False
