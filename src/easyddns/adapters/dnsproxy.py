# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/29 02:41:36
# @File Name:dnspod_proxy.py
"""Code Description: dnspod 服务代理
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

import requests
from easyddns.adapters.proxy import BaseDeploy, BaseQuery
from easyddns.domain import deploy, synchronizes


class DnspodError(Exception):
    """All DNSPOD Error"""


class DnspodProxy(BaseQuery, BaseDeploy):
    """
    Dnspod 服务
    :param  BaseQuery: 查询服务接口
    :param  BaseDeploy: 部署服务接口
    """
    sync: synchronizes.RecordSynchronizer

    def set_sync(self, sync: synchronizes.RecordSynchronizer) -> None:
        self.sync = sync

    def query(self, timeout: int = 3, logger: Any = print) -> Tuple[str, str]:
        """query sync's dnspod ipv4 addresss and record's id, it will try 3
        times until query success.
        """
        _params = deploy.make_dnspod_paramas(self.sync)
        ans = self.get_record_list(_params, timeout=timeout, logger=logger)
        return ans["ip_value"], ans["record_id"]

    def delpoy(self, timeout: int = 3, logger: Any = print
               ) -> int:
        """deploy new ip to dnspod resolver,it will try 3 times until query
         success.
        """
        if not self.check_access():
            return -1

        if not self.sync.is_done_sync():
            return -1

        _params = deploy.make_dnspod_paramas(self.sync)
        _params["value"] = _params["ip_value"]  # ! just change key name...

        return self.write(_params, timeout=timeout, logger=logger)

    @staticmethod
    def post_to_dnspod(
        url: str, data: dict, timeout: int, logger: Any = print
    ) -> requests.Response:
        """simple requests wrap post-method

        :param str url: url address
        :param dict data: parameters for writing
        :param int timeout: sentienal value for post method
        :param Any logger: defaults to print
        :return requests.Response: if post a url is fail.
        """
        try:
            r = requests.post(url, data=data, timeout=timeout)
        except requests.exceptions.RequestException as er:
            logger(er)
            return requests.Response()
        else:
            return r

    def get_record_list(self,
                        params: Dict[str, str], timeout: int = 3,
                        logger: Any = print
                        ) -> Dict[Any, Any]:
        """获取 dnspod 中的解析记录
           - prev:
                timeout，logger 被正确赋值。self.paramas 符合 dnspod api 查询规则。
           - post:
                1. 如果成功，返回所需记录,格式为key('code','record_id','ip_value')
                2. 如果失败，返回空字典。
           - ref：https://www.dnspod.cn/docs/records.html#record-list
        """
        _url = "https://dnsapi.cn/Record.List"

        ans = self.post_to_dnspod(_url, params, timeout, logger)
        if ans.status_code is None:
            raise DnspodError("Dnspod can not connect!")
        code = ans.json()["status"]["code"]
        record_id = ans.json()["records"][0]["id"] if code == "1" else ""
        ip_value = ans.json()["records"][0]["value"] if code == "1" else ""
        return dict(code=code, record_id=record_id, ip_value=ip_value)

    def write_new_record(self,
                         params: Dict[str, str], timeout: int = 3,
                         logger: Any = print
                         ) -> str:
        """create a new record id from dnspod and。
        - prev:
            1. params is a dnspod and ti have assigned a new ipv4 address.
            2. timeout，logger has assigned.
        - post:
            1. if success: return new record's id
            2. if failed: return failed.
        - ref：https://www.dnspod.cn/docs/records.html#record-create

        """
        _url = "https://dnsapi.cn/Record.Create"

        ans = self.post_to_dnspod(_url, params, timeout, logger)
        if ans.status_code is None:
            return "failed"
        if ans.json()['status']['code'] == '1':
            return ans.json()["record"]["id"]
        return "failed"  # block other identifies

    def write(self,
              data: Dict[str, str], timeout: int = 3,
              logger: Any = print
              ) -> int:
        """ write a dnspod record to dnspod's name resolver

        :param dict params: a dnspod record and new ip has assigned.
        :param int timeo ut: a runtime sentinal value, defaults to 3
        :param Any logger:  any logger method, defaults to print
        :return str: status code if success else return -1
        """
        _url = "https://dnsapi.cn/Record.Ddns"

        if data["value"] == "" or data["record_id"] == "":
            return -1

        ans = self.post_to_dnspod(_url, data, timeout, logger)
        return int(ans.json()["status"]["code"])

    def check_access(self) -> bool:
        return True

    def get_results(self) -> Any:
        return self.sync
