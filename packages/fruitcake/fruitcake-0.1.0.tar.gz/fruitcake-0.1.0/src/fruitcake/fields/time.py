from datetime import time

from ..context import Context
from ..field import Field
from .string import String


# class Time(String):
#
#     def __init__(
#             self,
#             timezone_aware: bool = None,
#             **kwargs,
#     ):
#         """
#         :param kwargs: **kwargs for Field.__init__()
#         """
#         super().__init__(cls=time, **kwargs)
#
#     def deserialize(
#             self,
#             data: str,
#             context: Context = default_context,
#     ) -> time:

