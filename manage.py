#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get environment (default to development)
    env = os.getenv('DJANGO_ENV', 'development')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'hrms_lite.settings.{env}')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Install requirements before running this command."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
