# from abc import abstractmethod
# from typing import Any, Type, Iterable, Callable, Generic
#
# from .context import Context
# from .validation import ValidationError
#
#
# TAction = Callable[[Any, Context], Iterable[Any]]
#
# TSerialize = Callable[[Any, Context], Iterable[Any]]
#
#
# def b(a: int, b: Context):
#     return (i for i in range(1))
#
#
# def a() -> Iterable[int]:
#     return b(1, Context())
#
#
# # class Action(Generic[TObject]):
# #
# #     @abstractmethod
# #     def __call__(self, value: Any, context: Context) -> Any:
# #         """
# #         TODO
# #         """
# #         raise NotImplementedError
#
#
# # class Transformation(TTransformation):
# #     """
# #     TODO
# #     """
# #     def __call__(self, value: Any, context: Context) -> Any:
# #         """
# #         TODO
# #         """
# #         return self.apply(value, context)
# #
# #     @abstractmethod
# #     def apply(self, value: Any, context: Context) -> Any:
# #         """
# #         :param value:
# #         :param context:
# #         :returns:
# #         """
# #         raise NotImplementedError
#
#
# class RequireType(TAction):
#     def __init__(self, type: Type[Any], nullable: bool = False):
#         self.type = type
#         self.nullable = nullable
#
#     def __call__(self, value: Any, context: Context) -> Any:
#         """
#         TODO
#         """
#         if not isinstance(value, self.type):
#             raise ValidationError()
#
#
# class Cast(TAction):
#     def __init__(self, type: Type[Any]):
#         self.type = type
#
#     def __call__(self, value: Any, context: Context) -> Any:
#         """
#         TODO
#         """
#         return self.type(value)
#         # raise Exception('asd!')
#         # if not isinstance(value, self.type):
#         # return self.apply(value, context)
#
#     # def __init__(self, type: Type[Any]):
#     #     self.type = type
#     # def apply(self, value: Any, context: Context) -> Any:
#     #     return value
#
#
# class Default(TAction):
#     def __init__(self, default: Any):
#         self.default = default
#     def __call__(self, value: Any, context: Context) -> Any:
#         """
#         TODO
#         """
#         raise Exception('asd!')
#
#
# class Pipeline(TAction):
#     """
#     TODO
#     """
#     def __init__(self, *actions: TAction):
#         """
#         :param actions:
#         """
#         self.actions = actions
#
#     def __call__(self, value: Any, context: Context) -> Any:
#         """
#         Left-fold value through all transformations.
#
#         :param value:
#         :param context:
#         :returns: Transformed value
#         """
#         for action in self.actions:
#             value_transformed = action(value, context)
#             if value_transformed is not None:
#                 value = value_transformed
#
#         return value
#
#
# def pipe(*actions: TAction) -> Pipeline:
#     return Pipeline(*actions)
