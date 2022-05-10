# -*- coding: utf-8 -*-
# @Author: viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/06 18:24:22
# @File Name:sessions.py
"""a session for any DNS Service website
"""


from __future__ import annotations

import abc
from typing import Any, Callable, Set

from tqdm import tqdm

from easyddns.adapters.dnsproxy import DnspodProxy
from easyddns.adapters.ipv4proxy import IPv4Proxy
from easyddns.domain.synchronizes.records import IPv4AdressPolicy
from easyddns.domain.synchronizes.synchronizer import (RecordSynchronizer,
                                                       Synchronizer)


class SessionError(Exception):
    """DDNS Session Exception
    """


class Session(abc.ABC):
    """The Inteface of DNS Session
    """
    @abc.abstractmethod
    def query(
        self, sync: Synchronizer, websites: Set, repeat_time: int, timeout: int
    ) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def delpoy(
        self, sync: Synchronizer, repeat_time: int, timeout: int
    ) -> bool:
        raise NotImplementedError


class DnspodSession(Session):
    """This class is a session model for managing ipv4 finder proxy and
    DNSPOD's API Functions.
    """

    def __init__(self, logger: Callable = print) -> None:
        super().__init__()
        self._logger = logger
        self.local: IPv4Proxy = IPv4Proxy()
        self.remote: DnspodProxy = DnspodProxy()

    def query(self,
              sync: RecordSynchronizer,
              websites: Set,
              repeat_time: int = 3, timeout: int = 3) -> RecordSynchronizer:
        if not self.local.check_access():
            raise SessionError("internet has not connected.")

        if not sync:
            raise SessionError("sync must be assigned!")
        pbar = tqdm(range(100))
        pbar.update(10)

        _ip = self.dmz_worker(websites, timeout)
        sync.update_dmz_ip(_ip)
        pbar.update(40)

        _id, _ip = self.dnspod_worker(sync, repeat_time, timeout)
        sync.update_dnspod(_ip, _id)
        pbar.update(50)

        return sync

    def dnspod_worker(self, sync, repeat_time, timeout):
        self.remote.set_sync(sync)
        _id, _ip = "failed", "failed"
        for _ in range(repeat_time):
            _ip, _id = self.remote.query(timeout, self._logger)
            if IPv4AdressPolicy().is_allowed(_ip):
                return _id, _ip
        return _id, _ip

    def dmz_worker(self, websites, timeout):
        _ip = "failed"
        for webstie in websites:
            _, _ip = self.local.query(webstie, timeout, self._logger)
            if IPv4AdressPolicy().is_allowed(_ip):
                return _ip
        return _ip

    def delpoy(self,
               sync: RecordSynchronizer,
               repeat_time: int = 3, timeout: int = 3) -> int:
        """This function deploys a synchronizer's record to the Dnspod website.

        :param int repeat_time: defaults to 3
        :param int timeout: defaults to 3
        :return int: 1 if success, else return -1.
        """
        ans = -1
        self.remote.set_sync(sync)
        for _ in tqdm(range(repeat_time)):
            ans = self.remote.delpoy(timeout)
            if ans == 1:
                break
        return ans
