# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 12:22:54
# @File Name:proxy.py
"""Code Description: 网络代理服务模型。
"""

from __future__ import annotations

import abc
import socket
from typing import Tuple

from easyddns.domain.synchronizes.synchronizer import Synchronizer


class BaseQuery(abc.ABC):
    """Base Class of the Query Interfaces"""
    @abc.abstractmethod
    def query(self, **kwargs) -> Tuple[str, str]:
        raise NotImplementedError

    @staticmethod
    def check_access(host="114.114.114.114", port=53, timeout=3) -> bool:
        """try to connect 114 DNS Server with socket
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False

    @abc.abstractmethod
    def get_results(self) -> Synchronizer:
        raise NotImplementedError


class BaseDeploy(abc.ABC):
    """This base class describes deploying a sync in a remote DNS Server
    website.
    """
    @abc.abstractmethod
    def write(self, **kwargs) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def check_access(self, **kwargs) -> bool:
        raise NotImplementedError
