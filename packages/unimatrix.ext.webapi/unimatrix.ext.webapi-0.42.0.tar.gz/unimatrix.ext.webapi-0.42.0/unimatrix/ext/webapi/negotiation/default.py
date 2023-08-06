"""Declares :class:`DefaultContentNegotiation`."""
from fastapi import Request

from ..parsers import IParser
from ..utils import media_type_matches
from .base import BaseContentNegotiation


class DefaultContentNegotiation(BaseContentNegotiation):

    def select_parser(self, request: Request, parsers: list) -> IParser:
        """Given a list of parsers and a media type, return the appropriate
        parser to handle the incoming request.
        """
        content_type = request.headers.get('Content-Type') or ''
        for parser in parsers:
            if media_type_matches(parser.media_type, content_type):
                break
        else:
            parser = None
        return parser()
