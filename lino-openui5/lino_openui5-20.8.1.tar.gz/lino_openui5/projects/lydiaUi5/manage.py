#!/usr/bin/env python
import os
import sys
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = \
        'lino_openui5.projects.lydiaUi5.settings.demo'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
