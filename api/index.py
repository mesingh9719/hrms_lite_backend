import os
import sys
import traceback

# Add the parent directory to path so Django can find the apps
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms_lite.settings.production')

try:
    # Import and initialize Django WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application  # Vercel looks for 'app'
except Exception as e:
    # If Django fails to load, create a simple debug app
    error_message = f"Django failed to load:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
    
    def app(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [error_message.encode('utf-8')]
