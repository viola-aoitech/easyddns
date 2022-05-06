# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/05/05 15:01:03
# @File Name:jsonconfig.py
"""a json config file operation
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict

from easyddns.domain.login.exceptions import LoginError
from easyddns.domain.login.factory import RecordFactory, UserFactory
from easyddns.domain.login.record import User, Login


class JsonConfig:
    """easy ddns's config file loading and writing.
    """

    def __init__(self, path: str) -> None:
        self._conf: Path = Path(path)
        if not self._conf.exists():
            raise LoginError("config file has not exist, checking path!")
        self._login: Login = Login()

    @staticmethod
    def _write(path: Path, data: Dict) -> None:
        jdata = json.dumps(data)
        with open(path, 'w', encoding='utf8') as fout:
            fout.write(jdata)

    @staticmethod
    def _read(path: Path) -> Dict:
        """read a json file and convert to a dict"""
        with open(path, 'r', encoding='utf8') as fin:
            data = json.load(fin)
        return data

    def read(self, logger: Callable = print) -> None:
        """read user and record from a config json file."""
        data = self._read(self._conf)
        try:
            user = UserFactory().register(data)
            records = RecordFactory().register_many(data)
        except LoginError as er:
            logger(er)
        else:
            self._login = Login(user, records)

    @staticmethod
    def write(logger: Callable = print) -> None:
        """write user and records into a config file.
        """
        return logger("not implemented")

    @property
    def user(self) -> User:
        return self._login.user

    @property
    def login(self) -> Login:
        return self._login

    def __str__(self) -> str:
        return f"Conf(user:{self._login.user},records:{self._login.records})"

    def __repr__(self) -> str:
        return self.__str__()
