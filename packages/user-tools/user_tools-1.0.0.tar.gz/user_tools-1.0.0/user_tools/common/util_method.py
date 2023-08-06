#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_method.py
# @Time    : 2021-12-16
# @Author  : Skypekey


def return_info(err_info, data):

    if err_info:
        return (False, err_info)
    else:
        return (True, data)


if __name__ == "__main__":
    pass
