"""
WSGI config for aplikasi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplikasi.settings')

# application = get_wsgi_application()

settings_module = 'aplikasi.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'aplikasi.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
