import sqlite3
from volunteer import *
from exceptions import *
from logging_configure import *
import utility
from color_utilities import *

class deactivatedMenu:

    def __init__(self, username):
        self.Ifback = False
        self.queue = []
        self.vol_instance = volunteer()
        self.username = username

        plansql = select_sql_generation("volunteer", "plan_name", username = self.username)

        self.plan = self.vol_instance.cursor.execute(plansql).fetchall()[0][0]
        self.vol_instance.connection.commit()
        
        self.queue.append('self.deactivated()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]


    def quit(self):
        self.vol_instance.connection.close()
    def deactivated(self):
        message = input("Send a message to admin, or enter b to go back: ")
        if message == "b":
            self.Ifback = True
        else:
            self.vol_instance.vols_send_message(self.username, self.plan, message, admin_excl=True)
            self.queue.append('self.quit()')
            self.Ifback = True
