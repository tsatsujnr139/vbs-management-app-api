
from core.settings.production import *  # noqa

# import local settings
try:
    from core.settings.development import *  # noqa
except ImportError:
    pass
