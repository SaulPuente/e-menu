#-------------------------------------------------------------------------------
import os
import sys

import json
from typing import List
#-------------------------------------------------------------------------------
from ..mysql_queries.q_dao_t_recipe import dictionary_t_recipes
from ...data_transfer.dto_recipe import DTO_Recipe
#-------------------------------------------------------------------------------
class DAO_T_Recipes(object):
    #...........................................................................
    """ Class: DAO access to users table. """
    #...........................................................................
    def __init__(self,db_handler):
        self.db_handler     = db_handler
    #...........................................................................
    def select_all(self) -> List[DTO_Recipe]:
        db_conn = self.db_handler.connect()
        query = dictionary_t_recipes["select_all"]
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        recipes_list = []
        for result in results:
            result = list(result)
            recipes_list.append(DTO_Recipe(int(result[0]), str(result[1]), str(result[2]), str(result[3]), json.loads(str(result[4])), str(result[5]), str(result[6]), str(result[7])))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return recipes_list
    #...........................................................................
    def select_by_id(self, id: int=0) -> DTO_Recipe:
        db_conn = self.db_handler.connect()
        query = dictionary_t_recipes["select_by_id"]%(id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
        if not result: return DTO_Recipe()
        result = list(result)
        user = DTO_Recipe(int(result[0]), str(result[1]), str(result[2]), str(result[3]), json.loads(str(result[4])), str(result[5]), str(result[6]), str(result[7]))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return user
    #...........................................................................
    def insert_new(self, name: str="-", description: str="-", image: str="-", info: dict={}, price: str="0.0", location: str="-", place_name: str="-") -> int:
        db_conn = self.db_handler.connect()
        query = dictionary_t_recipes["insert_new"]%(name, description, image, json.dumps(info), price, location, place_name)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                id = cursor.lastrowid
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return id
    #...........................................................................
    def update_by_id(self, id: int, name: str="-", description: str="-", image: str="-", info: dict={}, price: str="0.0", location: str="-", place_name: str="-") -> bool:
        db_conn = self.db_handler.connect()
        query = dictionary_t_recipes['update_by_id']%(name, description, image, json.dumps(info), price, location, place_name, id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return True
    #...........................................................................
    def delete_by_id(self, id: int) -> bool:
        db_conn = self.db_handler.connect()
        query = dictionary_t_recipes['delete_by_id']%(id)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return True
    #...........................................................................
#-------------------------------------------------------------------------------