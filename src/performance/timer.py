# -*- coding: utf-8 -*-
# @Author:viola@aoitech.net
# Copyright (c) 2020-2025 viola
# @Date Time:2022/03/16 17:24:55
# @File Name:timer.py
"""Code Description: 性能测试测试模型, us 精度
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict


def time_output(dt: float, text: str = "{:3.3f} us") -> str:
    """format a test result

    Args:
        dt (Any):  time cost intervel in ns.
        text (sting,): formation text. Defaults to "{:3.3f} us".

    Returns:
        str: output a time cost string in 3 significant digits.
    """
    return text.format(round(dt*1e6, 3))


class TimerError(Exception):
    """Exception for timer"""


@dataclass
class Timer:
    """
    Simple Implement Timer Context mangeer

    - Usages:
    1. use it as a context manger.

    ```python
    import Timer

    with Timer("test name") as timer:
        code block
        record_out = timer.record
    ```

    2. Using it as a counter object.

    ```python
    import Timer

    t = Timer()
    t.start()
    sleep(10.0)
    t.end()

    # should print timec cost in us.
    ```

    - Ref:
        1. cover https://realpython.com/python-timer/
    """
    record: ClassVar[Dict[str, float]] = {}
    name: Any = None  # test name
    text: str = "time cost {:3.2f} us"
    logger: Any = print
    _t_start: Any = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if self.name:
            self.record.setdefault(self.name, 0)

    def start(self):
        if self._t_start is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")
        self._t_start = time.perf_counter()

    def stop(self) -> float:
        if self._t_start is None:
            raise TimerError("Timer is not running. Use .start() to run it")

        elapse_time = time.perf_counter() - self._t_start  # ubnit in second
        self._t_start = None

        if self.logger:
            self.logger(time_output(elapse_time, self.text))

        if self.name:
            self.record[self.name] += round(elapse_time*1e6, 3)  # total time.

        return elapse_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()


def simple_driver_01():
    tic = time.perf_counter_ns()
    time.sleep(0.02)
    toc = time.perf_counter_ns()

    dt = toc-tic
    print(f"Downloaded the tutorial in {time_output(dt)} microsecond")


def usage_01_driver():
    with Timer("context manager") as it:
        time.sleep(0.02)
        result = it.record
    print(result)


def usage_02_driver():
    timer = Timer()
    timer.start()
    time.sleep(0.02)
    timer.stop()


if __name__ == "__main__":
    usage_01_driver()
