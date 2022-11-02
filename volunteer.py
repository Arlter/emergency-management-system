import sqlite3
from database_utilities import *
from logging_configure import log_volunteer
import pandas as pd

class volunteer:

    def __init__(self,connection,cursor):
        """
        pass the connection and cursor to complete the operations on the db.
        :param connection: connection
        :param cursor: cursor
        """
        self.connection = connection
        self.cursor = cursor