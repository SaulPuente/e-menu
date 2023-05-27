#-------------------------------------------------------------------------------
import os
import sys

import json
from typing import List
#-------------------------------------------------------------------------------
from ..mysql_queries.q_dao_t_user import dictionary_t_user
from ...data_transfer.dto_user import DTO_User
#-------------------------------------------------------------------------------
class DAO_T_Users(object):
    #...........................................................................
    """ Class: DAO access to users table. """
    #...........................................................................
    def __init__(self,db_handler):
        self.db_handler     = db_handler
    #...........................................................................
    def select_all(self, limit: int=50000) -> List[DTO_User]:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user["select_all"]%(limit)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        users_list = []
        for result in results:
            result = list(result)
            users_list.append(DTO_User(int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6])))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return users_list
    #...........................................................................
    def select_by_id(self, id: int=0) -> DTO_User:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user["select_by_id"]%(id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        if not result: return DTO_User()
        result = list(result)
        user = DTO_User(int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return user
    #...........................................................................
    def insert_new_user(self, email: str="-", fname: str="-", lname: str="-", password: str="-", status: str="pending", token: str="-") -> int:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user["insert_new_user"]%(email, fname, lname, password, status, token)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                id = cursor.lastrowid
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return id
    #...........................................................................
    def select_by_email(self, email: str="-") -> DTO_User:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user["select_by_email"]%(email)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        if not result: return None
        result = list(result)
        user = DTO_User(int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return user
    #...........................................................................
    def select_by_name(self, name: str="") -> List[DTO_User]:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user["select_by_name"]%(name, name, name)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        users_list = []
        for result in results:
            result = list(result)
            users_list.append(DTO_User(int(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6])))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return users_list
    #...........................................................................
    def select_pass(self, id: int) -> str:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user['select_pass']%(id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        result = list(result)
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return str(result[0])
    #...........................................................................
    def update_pass(self, id: int, password: str) -> bool:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user['update_pass']%(password,id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return True
    #...........................................................................
    def update_user_status(self, id: int, status: str) -> bool:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user['update_user_status']%(status,id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return True
    #...........................................................................
    def select_token(self, id: int) -> str:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user['select_token']%(id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        result = list(result)
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return str(result[0])
    #...........................................................................
    def update_token(self, id: int, password: str) -> bool:
        db_conn = self.db_handler.connect()
        query = dictionary_t_user['update_token']%(password,id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return True
    #...........................................................................
#-------------------------------------------------------------------------------