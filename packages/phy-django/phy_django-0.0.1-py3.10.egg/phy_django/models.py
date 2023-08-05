import typing

import django.contrib
import django.contrib.auth
import django.core.exceptions
import django.db.models
import django.db.models.fields.files
import django.utils.timezone
from django.db.models import *
from django.db.transaction import atomic
from django.utils.functional import classproperty
from djmoney.models.fields import MoneyField

__keep = (atomic,)

if typing.TYPE_CHECKING:
    pass

user_model = django.contrib.auth.get_user_model()


class ForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('on_delete', PROTECT)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class FloatField(FloatField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        super().__init__(*args, **kwargs)


class FieldFile(django.db.models.fields.files.FieldFile):
    pass


class FileField(FileField):
    attr_class = FieldFile

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        super().__init__(*args, **kwargs)


class SmallIntegerField(SmallIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        super().__init__(*args, **kwargs)


class ShortStringField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('default', '')
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class LongStringField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('default', '')
        super().__init__(*args, **kwargs)


class MoneyField(MoneyField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', 0)
        kwargs.setdefault('max_digits', 14)
        kwargs.setdefault('decimal_places', 2)
        kwargs.setdefault('default_currency', 'CNY')
        super().__init__(*args, **kwargs)


class UserField(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', '用户')
        kwargs.setdefault('to', django.contrib.auth.get_user_model())
        kwargs.setdefault('on_delete', PROTECT)
        kwargs.setdefault('null', True)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class TextField(TextField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '')
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)


class BooleanField(BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', False)
        super().__init__(*args, **kwargs)


DEFAULT_DATETIME = django.utils.timezone.datetime(1970, 1, 1, tzinfo=django.utils.timezone.get_current_timezone())


class DateTimeField(DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', DEFAULT_DATETIME)
        super().__init__(*args, **kwargs)


class DateField(DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', DEFAULT_DATETIME.date())
        super().__init__(*args, **kwargs)


class DatetimeMixin(Model):
    class Meta:
        abstract = True

    created_datetime = django.db.models.DateTimeField(
        verbose_name='数据库入库时间', auto_now_add=True,
    )
    updated_datetime = django.db.models.DateTimeField(
        verbose_name='数据库更新时间', auto_now=True,
    )


class Model(DatetimeMixin, Model):
    class Meta:
        abstract = True
        verbose_name = '未定义模型名称'

        # noinspection PyMethodParameters
        @django.utils.functional.classproperty
        def verbose_name_plural(cls):
            return cls.verbose_name


class _MappableIntegerChoiceMeta(django.db.models.enums.ChoicesMeta):
    # noinspection PyMethodParameters
    def __new__(mcs, classname, bases, classdict, **kwds):
        has_meta = 'Meta' in classdict
        if has_meta:
            meta_class = classdict.pop('Meta')
            # noinspection PyProtectedMember
            classdict._member_names.remove('Meta')
        else:
            meta_class = None
        result = super().__new__(mcs, classname, bases, classdict, **kwds)
        if has_meta:
            result.Meta = meta_class
        return result


class MappableIntegerChoice(IntegerChoices, metaclass=_MappableIntegerChoiceMeta):
    """
    可以直接生成 Django 的 IntegerChoiceField ，包含选项。
    同时，支持设置默认值，支持定义值到Enum的映射以用于解析。
    """

    class Meta:
        default_value = 1
        mapping: dict[str, typing.Any] = {}

    @classmethod
    def parse(cls, value: str):
        return cls(cls.Meta.mapping.get(value, cls.Meta.default_value))

    @classmethod
    def as_field(cls, verbose_name: str = '', help_text='', negative=False, default=None):
        klass = SmallIntegerField if negative else PositiveSmallIntegerField
        default = cls.Meta.default_value if default is None else default
        return klass(verbose_name=verbose_name, choices=cls.choices, default=default, help_text=help_text)


class IntegerStringField(PositiveBigIntegerField):
    def to_python(self, value):
        if isinstance(value, int):
            return String.int_to_string(value)
        elif isinstance(value, str) or value is None:
            return value
        else:
            raise django.core.exceptions.ValidationError(f'Unknown type: {type(value)} of "{value}')

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def value_to_string(self, obj):
        return self.to_python(obj)

    def get_prep_value(self, value):
        return String.string_to_int(value)

    def get_db_prep_value(self, value: str, connection, prepared=False):
        return String.string_to_int(value)


class JSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', dict)
        super().__init__(*args, **kwargs)


class String(Model):
    class Meta:
        indexes = (
            Index(fields=['value']),
        )

    value = CharField(
        max_length=255, unique=True,
    )

    def __str__(self):
        return self.value

    __default: int = 1
    __string_to_int_cache: dict[str, int] = {}
    __int_to_string_cache: dict[int, str] = {}

    @classmethod
    def __init_cache(cls):
        objs = [(o.id, o.value) for o in cls.objects.all()]
        cls.__string_to_int_cache = {value: pk for pk, value in objs}
        cls.__int_to_string_cache = {pk: value for pk, value in objs}

    @classmethod
    def string_to_int(cls, value: typing.Optional[str]) -> int:
        # 字符串转整型的过程是一个写入的过程，从缓存中读取编号，或者写入编号
        if not cls.__string_to_int_cache:
            cls.__init_cache()
        if value is None:
            return cls.__default
        if value in cls.__string_to_int_cache:
            return cls.__string_to_int_cache[value]
        pk = cls.objects.get_or_create(value=value)[0].id
        cls.__string_to_int_cache[value] = pk
        return pk

    @classmethod
    def int_to_string(cls, value: typing.Optional[int]) -> str:
        # 整型转字符串的过程是一个读取的过程，从数据库中查询字符串的编号所对应的值
        if not cls.__int_to_string_cache:
            cls.__init_cache()
        return cls.__int_to_string_cache.get(value if value else cls.__default)


class Configuration(Model):
    class Meta(Model.Meta):
        verbose_name = '配置'
        abstract = False

    user = UserField()
    key = ShortStringField(verbose_name='键')
    value = JSONField(verbose_name='值')

    @staticmethod
    def get(key: str, user=None):
        obj, created = Configuration.objects.get_or_create(key=key, user=user)
        return obj.value

    @staticmethod
    def set(key: str, value: dict, user=None):
        obj, created = Configuration.objects.get_or_create(key=key, user=user)
        obj.value = value
        obj.save()
