# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/24 21:46:25
# @File Name:service.py
# pylint: disable=too-many-arguments
"""Code Description: service layer design
"""

from __future__ import annotations

from typing import Callable, Dict

from easyddns.configs import jsonconfig
from easyddns.domain import login, synchronizes
from easyddns.service_layer.unit_of_work import UnitOfWork
from easyddns.adapters.logfactory import error_logger


class InvalidSync(Exception):
    '''Sync Input Error'''


def register_sychronizer(
        user_id: str, token: str, domain: str, subdomain: str
) -> synchronizes.RecordSynchronizer:
    """register a domain model: record synchronzier..

    Args:
        user_id (str): dnspod's  user id
        token (str): dnspod's  user token
        domain (str): record domain name
        subdomain (str): record sun domain name

    Returns:
        synchronization.RecordSynchronizer: a model for sync logics operations
    """
    dmz = synchronizes.DmzRecord.register(user_id, token)
    dnspod = synchronizes.DnspodRecord.register(domain, subdomain)
    sync = synchronizes.register_synchornizer(master=dmz, slaver=dnspod)
    return sync


def run_sync(sync: synchronizes.Synchronizer, uow: UnitOfWork) -> int:
    """automatic run synchronizer to delpoy a domain name resolution.

    Args:
        sync (synchronizes.Synchronizer): init sync model
        uow (UnitOfWork): a special work for different dns website

   Returns:
        int: 1 if successs, else 0 when do not need to run prog.
    """
    with uow:
        dns = uow.query(sync)  # type: synchronizes.Synchronizer
        if dns is None:
            raise InvalidSync(f"Invalid Synchronize:{sync}.")
        if dns.need_sync():
            dns.sync()
            uow.deploy(dns)
        else:
            return 0
    return 1


def get_sync_status(sync: synchronizes.Synchronizer, uow: UnitOfWork) -> Dict:
    with uow:
        dns = uow.query(sync)  # type: synchronizes.Synchronizer
        if dns is None:
            raise InvalidSync(f"Invalid Synchronize:{sync}.")
    return dict(local=dns.master, remote=dns.slaver)


def load_config(path: str, logger: Callable = error_logger) -> login.Login:
    config = jsonconfig.JsonConfig(path)
    config.read(logger=logger)
    return config.login
