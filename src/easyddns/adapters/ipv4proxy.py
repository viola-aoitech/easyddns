# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/04/29 00:32:38
# @File Name:query_management.py
"""Code Description:
"""

from __future__ import annotations

import random
from typing import Any, Tuple

import requests
from easyddns.adapters.proxy import BaseQuery
from easyddns.domain.synchronizes.records import IPv4AdressPolicy

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
}


class IPv4Proxy(BaseQuery):
    """This class implemented a proxy pattern in charge of finding a local IP
    address from remote websites written into a config file.
    """

    @staticmethod
    def get_method(url: str,
                   headers: dict, timeout: int = 2, logger: Any = print
                   ) -> requests.Response:
        try:
            ans = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.RequestException as er:
            logger(er)
            return requests.Response()
        else:
            return ans

    def query(self,
              url: str, timeout: int = 4, logger: Any = print
              ) -> Tuple[str, str]:
        """query public ip from self providers.
        """
        checker = IPv4AdressPolicy()
        headers = get_headers()

        html = self.get_method(url, headers, timeout, logger)
        ip = checker.ipv4(html.text)

        if checker.is_allowed(ip):
            return url, ip
        return url, "failed"

    def get_results(self) -> Any:
        """placeholder function
        """
        return None


def get_headers() -> dict:
    """This function gets a camouflage header with the request operation.
    """
    agent = {"User-Agent": random.choice(lst_agent_phone)}
    return agent


lst_agent_phone = [
    # IPhone
    'Mozilla/5.0.html (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) '\
    'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.html.2 Mobile/8J2'\
    'Safari/6533.18.5',
    # IPAD
    'Mozilla/5.0.html (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) '\
    'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.html.2' \
    'Mobile/8C148 Safari/6533.18.5',
    'Mozilla/5.0.html (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) '\
    'AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.html.2 '\
    'Mobile/8J2 Safari/6533.18.5',
    # Android
    'Mozilla/5.0.html(Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 '\
    'Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0.html '\
    'Mobile Safari/533.1',
    'Mozilla/5.0.html (Linux; U; Android 2.3.7; en-us; '\
    'Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) '\
    'Version/4.0.html Mobile Safari/533.1',
    # QQ
    'MQQBrowser/26 Mozilla/5.0.html (Linux; U; Android 2.3.7; zh-cn; '\
    'MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) '\
    'Version/4.0.html Mobile Safari/533.1',
    # Android Opera Mobile
    'Opera/9.80 (Android 2.3.4; Linux; '\
    'Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    # Android Pad Moto Xoom
    'Mozilla/5.0.html (Linux; U; Android 3.0.html; en-us; Xoom Build/HRI39)'\
    ' AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0.html Safari/534.13',
]
