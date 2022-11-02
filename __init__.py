import logging

from admin import *
from database import  *
import pandas as pd
from logging_configure import log_none
import sys


if __name__ == "__main__":
    if '-h' in sys.argv:
        with open('help_info.txt', 'r') as f:
            contents = f.readlines()
        log_none.info(''.join(contents))
    # set up pandas for display
    pd.options.display.max_columns = None
    pd.options.display.width = 200

    # initialize database
    connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    initiate(connection,cursor)
    test_initiate(connection,cursor)
    # create an admin instance to use all the functionalities.
    admin = admin(connection, cursor)

    # following are just some tests
    admin.list_existing_plans()
    admin.deactivate_volunteer("vol1")
    admin.delete_volunteer("admin")
    #cursor.execute("UPDATE refugee_profile SET camp_name='camp2' WHERE profile_id='10000'")
    #connection.commit()

    # remember to close the cursor
    cursor.close()
