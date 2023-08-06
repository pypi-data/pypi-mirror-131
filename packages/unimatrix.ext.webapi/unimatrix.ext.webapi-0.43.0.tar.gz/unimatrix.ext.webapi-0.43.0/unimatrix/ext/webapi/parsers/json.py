"""Declares :class:`JSONParser`."""
import json

import fastapi

from ..exceptions import ParseError
from .base import BaseParser


class JSONParser(BaseParser):
    """
    Parses JSON-serialized data.
    """
    media_type: str = 'application/json'
    strict: bool    = True
    charset: str    = "utf-8"

    async def parse(self,
        request: fastapi.Request,
        media_type: str = None,
        parser_context: dict = None
    ) -> dict:
        """Parses the incoming bytestream as JSON and returns the resulting
        data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', self.charset)
        try:
            return json.loads(bytes.decode(await request.body(), encoding))
        except ValueError:
            raise ParseError
