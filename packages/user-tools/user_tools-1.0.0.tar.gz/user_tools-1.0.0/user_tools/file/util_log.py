#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_log.py
# @Time    : 2021-06-10
# @Author  : Skypekey


import pathlib
import logging
from functools import wraps
from logging.handlers import RotatingFileHandler


class Pylog():

    def __init__(self, log_file) -> None:

        self.log_file = log_file
        pathlib.Path(self.log_file).parent.mkdir(parents=True,
                                                 exist_ok=True)
        self.logger = logging.getLogger()  # 实例化一个logger对象
        self.logger.setLevel(logging.INFO)  # 设置初始显示级别
        self.fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')

    def __console(self, message, maxBytes=1024 * 1024 * 5, level=''):
        # 创建一个文件句柄
        file_handle = RotatingFileHandler(filename=self.log_file,
                                          mode='a', encoding="UTF-8",
                                          backupCount=1,
                                          maxBytes=maxBytes)
        # 创建一个输出格式
        file_handle.setFormatter(self.fmt)  # 文件句柄设置格式
        if(level.lower() == "debug"):
            file_handle.setLevel(logging.DEBUG)
        else:
            file_handle.setLevel(logging.INFO)
        self.logger.addHandler(file_handle)  # logger对象绑定文件句柄

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning' or level == 'warn':
            self.logger.warn(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'fatal' or level == 'critical':
            self.logger.critical(message)
        self.logger.removeHandler(file_handle)
        file_handle.close()

    def logger_tuple(self, func):
        """用于返回值为(True/False, "输出")的函数打印日志。"""

        @wraps(func)
        def with_logging(*args, **kwargs):
            result = func(*args, **kwargs)
            print(result)
            if result[0]:
                self.__console(result[1])
            else:
                self.__console(result[1], level='error')
            return result
        return with_logging

    def logger_msg(self, level, msg):
        """直接打印日志"""

        LEVEL = ["debug", "info", "warning", "warn",
                 "error", "fatal", "critical"]
        if level not in LEVEL:
            self.__console(f"Level {level} is not correct!", level="error")
        else:
            self.__console(msg, level=level)


if __name__ == "__main__":
    pass
