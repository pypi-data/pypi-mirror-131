from ..field import Field


class Integer(Field[int, int]):

    def __init__(self, **kwargs):
        """
        :param kwargs: **kwargs for Field.__init__()
        """
        super().__init__(cls=int, **kwargs)
        # super().__init__(cls=int, default=int, **kwargs)
