from __future__ import absolute_import

from . import validation
from .admin import NativeUUIDSearchMixin
from .fields import NativeShortUUIDField
from .fields import NativeShortUUIDFormField
from .fields import decode

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('django-nativeshortuuidfield').version
except Exception:
    VERSION = 'unknown'
