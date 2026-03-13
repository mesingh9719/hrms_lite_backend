"""WSGI config for HRMS Lite project."""
import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment (default to production for WSGI)
env = os.getenv('DJANGO_ENV', 'production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'hrms_lite.settings.{env}')

application = get_wsgi_application()
