import sqlite3   
from terminal.VolunteerMenu import *
from volunteer import *
from terminal.log_in import *
from database import *
from admin import *


connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = connection.cursor()

#initiate(connection,cursor)

admin = admin() # delete later
vol = volunteer() # delete later

# admin.add_emergency_plan("plan1", "earthquake", "a big one", "UK")
# admin.add_emergency_plan("plan4", "storm", "a small one", "Somewhere")
# admin.add_camp("plan4", "camp4")
# admin.create_volunteer("plan4", "camp4", "closed2", "plan", "12345678", "Monday,8-16", "close2", "1111", True, True)
admin.close_emergency_plan("plan4")
# admin.add_camp("plan1", "camp1")
# admin.create_volunteer("plan1", "camp1", "test", "volunteer", "12345678", "Monday,8-16", "test", "1111", True, True)
# admin.create_admin_announcement("i love you all")
# admin.create_volunteer("plan1", "camp1", "iamvol2", "volunteer", "12345678", "Monday,8-16", "vol2", "1111", True, True)
# vol.vols_send_message("test", "bruh", plan_name="plan1", camp_name="camp1")
# vol.vols_send_message("vol2", "hi guys", plan_name = "plan1", camp_name = "camp1")

#admin.list_existing_plans()
admin.display_admin_exclusive_messages()
# admin.delete_admin_exclusive_messages()
admin.display_messages_from_a_camp("plan4", "camp4")
#vol.vols_display_message(plan_name = 'plan4', camp_name = 'camp4')

# login(vol)
login()