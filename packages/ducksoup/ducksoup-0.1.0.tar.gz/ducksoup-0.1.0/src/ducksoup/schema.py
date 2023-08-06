from inspect import getmembers
from functools import cached_property, lru_cache
from typing import (
    Iterable, Dict as Dict_, Optional, Any, Tuple,
    Callable, Generic, Protocol, Type, Union,
    NamedTuple)

from .fields import Dict
from .field import Field, TObject
from .context import Context, default_context


# -- Types -------------------------------------------------------------------


# Type of serialized schema
from .validation import collect_validation_errors, ValidationError

TSchema = Dict_[str, Any]

# TODO
TFactory = Callable[[Context, TSchema], Any]


class ObjectFactory(Protocol):
    def __call__(self, **kwargs: Any) -> TObject: ...


# -- Schema ------------------------------------------------------------------


# class Schema(Dict):  # TODO
class Schema(Dict, Generic[TObject]):
    """
    TODO
    """

    def __init__(
            self,
            factory: Optional[Union[ObjectFactory, Type[TObject]]] = None,
            only: Optional[Iterable[str]] = None,
            strict: bool = True,
            **kwargs,
    ):
        """
        :param factory:
        :param strict:
        :param only:
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.factory = factory
        self.strict = strict
        self.only = only or ()

    @cached_property
    def fields(self) -> 'FieldContainer':
        """
        :return:
        """
        return FieldContainer(self)

    def cast(self, value: Any, context: Context) -> Any:
        return value

    def serialize(
            self,
            obj: Any,
            context: Context = default_context,
    ) -> TSchema:
        """
        :param obj:
        :param context:
        :return:
        """

        # Schema as dict, where key = field.key, and value is object
        schema_dict = {}

        with collect_validation_errors() as errors:

            for field in self.fields.serializable:
                # actual_key = field.key if field.key is not None else name
                # actual_attr = field.attr if field.attr is not None else name
                try:
                    if hasattr(obj, field.attr):
                        field_value = getattr(obj, field.attr)
                    else:
                        field_value = field.default_value
                except TypeError as e:
                    j = 2
                    # if self.strict and field.required:
                    # raise ValidationError('')

                if field_value is None and not context.include_none:
                    continue

                try:
                    schema_dict[field.key] = field.serialize(
                        obj=field_value,
                        context=context,
                    )
                except field.ValidationError as e:
                    errors.add(field.key, e)

        return schema_dict

    def deserialize(
            self,
            data: Optional[Dict_[str, Any]],
            context: Context = default_context,
    ) -> TObject:
        """
        :param data:
        :param context:
        :return:
        """
        if data is None:
            return None

        # Deserialize and validate using super class
        dict_data = super().deserialize(data, context)

        # Kwargs for object constructor, where key is field 'attr' and
        # value is the deserialized and validated value.
        kwargs = {}

        with collect_validation_errors() as errors:

            for field in self.fields.deserializable:
                if field.key in dict_data:
                    value = dict_data[field.key]
                elif self.strict:
                    errors.add(field.key, 'This key is required')
                    continue
                else:
                    value = field.default_value

                try:
                    kwargs[field.attr] = field.deserialize(
                        data=value,
                        context=context,
                    )
                except field.ValidationError as e:
                    errors.add(field.key, e)

            if self.strict:
                # TODO
                pass

        # with collect_validation_errors() as errors:
        #     for field_name, field in self.fields.deserializable:
        #         actual_key = field.key if field.key is not None else field_name  # noqa: E501
        #         actual_attr = field.attr if field.attr is not None else field_name  # noqa: E501
        #
        #         if actual_key in data:
        #             value = data[actual_key]
        #         elif self.strict:
        #             errors.add(actual_key, 'This key is required')
        #             continue
        #         else:
        #             value = field.default_value
        #
        #         try:
        #             obj_kwargs[actual_attr] = field.deserialize(value, context)
        #         except field.ValidationError as e:
        #             errors.add(actual_key, e)
        #
        # # Raise ValidationError, if any
        # if errors:
        #     raise errors

        # Instantiate object, passing **kwargs
        if self.factory is not None:
            return self.factory(**kwargs)
        else:
            return context.default_factory(**kwargs)


# -- Transformations ---------------------------------------------------------  # TODO


class FieldProxy(NamedTuple):
    field: Field
    name: str

    def __getattr__(self, item):
        return getattr(self.field, item)

    @property
    @lru_cache
    def key(self) -> str:
        return self.field.key if self.field.key is not None else self.name

    @property
    @lru_cache
    def attr(self) -> str:
        return self.field.attr if self.field.attr is not None else self.name


class FieldContainer(object):
    """
    TODO
    """
    def __init__(self, schema: Schema):
        """
        :param schema:
        """
        self.schema = schema

    def __iter__(self) -> Iterable[FieldProxy]:
        """
        :return:
        """
        return (
            FieldProxy(field=obj, name=name)
            for name, obj in getmembers(self.schema)
            if isinstance(obj, Field)
            and self.should_include(name)
        )

    @cached_property
    def serializable(self) -> Tuple[FieldProxy, ...]:
        """
        :return:
        """
        return tuple(f for f in self if f.serializable)

    @cached_property
    def deserializable(self) -> Tuple[FieldProxy, ...]:
        """
        :return:
        """
        return tuple(f for f in self if f.deserializable)

    def should_include(self, field_name: str) -> bool:
        """
        :return:
        """
        return not self.schema.only or field_name in self.schema.only
