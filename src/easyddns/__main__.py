# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/26 20:47:52
# @File Name:main.py
"""Code Description: script for application
"""
import sys

if __name__ == "__main__":
    if __package__ == '':
        # To be able to run 'python easyddns':
        import os.path
        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    from easyddns.application.cli import main
    sys.exit(main())
