
from settings.production import *  # noqa

# import local settings
try:
    from settings.development import *  # noqa
except ImportError:
    pass
