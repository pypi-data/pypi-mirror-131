"""Declares :class:`BaseContentNegotiation`."""
import fastapi


class BaseContentNegotiation:

    def select_parser(self, request: fastapi.Request, parsers: list):
        raise NotImplementedError

    def select_renderer(self, request, renderers, format_suffix=None):
        raise NotImplementedError
