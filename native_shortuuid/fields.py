import uuid

import django.db.models
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

import rest_framework.serializers
import shortuuid


def convert_uuid_to_uuid_v2(uuid_or_shortuuid22):
    if isinstance(uuid_or_shortuuid22, uuid.UUID):
        shortuuid22 = shortuuid.encode(uuid_or_shortuuid22)
    else:
        shortuuid22 = uuid_or_shortuuid22

    if len(shortuuid22) == 22:
        shortuuid20 = shortuuid22[2:]
    elif len(shortuuid22) == 20:
        shortuuid20 = shortuuid22
    else:
        raise ValueError(f'Invalid ShortUUID {shortuuid22}')

    return shortuuid.decode(shortuuid20)


def uuid4_12bits_masked():
    random_uuid = uuid.uuid4()
    # Convert the UUID to its 128-bit integer representation
    int_representation = random_uuid.int
    bitmask = (1 << 116) - 1
    modified_int = int_representation & bitmask
    # Convert the modified integer back to a UUID
    return uuid.UUID(int=modified_int)


def short_uuid4_20():
    return shortuuid.encode(uuid4_12bits_masked(), pad_length=20)


def short_uuid4():
    return shortuuid.encode(uuid.uuid4())


def decode(value):
    """Decode the value from ShortUUID to UUID.

    Raises ValueError when the value is not valid.
    """
    if not isinstance(value, str) or len(value) not in (20, 22, ):
        raise ValueError('Badly formed ShortUUID')
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


class NativeShortUUID20FormField(NativeShortUUIDFormField):
    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None

        try:
            decode(value)
        except ValueError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')

        if len(value) == 22:
            # Always trim the first 2 chars of a 22-chars shortuuid
            value = value[2:]

        return value


class NativeShortUUIDSerializerField(rest_framework.serializers.CharField):
    default_error_messages = {
        'invalid': _('Must be a valid short UUID.'),
    }

    def __init__(self, **kwargs):
        kwargs['min_length'] = 20
        kwargs['max_length'] = 22
        kwargs['trim_whitespace'] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # check that data is a valid shortuuid
        try:
            decode(data)
        except Exception:
            self.fail('invalid', value=data)
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, uuid.UUID):
            return shortuuid.encode(value)
        return str(value)


class NativeShortUUID20SerializerField(rest_framework.serializers.CharField):
    default_error_messages = {
        'invalid': _('Must be a valid short UUID.'),
    }

    def __init__(self, **kwargs):
        kwargs['min_length'] = 20
        kwargs['max_length'] = 22
        kwargs['trim_whitespace'] = True
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        # check that data is a valid shortuuid
        try:
            decode(data)
        except Exception:
            self.fail('invalid', value=data)

        if len(data) == 22:
            data = data[2:]

        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, uuid.UUID):
            value = shortuuid.encode(value, pad_length=20)
        if len(value) == 22:
            value = value[2:]
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


class NativeShortUUID20Field(django.db.models.UUIDField):
    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid ShortUUID.'),
    }

    def __init__(self, verbose_name=None, **kwargs):
        self.default_value = kwargs.get('default', None)
        if self.default_value is uuid4_12bits_masked:
            kwargs['default'] = short_uuid4_20
        super().__init__(verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.default_value is uuid4_12bits_masked:
            kwargs['default'] = uuid4_12bits_masked
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        shortuuid_value = shortuuid.encode(value, pad_length=20)
        if len(shortuuid_value) > 20:
            # If the resulted shortuuid did not fit in 20 chars,
            # then this is an old uuid which should result in 22 chars instead.
            shortuuid_value = shortuuid.encode(value, pad_length=22)
        return shortuuid_value

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
            'form_class': NativeShortUUID20FormField,
            **kwargs,
        })
