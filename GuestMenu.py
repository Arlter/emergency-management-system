import sqlite3
from volunteer import *
from exceptions import *
from logging_configure import *
import database_utilities
from color_utilities import *

class GuestMenu:
    def __init__(self):
        self.Ifback = False
        self.queue = []
        self.Guest = volunteer()
        self.username = 'guest'

        self.queue.append('self.Guest_request()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]


    def quit(self):
        self.Guest.connection.close()

    def Guest_request(self):
        request = input("Send the message to admin, or enter b to go back: ")
        if request == 'b':
            self.Ifback = True
        else:
            self.Guest.vols_send_message(self.username, 'null', request, admin_excl=True)
            self.queue.append('self.quit()')
            self.Ifback = True