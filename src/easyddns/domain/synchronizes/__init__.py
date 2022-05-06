# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/29 02:40:36
# @File Name:__init__.py
"""Code Description:
"""

from easyddns.domain.synchronizes.dmz import DmzRecord
from easyddns.domain.synchronizes.dnspod import DnspodRecord
from easyddns.domain.synchronizes.records import IPv4AdressPolicy
from easyddns.domain.synchronizes.synchronizer import (RecordSynchronizer,
                                                       Synchronizer,
                                                       register_synchornizer)

__all__ = ["DmzRecord", "DnspodRecord", "Synchronizer",
           "RecordSynchronizer", "register_synchornizer", "IPv4AdressPolicy"]
