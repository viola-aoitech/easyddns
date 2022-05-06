# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 14:38:12
# @File Name:dmz.py
"""Code Description:主机记录模型
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from easyddns.domain.synchronizes.records import Record


@dataclass(frozen=True, repr=True)
class DmzRecord(Record):
    """Dmz 主机记录

    - 前条件：
        支持输入有效的用户 id 和 token，来自所使用的 dns 服务器。
    - 后条件:
        返回一个支持同步业务的 dmz 端值对象。
    """
    usr_info: str
    ip: str

    @classmethod
    def register(cls, user_id: str, token: str, ip="") -> DmzRecord:
        return cls(f"{user_id},{token}", ip)

    def replace(self, new_ip: Any) -> DmzRecord:
        return DmzRecord(self.usr_info, new_ip)

    @property
    def user(self) -> str:
        return self.usr_info

    def can_deploy(self) -> bool:
        """检查记录是否包含 id ,token
        """
        if len(self.usr_info) <= 0:
            return False
        return True

    def need_sync(self) -> bool:
        """检查记录是否包含ip，作为同步的必要条件
        """
        if not self.have_ip():
            return False
        return True
