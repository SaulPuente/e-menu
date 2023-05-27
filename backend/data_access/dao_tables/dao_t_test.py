#-------------------------------------------------------------------------------
from ..mysql_queries.q_dao_test import dictionary_t_test
from ...data_transfer.dto_test import DTO_Test
#-------------------------------------------------------------------------------
class DAO_T_Test(object):
    #...........................................................................
    """ Class: DAO access to companies table. """
    #...........................................................................
    def __init__(self,db_handler):
        self.db_handler     = db_handler
    #...........................................................................
    def select_all(self):
        db_conn = self.db_handler.connect()
        query = dictionary_t_test["select_all"]
        print(query)
        with db_conn as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
        test_list = []
        print(results)
        for result in results:
            result = list(result)
            test_list.append(DTO_Test(int(result[0]), str(result[1]), str(result[2])))
        if db_conn.open: self.db_handler.disconnect(db_conn)
        return test_list
    #...........................................................................
#-------------------------------------------------------------------------------