# -*- coding: utf-8 -*-
# @Author: viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/06 15:26:41
# @File Name:uow.py
"""unit of work pattern model
"""

from __future__ import annotations

import abc
from typing import Any

from easyddns.adapters import logfactory
from easyddns.configs.websites import IP_WEBSITES
from easyddns.domain.synchronizes import synchronizer
from easyddns.service_layer import sessions


class UnitOfWork(abc.ABC):
    """TThis class encapsulates context management with the unit of work
    pattern.
    """
    dns: sessions.Session
    connect: bool = False

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        self.finish()

    @abc.abstractmethod
    def query(self, sync: synchronizer.Synchronizer) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def deploy(self, sync: synchronizer.Synchronizer) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def finish(self) -> None:
        raise NotImplementedError


class DnspodUnitOfWork(UnitOfWork):
    """Concrete Unit of Wokr model"""
    dns: sessions.DnspodSession

    def __init__(self,
                 session_factory: Any,
                 repeats: int, timeout: int,
                 logger: Any = logfactory.error_logger
                 ) -> None:
        super().__init__()
        self.session_factory = session_factory
        self.repeats = repeats
        self.timeout = timeout
        self.logger = logger
        self.connect = False

    def __enter__(self) -> UnitOfWork:
        self.dns = self.session_factory(logger=self.logger)
        self.connect = True
        return self

    def query(
        self, sync: synchronizer.RecordSynchronizer
    ) -> synchronizer.RecordSynchronizer:
        record = sync
        try:
            record = self.dns.query(
                sync, IP_WEBSITES, self.repeats, self.timeout
            )
        except sessions.SessionError as er:
            self.logger(er)
        except synchronizer.SynchronzierError as er:
            self.logger(er)
        return record

    def deploy(
        self, sync: synchronizer.RecordSynchronizer
    ) -> int:
        ans = -1
        try:
            ans = self.dns.delpoy(sync, self.repeats, self.timeout)
        except sessions.SessionError as er:
            self.logger(er)
        return ans

    def finish(self) -> None:
        if self.connect:
            self.connect = False
