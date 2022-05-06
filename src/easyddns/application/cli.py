# -*- coding: utf-8 -*-
# @Author: viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/06 13:21:00
# @File Name:cliapp.py
# pylint: disable = import-outside-toplevel
"""
Wheel command-line utility.
"""

from __future__ import annotations

import argparse

from easyddns.service_layer import services, sessions, unit_of_work
from easyddns.domain.login.record import AliyunUser, DnspodUser
from easyddns.adapters.logfactory import error_logger


def output_ipv4addrs(dmz, dnspod) -> None:
    from datetime import datetime
    now = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    print(f"Query Time: {now}")
    print(f"Query Result:\n Dmz: {dmz}, dnspod: {dnspod}")


def display_ip(user, records):
    if isinstance(user, DnspodUser):
        for record in records:
            sync = services.register_sychronizer(
                user.usr_id, user.usr_token, record.domain, record.sub_domain
            )
            uow = unit_of_work.DnspodUnitOfWork(
                sessions.DnspodSession, 3, 2, error_logger
            )

            result = services.get_sync_status(sync, uow)
            output_ipv4addrs(result["local"], result["remote"])
    if isinstance(user, AliyunUser):
        print("Not implement yet!")


def auto_sync(user, records):
    if isinstance(user, DnspodUser):
        for record in records:
            sync = services.register_sychronizer(
                user.usr_id, user.usr_token, record.domain, record.sub_domain
            )
            uow = unit_of_work.DnspodUnitOfWork(
                sessions.DnspodSession, 3, 2, error_logger
            )

            result = services.run_sync(sync, uow)
            if result == 0:
                print("not need run sync!")
            if result == 1:
                print("sync success!")


def main() -> int:
    from .. import __version__
    info = f"""Easy Dynamics Domain Name Resolution: {__version__}"""
    parser = argparse.ArgumentParser(description=info)

    parser.add_argument(
        'configs', type=str,
        help='init program from a json configure file.'
    )

    parser.add_argument(
        '-d', '--display', dest='display', action='store_true',
        help='only display sync information to stdout.'
    )

    args = parser.parse_args()
    login = services.load_config(args.configs)

    user = login.user
    records = login.records

    if args.display:
        display_ip(user, records)
    else:
        auto_sync(user, records)

    return 1
