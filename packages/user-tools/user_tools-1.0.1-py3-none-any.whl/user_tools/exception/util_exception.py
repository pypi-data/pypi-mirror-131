#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_exception.py
# @Time    : 2021-12-14
# @Author  : Skypekey


class ParameterException(Exception):
    def __init__(self, errinfo) -> None:
        super().__init__()
        self.errinfo = errinfo

    def __str__(self) -> str:
        return self.errinfo


if __name__ == "__main__":
    pass
