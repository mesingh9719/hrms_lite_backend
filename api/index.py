import os

# Use production settings on Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_lite.settings.production')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
