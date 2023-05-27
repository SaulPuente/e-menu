import pymysql
import logging

#-------------------------------------------------------------------------------
class Threading_DB_Connection(object):
    #...........................................................................
    """ Class: DB Connectors Creation. """
    #...........................................................................
    def __init__(self,p_dbconfig=None):
        self.local_dbconfig = p_dbconfig
    #...........................................................................
    def connect(self):
        database_username   = self.local_dbconfig["database_username"]
        database_password   = self.local_dbconfig["database_password"]
        database_name       = self.local_dbconfig["database_name"]
        host                = self.local_dbconfig["host"]
        port                = self.local_dbconfig["port"]

        connection = pymysql.connect(
            host=host,
            user=database_username,
            passwd=database_password,
            db=database_name,
            port=port,
            charset='utf8'
            )

        return connection

    def disconnect(self, connection):

        connection.close()