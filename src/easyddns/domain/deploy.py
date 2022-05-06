# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/28 21:28:17
# @File Name:deploy.py
"""Code Description: 部署 sync 的领域服务。
"""
from __future__ import annotations

from typing import Dict

from easyddns.domain.synchronizes.synchronizer import RecordSynchronizer


def make_dnspod_paramas(sync: RecordSynchronizer) -> Dict:
    """convert a sync object to parameters for dnspod website.

       - prev: the sync object should be able to deploy.

       - post: the input sync object will convert to a dnspod paramas
        with or without new ip.
    """
    token = sync.dmz_record.user
    domain = sync.dnspod_record.domain
    sub_domain = sync.dnspod_record.sub_domain
    record_id = sync.dnspod_record.id
    record_ip = sync.dnspod_record.ip

    return dict(
        login_token=token,
        domain=domain,
        format="json",
        sub_domain=sub_domain,
        record_type="A",
        record_line="默认",
        record_id=record_id,
        ip_value=record_ip,
    )
