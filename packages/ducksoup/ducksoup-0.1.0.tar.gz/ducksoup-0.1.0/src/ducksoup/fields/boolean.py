from ..field import Field


class Boolean(Field[bool, bool]):

    def __init__(self, **kwargs):
        """
        :param kwargs: **kwargs for Field.__init__()
        """
        super().__init__(cls=bool, **kwargs)
