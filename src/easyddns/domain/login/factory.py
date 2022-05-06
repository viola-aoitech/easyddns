
# -*- coding: utf-8 -*-
# @Author: viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/06 10:47:06
# @File Name:factory.py
# pylint: disable=too-few-public-methods,missing-class-docstring


"""create a login object from a json.

json must be like belows:

"DNS": {
        "name": "xxx",
        "login": {
            "user id": "xx",
            "user token": "xxx"
        }
    },

"Record 1": {
        "type": "AAAA",
        "domain name": "www.aoitech.cn",
        "ttl": "300"
    },
"Need 1": {
        "type": "AAAA",
        "domain name": "www.aoitech.cn",
        "ttl": "300"
    },
"""

from __future__ import annotations

from typing import Any, Dict, Tuple, Set

from easyddns.domain.login.exceptions import LoginError
from easyddns.domain.login.record import AliyunUser, DnspodUser, Record, User

DNS_USER_DICT = {
    "Dnspod": [DnspodUser, "user id", 'user token'],
    "Aliyun": [AliyunUser, "access id", "access key"]
}

DNS_RECORD_NAMES = {"Record", "Need"}


class UserFactory:
    """make a user value object."""

    def register(self, data: Dict) -> User:
        """make a user from a structured dict.

        Args:
            data (Dict):user config which has been inited from a config
            json file.

        Returns:
            User: user info object
        """
        try:
            user_maker = DNS_USER_DICT[data["DNS"]['name']][0]
            id_name = DNS_USER_DICT[data["DNS"]['name']][1]
            key_name = DNS_USER_DICT[data["DNS"]['name']][2]
            id_value, key_value = self._parser_user(data, id_name, key_name)
        except KeyError as er:
            raise LoginError(f"Register::KeyError {er}") from er
        except NameError as er:
            raise LoginError(f"Register::NameError {er}") from er

        return user_maker.register(id_value, key_value)

    @staticmethod
    def _parser_user(
        data: Dict, id_name: str, key_name: str
    ) -> Tuple[str, str]:
        login = data['DNS']['login']
        if not login[id_name] or not login[key_name]:
            raise LoginError(
                f"login data must have user {id_name} and {key_name}.")
        return login[id_name], login[key_name]


class RecordFactory:
    """make a record from a structured dict and name."""

    def register_many(self, data: Dict) -> Set[Record]:
        records = set()
        for name in data.keys():
            if self._has_record_name(name):
                domain_name, ttl, rtype = self._parser_record(data, name)
                records.add(Record.register(domain_name, int(ttl), rtype))
        return records

    @staticmethod
    def _parser_record(data: Dict, name: str) -> Tuple[str, str, str]:
        try:
            rtype = data[name]["type"]
            domain_name = data[name]["domain name"]
            ttl = data[name]["ttl"]
        except KeyError as er:
            raise LoginError(f"Register::KeyError {er}") from er
        except NameError as er:
            raise LoginError(f"Register::NameError {er}") from er
        return domain_name, ttl, rtype

    @staticmethod
    def _has_record_name(data: Any) -> bool:
        for keyword in DNS_RECORD_NAMES:
            if keyword in data:
                return True
        return False
