#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackingtoolsgui.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def checkPackages():
    # If Windows NT
    extra_packages = {
        "nt" : ['pywin32', 'pywin32-ctypes', 'opencv-python'],
        "linux" : ['opencv-python'],
    }
    for system in extra_packages:
        if system in os.name:
            for package in extra_packages[system]:
                if not package in sys.modules:
                    pipmain(['install', package])

if __name__ == '__main__':
    checkPackages()
    main()
