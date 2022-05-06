# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 14:30:29
# @File Name:records.py
"""Code Description:
"""

from __future__ import annotations

import abc
import re
from dataclasses import dataclass
from typing import Any


class Record(abc.ABC):
    """同步记录业务模型

    - 前条件：
        输入合法的ipv4 地址为初始值，使用register函数进行构造。

    - 后条件：
        返回一个支持同步操作的值对象。
    """
    ip: Any

    @classmethod
    def register(cls, *args) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, *args) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def can_deploy(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def need_sync(self) -> bool:
        """检查记录是否包含ip，作为同步的必要条件
        """
        raise NotImplementedError

    def have_ip(self) -> bool:
        return IPv4AdressPolicy().is_allowed(self.ip)


@dataclass(frozen=True)
class IPv4AdressPolicy:
    """策略模式：验证ip地址是否为有效值。
    """

    def is_allowed(self, ip: str) -> bool:
        """判断是否为有效 IP 地址"""
        if len(ip) > 15 or len(ip) < 7:
            return False
        if "." not in ip:
            return False
        if self.ipv4(ip) == "empty":
            return False
        return True

    @staticmethod
    def ipv4(context: str) -> str:
        result = re.findall(
            r"((?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d]))", context, re.I)
        if len(result) > 0:
            return result[0]
        return "empty"
