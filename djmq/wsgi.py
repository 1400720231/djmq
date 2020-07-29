# django原生配置wsgi

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djmq.settings")
application = get_wsgi_application()
