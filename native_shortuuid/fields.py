import uuid

import django.db.models
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

import rest_framework.serializers
import shortuuid


def short_uuid4():
    return shortuuid.encode(uuid.uuid4())


def decode(value):
    """Decode the value from ShortUUID to UUID.

    Raises ValueError when the value is not valid.
    """
    if not isinstance(value, str) or len(value) != 22:
        raise ValueError('badly formed ShortUUID')
    return shortuuid.decode(value)


class NativeShortUUIDFormField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid ShortUUID.'),
    }

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        try:
            decode(value)
        except ValueError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value


class NativeShortUUIDSerializerField(rest_framework.serializers.CharField):
    default_error_messages = {
        'invalid': _('Must be a valid short UUID.'),
    }

    def __init__(self, **kwargs):
        kwargs['min_length'] = kwargs['max_length'] = 22
        kwargs['trim_whitespace'] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # check that data is a valid shortuuid
        try:
            shortuuid.decode(data)
        except Exception:
            self.fail('invalid', value=data)
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, uuid.UUID):
            return shortuuid.encode(value)
        return str(value)


class NativeShortUUIDField(django.db.models.UUIDField):
    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid ShortUUID.'),
    }

    def __init__(self, verbose_name=None, **kwargs):
        self.default_value = kwargs.get('default', None)
        if self.default_value is uuid.uuid4:
            kwargs['default'] = short_uuid4
        super().__init__(verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.default_value is uuid.uuid4:
            kwargs['default'] = uuid.uuid4
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return shortuuid.encode(value)

    def to_python(self, value):
        if value is not None and not isinstance(value, uuid.UUID):
            try:
                return decode(value)
            except ValueError:
                raise ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': NativeShortUUIDFormField,
            **kwargs,
        })
