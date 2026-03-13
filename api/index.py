import os
import sys

# Add the parent directory to path so Django can find the apps
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_lite.settings.production')

# Import and initialize Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application  # Vercel looks for 'app'
