from typing import Any

from ..field import Field
from ..context import Context


class Dict(Field[dict, dict]):

    def __init__(self, **kwargs):
        """
        :param kwargs: **kwargs for Field.__init__()
        """
        kwargs.setdefault('default', dict)
        super().__init__(cls=dict, **kwargs)

    def cast(self, value: Any, context: Context) -> Field[dict, dict]:
        if not isinstance(value, dict):
            raise self.ValidationError(f'Can not cast to {self.cls}: {value}')
        return self.cls(value)
