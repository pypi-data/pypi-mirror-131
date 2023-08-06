from typing import List as _List

from ..field import Field
from ..context import Context


class List(Field[_List, _List]):

    def __init__(self, **kwargs):
        super().__init__(cls=int, **kwargs)

    def serialize(
            self,
            obj: list,
            context: Context,
    ) -> list:
        """
        :param obj:
        :param context:
        :return:
        """
        return list(obj)

    def deserialize(
            self,
            data: list,
            context: Context,
    ) -> list:
        """
        :param data:
        :param context:
        :return:
        """
        return list(data)
