from django.urls import register_converter

import shortuuid


class ShortUUIDConverter:
    regex = '[{}]{{22}}'.format(shortuuid.get_alphabet())

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(ShortUUIDConverter, 'shortuuid')
