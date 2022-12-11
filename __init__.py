from admin import *
from database import  *
import pandas as pd
from logging_configure import log_general
import sys
from log_in import *

if __name__ == "__main__":
    if '-h' in sys.argv:
        with open('help_info.txt', 'r') as f:
            contents = f.readlines()
        log_general.info(''.join(contents))
    # set up pandas for display
    pd.options.display.max_columns = None
    pd.options.display.width = 1000
    pd.options.display.max_colwidth = 115

    # initialize database
    connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    initiate(connection,cursor)
    test_initiate(connection,cursor)
    connection.close()

    # TESTS, delete later
    # admin = admin()
    # vol = volunteer()

    # admin.add_emergency_plan("plan4", "earthquake", "a big one", "UK")
    # admin.add_emergency_plan("plan5", "storm", "a small one", "Somewhere")
    # admin.add_camp("plan4", "camp1")
    # admin.add_camp("plan5", "camp1")
    # plans 1,2,3 are currently created directly in database.py
    # either delete those, or start from plan4 when demonstrating
    # admin.create_volunteer("plan4", "camp1", "first", "last", "12345678", "1,2", "test", "1111", True, True)
    # admin.create_volunteer("plan5", "camp1", "closed", "plan", "99999999", "3,4", "closed", "1111", True, True)
    # admin.deactivate_volunteer("closed")
    # vol.vols_send_message("closed", "plan2", "goodbye camp2!", plan_name = "plan2", camp_name = "camp1")
    # admin.close_emergency_plan("plan2")
    # admin.create_admin_announcement("I am admin")
    # vol.vols_send_message("test", "plan4", "hey admin!", admin_excl = True)
    # vol.vols_send_message("test", "plan4", "bruh", plan_name="plan4", camp_name="camp1")
    # vol.vols_send_message("test", "plan4", "yo camp1", plan_name="plan4", camp_name="camp1")
    # vol.vols_send_message("closed", "plan5", "hi guys", plan_name = "plan5", camp_name = "camp1")

    # admin.list_existing_plans()
    # admin.display_admin_exclusive_messages()
    #admin.delete_admin_exclusive_messages()
    # admin.display_messages_from_a_camp("plan4", "camp1")
    # admin.display_messages_from_a_camp("plan5", "camp1")
    # vol.vols_display_message(admin_anno = True)
    # vol.vols_display_message(plan_name = 'plan4', camp_name = 'camp1')
    # vol.vols_display_message(plan_name = 'plan5', camp_name = 'camp1')
    # vol.display_personal_profile("test")

    login()

    # following are just some tests
    #admin.close_emergency_plan("plan2")
    #admin.list_existing_plans()
    #admin.display_plan_summary("plan2")
    #admin.deactivate_volunteer("vol1")
    #admin.delete_volunteer("admin")
    #admin.raise_error_for_inexistence("emergency_plan",edit_check=True,plan_name="plan2")
    #admin.raise_error_for_existence("emergency_plan",plan_name = "plan1")
    #admin.display_admin_exclusive_messages()
    #admin.create_admin_announcement("i love you all")
    #admin.delete_admin_exclusive_messages()
    #admin.display_messages_from_a_camp("plan1","camp1")
    #.display_logs()

    # don't delete this
