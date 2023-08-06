"""Declares :class:`BaseParser`."""
import abc


class BaseParser(metaclass=abc.ABCMeta):
    """All parsers should extend `BaseParser`, specifying a `media_type`
    attribute, and overriding the `.parse()` method.
    """
    media_type: str = abc.abstractproperty()

    async def parse(self, stream, media_type: str = None, parser_context=None):
        """ Given a stream to read from, return the parsed representation.
        Should return parsed data, or a `DataAndFiles` object consisting of the
        parsed data and files.
        """
        raise NotImplementedError(".parse() must be overridden.")
