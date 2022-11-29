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
    pd.options.display.width = 200

    # initialize database
    connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    initiate(connection,cursor)
    test_initiate(connection,cursor)
    # create an admin instance to use all the functionalities.
    admin = admin(connection, cursor)


    # following are just some tests
    #$plan_name, $camp_name, $first_name, $last_name, $phone_num, $availability, $username, $password, $activated, $reassignable
    #admin.create_volunteer("plan1", "camp2", "kien", "hang", 1234, "Monday,8-16", "kien", "password", "activated", "reassignable")
    #admin.edit_personal_profile("kien", plan_name="plan1", camp_name="camp1")
    admin.password_change("kien","newpass")
    admin.view_volunteer_details("kien")
    # admin.list_existing_plans()
    # admin.display_plan_summary("plan2")
    #.display_logs()
    cursor.close()
