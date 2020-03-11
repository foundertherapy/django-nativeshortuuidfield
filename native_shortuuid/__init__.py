from __future__  import absolute_import

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('django-nativeshortuuidfield').version
except Exception:
    VERSION = 'unknown'

from .fields import NativeShortUUIDField
from .fields import NativeShortUUIDFormField
