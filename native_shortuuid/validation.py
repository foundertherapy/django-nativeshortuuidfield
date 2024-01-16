from django.urls import register_converter

import shortuuid


def validate_shortuuid(val):
    if not isinstance(val, str):
        raise ValueError('Must be of type str')
    if len(val) not in (20, 22, ):
        raise ValueError(f'Incorrect length: {len(val)}')
    shortuuid.decode(val)


class ShortUUIDConverter:
    regex = '[{}]{{20}}([{}]{{2}})?'.format(shortuuid.get_alphabet(), shortuuid.get_alphabet())

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class ShortUUID20Converter:
    regex = '[{}]{{20}}([{}]{{2}})?'.format(shortuuid.get_alphabet(), shortuuid.get_alphabet())

    def to_python(self, value):
        if len(value) == 22:
            value = value[2:]
        return value

    def to_url(self, value):
        if len(value) == 22:
            value = value[2:]
        return value


register_converter(ShortUUIDConverter, 'shortuuid')
register_converter(ShortUUID20Converter, 'shortuuid20')
