# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 14:40:21
# @File Name:synchronizer.py
"""Code Description:同步记录小聚合
"""

from __future__ import annotations

import abc
from typing import Any

from easyddns.domain.synchronizes.dmz import DmzRecord
from easyddns.domain.synchronizes.dnspod import DnspodRecord
from easyddns.domain.synchronizes.records import IPv4AdressPolicy, Record


class SynchronzierError(Exception):
    """Synchronzier Exception
    """


class Synchronizer(abc.ABC):
    """同步器聚合根模型

    - 业务逻辑：
        1. 如果 master 中的记录和 slaver 中的记录不一致，则进行同步。
        2. 如果 master 和 slalver 中的记录齐备并且已同步，则可进行部署。
        3. 利用版本号来作为该实体的唯一识别符。
    """
    _master: Any
    _slaver: Any
    _version: int

    @abc.abstractmethod
    def sync(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def need_sync(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def can_delpoy(self) -> bool:
        raise NotImplementedError

    @property
    def master(self) -> Record:
        return self._master

    @property
    def slaver(self) -> Record:
        return self._slaver


class RecordSynchronizer(Synchronizer):
    """
    同步器聚合根模型业务实现：采用主从方式进行同步，当发现从属得记录与主记录不一致时，采用主记录
    的ipv4地址更新从属记录中的ipv4地址，并将同步后的sync对象部署到 dns 服务器上。

    - 前条件：
        1. 主为：dmz, 从为：dnspod。
        2. dmz 和 dnspod 的记录都应该齐备。
        3. dmz 和 dnspod 的记录需要同时满足可同步和可部署的条件。

    - 后条件:
        1. 返回一个用于同步 dmz 和 dnspod 记录的实体对象。
        2. 返回一个用于状态查询的同步器实体对象。

    """

    def __init__(self,
                 master: DmzRecord,
                 slaver: DnspodRecord, version: int = 0) -> None:
        self._master: DmzRecord = master
        self._slaver: DnspodRecord = slaver
        self._version = version

    def is_done_sync(self) -> bool:
        return self._master.ip == self._slaver.ip

    def need_sync(self) -> bool:
        if self.is_done_sync():
            return False
        return self._master.need_sync() or not self._slaver.need_sync()

    def can_delpoy(self) -> bool:
        """是否可以部署
        """
        if not self.is_done_sync():
            return False
        if self.version_number < 2:
            return False
        return self._master.can_deploy() and self._slaver.can_deploy()

    def sync(self) -> RecordSynchronizer:
        """同步 Dmz 端和 Dnspod 端的解析记录
        """
        if self._master.have_ip():
            self._slaver = \
                self._slaver.replace(self._slaver.id, self._master.ip)
            self._version += 1
        return self

    def is_valid(self) -> bool:
        return (self._master is not None and self._slaver is not None)

    def update_dmz_ip(self, new_ip: str):
        ipv4_identifier = IPv4AdressPolicy()
        if not ipv4_identifier.is_allowed(new_ip):
            raise SynchronzierError(f"input a invalid ipv4 address:{new_ip}")
        self._master = self._master.replace(new_ip)
        self._version += 1

    def update_dnspod(self, new_ip: str, new_id: str):
        ipv4_identifier = IPv4AdressPolicy()
        if not ipv4_identifier.is_allowed(new_ip):
            raise SynchronzierError(f"input a invalid ipv4 address:{new_ip}")
        self._slaver = self._slaver.replace(new_id, new_ip)
        self._version += 1

    @property
    def dmz_record(self) -> DmzRecord:
        return self._master

    @property
    def dnspod_record(self) -> DnspodRecord:
        return self._slaver

    @property
    def version_number(self) -> int:
        return self._version

    def __str__(self) -> str:
        return f"RecordSynchronizer(master:{self.dmz_record},"\
            f"slaver:{self.dnspod_record})"

    def __repr__(self) -> str:
        return self.__str__()


def register_synchornizer(
        master: DmzRecord, slaver: DnspodRecord
) -> RecordSynchronizer:
    return RecordSynchronizer(master=master, slaver=slaver, version=0)
