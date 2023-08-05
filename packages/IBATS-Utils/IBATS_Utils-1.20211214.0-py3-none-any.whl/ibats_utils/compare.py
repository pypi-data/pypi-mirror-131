#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/9/27 10:31
@File    : compare.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from dataclasses import dataclass


@dataclass
class FalseUntilEqual:
    match_obj: str
    ret: bool = False

    def __eq__(self, other):
        if not self.ret:
            self.ret = self.match_obj == other
        return self.ret


@dataclass
class TrueUntilEqual:
    match_obj: str
    ret: bool = True

    def __eq__(self, other):
        if self.ret:
            self.ret = not (self.match_obj == other)
        return self.ret
