from __future__ import absolute_import

from . import validation
from .admin import NativeUUID20SearchMixin
from .admin import NativeUUIDSearchMixin
from .fields import NativeShortUUID20Field
from .fields import NativeShortUUID20FormField
from .fields import NativeShortUUIDField
from .fields import NativeShortUUIDFormField
from .fields import convert_uuid_to_uuid_v2
from .fields import decode
from .fields import short_uuid4_20
from .fields import uuid4_12bits_masked

try:
    from importlib.metadata import version
    VERSION = version('django-nativeshortuuidfield')
except Exception:
    # Fallback for Python < 3.8 or if package not installed
    try:
        import pkg_resources
        VERSION = pkg_resources.get_distribution('django-nativeshortuuidfield').version
    except Exception:
        VERSION = 'unknown'
