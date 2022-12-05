import sqlite3   
from terminal.VolunteerMenu import *
from volunteer import *
from terminal.log_in import *
from database import *
from admin import *


connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = connection.cursor()

initiate(connection,cursor)

admin = admin(connection, cursor)
vol = volunteer(connection,cursor)

# admin.add_emergency_plan("plan1", "earthquake", "a big one", "UK")
# admin.add_camp("plan1", "camp1")
# admin.create_volunteer("plan1", "camp1", "test", "volunteer", "12345678", "Monday,8-16", "test", "1111", True, True)

# min.list_existing_plans()

login(vol)