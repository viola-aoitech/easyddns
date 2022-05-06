# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/03/28 12:25:44
""" create a python file logger object
"""

import logging
from pathlib import Path


def register_logger(name: str) -> logging.Logger:
    """注册一个python logger

    :param str name: 主机名称
    :return logging: 返回
    """
    datefmt = r'%Y-%m-%d %H:%M:%S'
    record_format = r"%(asctime)s::%(levelname)s::"
    record_format += r"%(pathname)s::"
    record_format += "%(message)s"

    log_path = Path(f'./logs/{name}.log')
    if not log_path.parent.exists():
        log_path.parent.mkdir()

    logging.basicConfig(level=logging.WARNING,
                        format=record_format,
                        datefmt=datefmt,
                        filename=log_path,
                        filemode='a')
    return logging.getLogger(name)


dnspod_logger = register_logger("smart_ddns")
error_logger = dnspod_logger.error
