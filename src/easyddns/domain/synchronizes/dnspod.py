
# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 14:36:34
# @File Name:dnspod.py
"""Code Description: dnspod记录模型
"""

from __future__ import annotations

from dataclasses import dataclass, field

from easyddns.domain.synchronizes.records import Record


@dataclass(frozen=True)
class DnspodRecord(Record):
    """Dnspod 网站记录模型
    """
    id: str
    ip: str
    domain: str
    sub_domain: str = field(default="www", init=True)

    @classmethod
    def register(cls,
                 domain: str, sub_domain: str = "www",
                 record_ip: str = "", record_id: str = ""
                 ) -> DnspodRecord:
        return cls(record_id, record_ip, domain, sub_domain)

    def replace(self, new_id, new_ip) -> DnspodRecord:
        return DnspodRecord(new_id, new_ip, self.domain, self.sub_domain)

    def __eq__(self, other: DnspodRecord) -> bool:
        if not isinstance(other, DnspodRecord):
            return False
        if not other.have_ip():
            return False
        return (self.ip == other.ip and self.domain == other.domain)

    def can_deploy(self) -> bool:
        """返回记录是否能被部署

        :return bool: 如果 id 和 ip 不为空，则可以部署。
        """
        return len(self.id) > 0 and self.have_ip()  # is empty dnspod record

    def need_sync(self) -> bool:
        return len(self.id) > 0 and self.have_ip()  # is empty dnspod record
