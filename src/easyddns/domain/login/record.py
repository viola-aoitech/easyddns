# -*- coding: utf-8 -*-
# @Author: viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/06 08:54:13
# @File Name:record.py
# pylint: disable=too-few-public-methods,missing-class-docstring

"""
model of login record implement read and write usr config json file.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any,  Set, Tuple
from easyddns.domain.login.exceptions import LoginError


class User(abc.ABC):
    """User information Base class"""


@dataclass(frozen=True)
class DnspodUser(User):
    """Dnspod User info Value Object"""
    usr_id: Any
    usr_token: Any

    @classmethod
    def register(cls, usr_id: str, usr_token: str) -> DnspodUser:
        return cls(usr_id, usr_token)

    def __post_init__(self) -> None:
        if not self.usr_id or not self.usr_token:
            raise LoginError("Dnspod need filled id and token value.")


@dataclass(frozen=True)
class AliyunUser(User):
    """Aliyun User info Value Object"""
    access_id: Any
    access_key: Any

    def __post_init__(self) -> None:
        if not self.access_id or not self.access_key:
            raise LoginError(
                "AliCloud need filled access_id and token access_key."
            )

    @classmethod
    def register(cls, access_id: str, access_key: str) -> AliyunUser:
        return cls(access_id, access_key)


@dataclass(frozen=True)
class Record:
    """Config Record Value Object"""
    domain: Any
    sub_domain: Any
    ttl: Any = field(default='300')
    rtype: Any = field(default="AAAA")

    def __post_init__(self) -> None:
        if not self.domain or not self.sub_domain:
            raise LoginError("domain and sub_domain must not empty.")

    @classmethod
    def register(cls,
                 domain_name: str, ttl: int, record_type: str = 'AAAA'
                 ) -> Record:
        sub_domain, domain = cls._parser_domain(domain_name)
        return cls(domain, sub_domain, str(ttl), record_type)

    @staticmethod
    def _parser_domain(domain_name: str) -> Tuple[str, str]:
        splits = domain_name.split('.', maxsplit=1)
        return splits[0], splits[1]


@dataclass(frozen=False, repr=True)
class Login:
    user: User = field(default_factory=User)
    records: Set[Record] = field(default_factory=set)
