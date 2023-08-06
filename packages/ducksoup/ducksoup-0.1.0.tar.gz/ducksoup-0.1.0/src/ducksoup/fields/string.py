from typing import Optional, Any

from ..field import Field
from ..context import Context


class String(Field[str, str]):

    def __init__(self, **kwargs):
        super().__init__(cls=str, **kwargs)

    def cast(self, value: Any, context: Context) -> str:
        if isinstance(value, bytes):
            return value.decode('utf8')
        return super().cast(value, context)
