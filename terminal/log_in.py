from COMP0066.utility import bi_color_text
from COMP0066.terminal.color_utilities import colors
from COMP0066.logging_configure import *
from COMP0066.exceptions import *
import sqlite3
from COMP0066.terminal.AdminMenu import AdminMenu
from COMP0066.terminal.VolunteerMenu import VolunteerMenu
from COMP0066.terminal.GuestMenu import GuestMenu
from COMP0066.terminal.Deactivated import DeactivatedMenu
class login:

    def __init__(self):
        self.logqueue = []
        self.volunteer_username = None

        self.afterlogin = {
                '0': "AdminMenu()",
                '1': "VolunteerMenu(self.volunteer_username)",
                '2': "GuestMenu()",
                '3': "deactivatedMenu(self.volunteer_username)"}

        self.logqueue.append('self.trylogin()')

        while len(self.logqueue)!= 0:
            temp = eval(self.logqueue[0])
            if temp:
                if temp.Ifback == True:
                    self.logqueue.append('self.trylogin()')
            self.logqueue = self.logqueue[1:]

    def trylogin(self):
        connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        cursor = connection.cursor()


        SuccessLog = False
        CurrentRole = None
        while SuccessLog == False:
            '''Log in'''
            print(colors.bg.green, "Log in", colors.reset)
            UserNameinput = input("Username: ")
            Passwordinput = input("Password: ")
            Search = "SELECT * FROM volunteer WHERE username = " + "'" + UserNameinput + "'" + " and password = " + "'" + Passwordinput + "'"
            cursor.execute(Search)

            try:
                result = cursor.fetchone()
                if result:
                    if result[8] == "FALSE":
                        log_general.info(f"{colors.fg.red}Your account is deactivated, please contact admin{colors.reset}")
                        CurrentRole = '3'
                        self.volunteer_username = UserNameinput
                        SuccessLog = True

                    else:

                        if UserNameinput == 'admin':
                            log_general.info(f"\n{colors.fg.green} 🙌 Welcome! Your role is Admin 🙌{colors.reset}\n")
                            CurrentRole = '0'
                            SuccessLog = True


                        elif UserNameinput == 'guest':
                            log_general.info(f"\n{colors.fg.green} 🙌 Welcome! Your role is Guest 🙌{colors.reset}\n")
                            CurrentRole = '2'
                            SuccessLog = True

                        else:
                            log_general.info(f"\n{colors.fg.green} 🙌 Welcome! Your role is Volunteer 🙌{colors.reset}\n")
                            CurrentRole = '1'
                            self.volunteer_username = UserNameinput
                            SuccessLog = True

                else:
                    raise invalid_login

            except invalid_login as e:
                log_general.error(bi_color_text(f"{e}", font_color='r'))

        self.logqueue.append(self.afterlogin[CurrentRole])