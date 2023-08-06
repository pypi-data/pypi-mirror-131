#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""skalchemy: module."""

from __future__ import absolute_import

__version__ = '0.0.0'

import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 Please")

usage = "Usage: " + sys.argv[0] + """ option

    options:
    
        option1
        option2
"""

def main():
    """main: app."""
    try:
        if sys.argv[1:]:
            if sys.argv[1] == "--help":
                print(usage)
            elif sys.argv[1] == "--version":
                print(__version__)
            else:
                options[sys.argv[1]]()
        else:
            print(usage)
    except KeyError as _e:
        print("KeyError: " + str(_e))
        sys.exit(1)


if __name__ == '__main__':
    main()
