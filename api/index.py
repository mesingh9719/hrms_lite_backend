import os
import sys

# Use production settings on Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_lite.settings.production')

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
