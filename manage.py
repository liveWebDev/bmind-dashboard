#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import sys
from django.template.defaulttags import register

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "DataViz.settings"
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
