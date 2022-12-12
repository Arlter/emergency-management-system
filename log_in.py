from color_utilities import *
from admin import admin
from AdminMenu import *
from VolunteerMenu import *
from deactivated import *
from GuestMenu import *
import sqlite3

class login():

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
                            log_general.info(f"{colors.fg.green}Welcome! Your role is Admin{colors.reset}")
                            CurrentRole = '0'
                            SuccessLog = True


                        elif UserNameinput == 'guest':
                            log_general.info(f"{colors.fg.green}Welcome! Your role is Guest{colors.reset}")
                            CurrentRole = '2'
                            SuccessLog = True

                        else:
                            log_general.info(f"{colors.fg.green}Welcome! Your role is Volunteer{colors.reset}")
                            CurrentRole = '1'
                            self.volunteer_username = UserNameinput
                            SuccessLog = True

                else:
                    log_general.error(f"{colors.fg.red}Invalid login{colors.reset}")
                    raise option_not_existed

            except option_not_existed as e:
                log_admin.error(e)


        self.logqueue.append(self.afterlogin[CurrentRole])