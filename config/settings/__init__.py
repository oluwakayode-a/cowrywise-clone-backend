import os
from .base import *

if os.getenv('ENVIRONMENT') == 'PRODUCTION':
    from .production import *
elif os.getenv('ENVIRONMENT') == 'DEVELOPMENT':
    from .development import *