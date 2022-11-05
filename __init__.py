import logging

from admin import *
from database import  *
import pandas as pd
from logging_configure import log_general
import sys


if __name__ == "__main__":
    if '-h' in sys.argv:
        with open('help_info.txt', 'r') as f:
            contents = f.readlines()
        log_general.info(''.join(contents))
    # set up pandas for display
    pd.options.display.max_columns = None
    pd.options.display.width = 1000

    # initialize database
    connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    initiate(connection,cursor)
    test_initiate(connection,cursor)
    # create an admin instance to use all the functionalities.
    admin = admin(connection, cursor)


    # following are just some tests
    admin.close_emergency_plan("plan2")
    admin.list_existing_plans()
    admin.display_plan_summary("plan2")
    admin.deactivate_volunteer("vol1")
    admin.delete_volunteer("admin")
    admin.raise_error_for_inexistence("emergency_plan",edit_check=True,plan_name="plan2")
    admin.raise_error_for_existence("emergency_plan",plan_name = "plan1")
    admin.display_admin_exclusive_messages()
    admin.create_admin_announcement("i love you all")
    admin.delete_admin_exclusive_messages()
    admin.display_messages_from_a_camp("plan1","camp1")
    #admin.display_logs()
    cursor.close()
