from os import name
import re
from .core import CheckDatas, Connection, SQLConditions
from ..types_ import DataSet

from .exceptions_ import SlashRulesError

class Insert():
    def __init__(self, conn, table_name, names, values, rules="*"):
        responce = self.__validate(table_name, names, values, rules)
        conn.execute(CheckDatas.checkSQL(responce, "insert"))

    def __validate(self, table_name, names, values, rules):
        CheckDatas.checkStr(table_name)

        for name in names:
            CheckDatas.checkStr(name)

        for value in values:
            if value.type_name == "type_text":
                CheckDatas.checkStr(value.value)

            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

        names = str(names)
        names = names.replace("(", "")
        names = names.replace(")", "").replace("'", "")
        r = f"""INSERT INTO {table_name} ({names}) VALUES ("""

        for index, v in enumerate(values):
            if v.type_name == "type_int":
                r += str(v.value)
                if (index + 1) != len(values):
                    r += ", "
            elif v.type_name == "type_text":
                r += ("'" + v.value + "'")
                if (index + 1) != len(values):
                    r += ","
            elif v.type_name == "type_bool":
                r += str(v.value)
                if (index + 1) != len(values):
                    r += ", "
            elif v.type_name == "type_date":
                r += ("'" + str(v.value) + "'")
                if (index + 1) != len(values):
                    r += ", "
        r += ")"

        return r

class Delete():
    def __init__(self, conn, table_name, condition: SQLConditions):
        responce = self.__validate(table_name, condition)
        conn.execute(CheckDatas.checkSQL(responce, "delete"))

    def __validate(self, table_name, condition):
        CheckDatas.checkStr(table_name)
        r = "DELETE FROM {}{}".format(
                table_name,
                condition
            )

        return r

class Select():
    def __init__(self, conn, table_name, names, condition: SQLConditions):
        self.__conn = conn
        self.__responce = self.__validate(table_name, names, condition)
        self.__table_name = table_name
        self.__names = names

    def __validate(self, table_name, names, condition):
        CheckDatas.checkStr(table_name)

        return "SELECT {} FROM {}{}".format(
            ", ".join([n for n in names]),
            table_name, condition
        )

    def get(self):
        self.__conn.execute(CheckDatas.checkSQL(self.__responce, "select"))

        return DataSet(self.__table_name, self.__names, self.__conn.fetchall())

class Update():
    def __init__(self, conn, table_name, names, values, condition, rules="*"):
        responce = self.__validate(table_name, names, values, condition, rules)
        conn.execute(CheckDatas.checkSQL(responce, "update"))

    def __validate(self, table_name, names, values, condition, rules):
        CheckDatas.checkStr(table_name)
        r = "UPDATE {} SET ".format(table_name)

        for index, value in enumerate(values):
            valid_responce = value._is_valid_datas(rules)
            if not valid_responce[0]:
                raise SlashRulesError(f"\n\n\nRule: {valid_responce[1]}")

            if value.type_name == "type_text":
                r += " = ".join((names[index], f"'{value.value}'"))
            elif value.type_name == "type_int":
                r += " = ".join((names[index], f"{value.value}"))
            elif value.type_name == "type_bool":
                r += " = ".join((names[index], f"{value.value}"))
            elif value.type_name == "type_date":
                r += " = ".join((names[index], f"'{value.value}'"))

            r += ", " if index != (len(values) - 1) else ""

        r += condition

        return r

class Operations():
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, table_name, names, values, *, rules="*"):
        if rules == "*":
            Insert(self.__connection, table_name, names, values)
        else:
            Insert(self.__connection, table_name, names, values, rules)

    def select(self, table_name, names, condition = " "):
        return Select(self.__connection, table_name, names, condition).get()

    def delete(self, table_name, condition = " "):
        Delete(self.__connection, table_name, condition)

    def update(self, table_name, column_names, values, condition = " "):
        Update(self.__connection, table_name, column_names, values, condition)
