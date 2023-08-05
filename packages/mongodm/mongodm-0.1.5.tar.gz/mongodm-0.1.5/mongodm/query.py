from typing import Any

from .utils import processing_kwargs


class Q(dict):
    """Query object"""

    @processing_kwargs
    def __init__(self, **kwargs: Any) -> None:
        self.update(kwargs)
