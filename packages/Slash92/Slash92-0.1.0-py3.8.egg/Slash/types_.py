import hashlib
from typing import final
from .Core import core
from random import randint
from hashlib import md5


class Rules:
    def __init__(self):
        self.__rules = {
            "type_int"  : {
                "min" : 0,
                "max" : 255,
                "valide_foo" : self.valid_int
            },
            "type_text" : {
                "length" : 100,
                "valide_foo" : self.valid_text
            },
            "type_bool" : {
                "symbols" : [True, False],
                "valide_foo" : self.valid_bool
            },
            "type_date" : {
                "current" : "{}.{}.{}",
                "valide_foo" : self.valid_date
            }
        }

    def get_rules(self):
        return self.__rules
    
    def get_user_rules(self):
        return self.user_rules

    def new_rules(self, rules: dict):
        self.user_rules = rules
        return self.user_rules

    def valid_int(self, int_val, r):
        if (r["min"] < int_val < r["max"]):
            return True
        else:
            return False

    def valid_text(self, text_val, r):
        if (len(text_val) <= r["length"]):
            return True
        else:
            return False

    def valid_bool(self, bool_val, r):
        if (bool_val in r["symbols"]):
            return True
        else:
            return False

    def valid_date(self, date_val, r): ...

class ORMType:
    def _is_valid_datas(self, user_rules: Rules):
        if user_rules == "*":
            rules = Rules()
            rule = rules.get_rules()[self.type_name]

            return (rule["valide_foo"](self.value, rule), rule)
        else:
            rule = user_rules.get_user_rules()[self.type_name]

            return (rule["valide_foo"](self.value, rule), rule)

class Int(ORMType):
    def __init__(self, value):
        self.type_name = "type_int"
        self.value = value

class Text(ORMType):
    def __init__(self, value):
        self.type_name = "type_text"
        self.value = value

class Bool(ORMType):
    def __init__(self, value):
        self.type_name = "type_bool"
        self.value = value

class Date(ORMType):
    def __init__(self, value):
        self.type_name = "type_date"
        self.value = value


class BasicTypes:
    TYPES_LIST = (Int, Text, Bool, Date)
    DB_TYPES_LIST = {
        Int : "INT", Text : "TEXT",
        Bool : "BOOL", Date : "DATE"
    }


class Column:
    def __init__(self, column_type, column_name):
        self.column_type = column_type
        self.column_name = column_name
        self.column_sql_type = BasicTypes.DB_TYPES_LIST.get(self.column_type)


class Table:
    def __init__(self, name: str):
        self.__name = name
        self.__columns = []
        TablesManager.tables.update(
            {
                md5(self.__name.encode("utf-8")).digest() : self
            }
        )

    def get_name(self):
        return self.__name
    
    def set_columns(self, *names):
        self.__columns = names
    
    def get_columns(self):
        return self.__columns

    def create(self, connection):
        core.Create(self, BasicTypes.TYPES_LIST, connection)

@final
class TablesManager:
    tables = {}

    @staticmethod
    def find_by_name(name):
        return TablesManager.tables.get(md5(name.encode("utf-8")).digest())
    
    
