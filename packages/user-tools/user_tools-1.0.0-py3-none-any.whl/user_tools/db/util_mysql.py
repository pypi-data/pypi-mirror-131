#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @File    : util_mysql.py
# @Time    : 2021-12-14
# @Author  : Skypekey


#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""A custom object for MySQL, to operate the MySQL database."""

import pymysql
from common import util_method
from exception import util_exception


class User_MySQL():
    def __init__(self, info, method="host") -> None:
        self.info = info
        self.method = method

    def __verify(self):
        """Initialize database authentication information.

        :param method(str): Method used for database authentication. Only host and socket.
        :param info(Dict): Database authentication information.\n
            The format of info:\n
                info = {
                    # required, where use host to access database.
                    "host": "host",
                    "username": "user", # required
                    "password": "password", # required
                    "port": 3306, # optional, default is 3306
                    "database": "mysql", # optional
                    # required, where use socket to access database.
                    "socket": "/tmp/mysql.sock"
                }
        :return Tuple(bool, db_conn|str, db_cur|None): If there is no error, return the database connection handle and cursor handle, otherwise an error message is returned."""

        arg_list = ["host", "username", "password",
                    "port", "database", "socket"]
        connect_info = self.info.copy()
        err_info = ""

        for i in self.info.keys():
            if i not in arg_list:
                err_info = f"非法参数 {i}，只允许以下参数：\n{''.join(arg_list)}"
                break
        if self.method not in ["host", "socket"]:
            err_info = "method 只能为 host 或 socket"
            # err_info = "Only host and socket methods are allowed"
        elif not isinstance(self.info, dict):
            err_info = "info 必须为字典对象"
        elif "username" not in self.info or not self.info["username"]:
            err_info = "info 中必须包含 username 且不能为空"
        elif "password" not in self.info or not self.info["password"]:
            err_info = "info 中必须包含 password 且不能为空"
        elif "database" not in self.info or not self.info["database"]:
            err_info = "info 中必须包含 database 且不能为空"
        elif self.method == "host":
            if "host" not in self.info or not self.info["host"]:
                err_info = f"When using {self.method} authentication,\
                             host is required"
            elif "port" not in self.info or not self.info["port"]:
                connect_info["port"] = 3306
        elif self.method == "socket":
            if "socket" not in self.info or not self.info["socket"]:
                err_info = f"When using {self.method} authentication,\
                             socket is required"

        util_method.return_info(err_info, connect_info)

    def __connect(self):
        """Connect to database."""

        try:
            flag, result = self.__verify()
            if flag:
                self.db_conn = pymysql.connect(**result)
                self.db_cur = self.db_conn.cursor(pymysql.cursors.DictCursor)
            else:
                raise util_exception.ParameterException(result)
        except Exception as e:
            return f"Database connection error, exception info is:\n{str(e)}"

    def __close(self):
        self.db_cur.close()
        self.db_conn.close()

    def __check(self, isquery=True):
        err_info = self.__connect()
        if not err_info:
            isselect = self.sql.lower().startswith("select")
            into = "into" in self.sql.lower().spilt(" ")
            if isquery and (not isselect or into):
                err_info = "Only Select sql statement is supported when use query method."
            elif not isquery and isselect and not into:
                err_info = "Sql statement must contains into when use noquery method and use select sql statement."

        util_method.return_info(err_info, "")

    def Query(self, sql):
        """Query data from the database.

        :param sql(str): It's a sql statement."""

        err_info = ""
        data = ""

        check_result = self.__check()
        if not check_result:
            try:
                self.db_cur.execute(sql)
                data = self.db_cur.fetchall()
            except Exception as e:
                err_info = f"sql statement is {sql}.\n exception info is:\n{str(e)}"
            finally:
                self.__close()
        util_method.return_info(err_info, data)

    def NoQuery(self, sql):
        """Change the data in the database.

        :param sql(str): It's a sql statement."""

        err_info = ""
        data = ""

        check_result = self.__check()
        if not check_result:
            try:
                self.db_cur.execute(sql)
                self.db_conn.commit()
            except Exception as e:
                self.db_conn.rollback()
                err_info = f"sql statement is {sql}.\n exception info is:\n{str(e)}"
            finally:
                self.__close()

        util_method.return_info(err_info, data)


if __name__ == "__main__":
    pass
