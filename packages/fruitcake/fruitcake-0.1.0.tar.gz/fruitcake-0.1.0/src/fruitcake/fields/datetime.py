from ..field import Field


class DateTime(Field[int, int]):

    def __init__(self, timezone_aware: bool = True, **kwargs):
        """
        :param kwargs: **kwargs for Field.__init__()
        """
        super().__init__(cls=int, **kwargs)
        # super().__init__(cls=int, default=int, **kwargs)
