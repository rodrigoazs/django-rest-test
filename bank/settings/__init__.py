import os
from .base import *

if os.environ.get('DJANGO_DEVELOPMENT'):
    from .dev import *
else:
    from .prod import *