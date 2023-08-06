from zeusai_py import exceptions


class IOException(exceptions.ZeusAIException):
    """Base exception for all IO module related exceptions"""
    pass


# Source: https://github.com/python/cpython/blob/3.7/Lib/asyncio/streams.py
class IncompleteReadError(EOFError):
    """
    Incomplete read error. Attributes:
    - partial: read bytes string before the end of stream was reached
    - expected: total number of expected bytes (or None if unknown)
    """
    def __init__(self, partial, expected):
        super().__init__(f'{len(partial)} bytes read on a total of '
                         f'{expected!r} expected bytes')
        self.partial = partial
        self.expected = expected

    def __reduce__(self):
        return type(self), (self.partial, self.expected)
