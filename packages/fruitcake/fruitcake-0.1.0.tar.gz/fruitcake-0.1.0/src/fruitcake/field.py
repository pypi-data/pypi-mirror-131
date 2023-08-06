from typing import List, Optional, Type, TypeVar, Generic, Any, Union, \
    Callable

from .context import Context, default_context
from .validation import TValidator, ValidationError


# -- Types -------------------------------------------------------------------


# Type of deserialized (Python) objects
TObject = TypeVar('TObject')

# Type of serialized data
TSerialized = TypeVar('TSerialized')


# -- Field -------------------------------------------------------------------


class Field(Generic[TObject, TSerialized]):
    """
    TODO
    """

    # Shortcut
    ValidationError = ValidationError

    def __init__(
            self,
            cls: Type[TObject],
            required: bool = True,
            nullable: bool = False,
            cast: bool = True,
            key: Optional[str] = None,
            attr: Optional[str] = None,
            default: Optional[Union[TObject, Callable[[], TObject]]] = None,
            validators: Optional[List[TValidator]] = None,
            serializable: bool = True,
            deserializable: bool = True,
            name: Optional[str] = None,
            description: Optional[str] = None,
    ):
        """
        :param cls: The class to instantiate when deserializing data into
            objects. Will receive.
        :param required: Whether this field is required (can not be None)
        :param nullable:
        :param cast: Allow casting of value when deserializing.
            Otherwise, not-exact datatypes causes ValidationError.
        :param key:
        :param attr:
        :param default: Default value, or a callable.
        :param validators:
        :param serializable:
        :param deserializable:
        :param name:
        :param description:
        """
        self.cls = cls
        self.required = required
        # self.nullable = nullable
        # self.cast = cast
        self.key = key
        self.attr = attr
        self.default = default
        self.validators = validators or []
        self.serializable = serializable
        self.deserializable = deserializable
        self.name = name
        self.description = description

    @property
    def default_value(self) -> Any:
        """
        :returns: Field default value, including None
        """
        if callable(self.default):
            return self.default()
        else:
            return self.default

    def cast(self, value: Any, context: Context) -> TObject:
        return self.cls(value)
        # try:
        #     data = self.cast(data, context)
        # except (ValueError, TypeError):
        #     raise ValidationError(f'Can not cast to {self.cls}: {data}')

    def normalize(self, value: Any, context: Context) -> TObject:
        return value

    # ------------------------------------------------------------------------

    def serialize(
            self,
            obj: TObject,
            context: Context = default_context,
    ) -> TSerialized:
        """
        :param obj:
        :param context:
        :return:
        """
        if self.serializable is not True:
            raise RuntimeError('Serializing un-serializable field')

        if self.required:
            if obj is None:
                raise ValidationError('Field can not be null')

        if obj is not None and not isinstance(obj, self.cls):
            try:
                obj = self.cast(obj, context)
            except (ValueError, TypeError):
                raise ValidationError(f'Can not cast to {self.cls}: {obj}')

        return obj

    def deserialize(
            self,
            data: TSerialized,
            context: Context = default_context,
    ) -> TObject:
        """
        :param data:
        :param context:
        :return:
        """
        if self.serializable is not True:
            raise RuntimeError('Serializing un-serializable field')

        if self.required:
            if data is None:
                raise ValidationError('Field can not be null')

        if data is not None and not isinstance(data, self.cls):
            # data = self.cast(data, context)
            try:
                data = self.cast(data, context)
            except (ValueError, TypeError):
                raise ValidationError(f'Can not cast to {self.cls}: {data}')

        return data

        # if self.deserializable is not True:
        #     raise RuntimeError('Deserializing un-deserializable field')
        #
        # return self.deserializer(
        #     value=data,
        #     context=context,
        # )


# class SimpleField(Field[TObject, TSerialized]):
#
#     def __init__(self, cls: Type[TObject], **kwargs):
#         """
#         :param cls: The class to instantiate when deserializing data into
#             objects. Will receive.
#         :param kwargs: **kwargs for Field.__init__()
#         """
#         super().__init__(**kwargs)
#         self.cls = cls
#
#     # @cached_property
#     @property
#     def serializer(self) -> Pipeline:
#         """
#         :returns:
#         """
#         l = 2
#         pipe = [Cast(self.cls)]
#         pipe.extend(self.validators)
#
#         j = 2
#
#         return Pipeline(*pipe)
#
#     # @cached_property
#     @property
#     def deserializer(self) -> Pipeline:
#         """
#         :returns:
#         """
#         pipe = [Cast(self.cls)]
#         pipe.extend(self.validators)
#
#         j = 2
#
#         return Pipeline(*pipe)


# -- Transformations ---------------------------------------------------------


class SetDefault(object):
    def __init__(self, default: Any):
        self.default = default

    def __call__(self, value: Any, context: Context) -> Any:
        if value is None:
            value = self.default
        return value


# class


# class FieldOLD(Generic[TObject, TSerialized]):
#     """
#     TODO
#     """
#
#     @classmethod
#     def create(cls, context: Context, data: TSerialized) -> TObject:
#         """
#         :param context:
#         :param data:
#         :returns:
#         """
#         return cls(data)
#
#     def __init__(
#             self,
#             cls: Optional[Type[TObject]] = None,
#             required: bool = True,
#             nullable: bool = False,
#             cast: bool = True,
#             key: Optional[str] = None,
#             attr: Optional[str] = None,
#             default: Optional[TObject] = None,
#             validators: Optional[List[TValidator]] = None,
#             serializable: bool = True,
#             deserializable: bool = True,
#             description: Optional[str] = None,
#     ):
#         """
#         :param cls: The class to instantiate when deserializing data into
#             objects. Will receive.
#         :param required:
#         :param nullable:
#         :param cast: Allow casting of value when deserializing.
#             Otherwise, not-exact datatypes causes ValidationError.
#         :param key:
#         :param attr:
#         :param default:
#         :param validators:
#         :param serializable:
#         :param deserializable:
#         :param description:
#         """
#         self.cls = cls
#         self.required = required
#         self.nullable = nullable
#         self.cast = cast
#         self.key = key
#         self.attr = attr
#         self.default = default
#         self.validators = validators or []
#         self.serializable = serializable
#         self.deserializable = deserializable
#         self.description = description
#
#     def validate(
#             self,
#             data: TSerialized,
#             context: Context,
#     ):
#         """
#         :param value:
#         :param context:
#         :return:
#         """
#         if data is None and not self.nullable:
#             raise ValidationError('Field is not nullable')
#
#         # if not isinstance(data)
#         # if self.cast:
#         #     try:
#
#         # cls = self.factory or context.default_factory
#         #
#         # try:
#         #     value = cls(value)
#         # except ValueError:
#         #     raise ValidationError('Invalid type')
#         # except:
#         #     j = 2
#         #     raise
#
#         for validator in self.validators:
#             validator(data)
#
#     @abstractmethod
#     def serialize(
#             self,
#             obj: TObject,
#             context: Context,
#     ) -> TSerialized:
#         """
#         :param obj:
#         :param context:
#         :return:
#         """
#         raise NotImplementedError
#
#     def serialize_many(
#             self,
#             obj_list: Iterable[TObject],
#             context: Context,
#     ) -> List[TSerialized]:
#         """
#         :param obj_list:
#         :param context:
#         :return:
#         """
#         values = []
#         # errors = ValidationError()
#
#         with CatchValidationErrors() as errors:
#             for i, obj in enumerate(obj_list):
#                 try:
#                     value = self.serialize(
#                         obj=obj,
#                         context=context,
#                     )
#                 except ValidationError as e:
#                     errors.add(i, e)
#                 else:
#                     values.append(value)
#
#         # if errors:
#         #     raise errors
#
#         return values
#
#     @abstractmethod
#     def deserialize(
#             self,
#             data: TSerialized,
#             context: Context,
#     ) -> TObject:
#         """
#         :param data:
#         :param context:
#         :return:
#         """
#         raise NotImplementedError
#
#     def deserialize_many(
#             self,
#             data_list: Iterable[TSerialized],
#             context: Context,
#     ) -> List[TObject]:
#         """
#         :param data_list:
#         :param context:
#         :return:
#         """
#         raise NotImplementedError
#
#     # def cast(self, context: Context, data: TData) -> TObject:
#     #     """
#     #     Cast
#     #     :param context:
#     #     :param data:
#     #     :return:
#     #     """
#     #     return self.cls(data)
