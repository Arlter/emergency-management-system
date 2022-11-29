from color_utilities import *
from Admin_and_Volun.admin import admin
from AdminMenu import *
from VolunteerMenu import *
import sqlite3

class login():

    def __init__(self):
        self.logqueue = []

        self.afterlogin = {
                '0': "AdminMenu()",
                '1': "VolunteerMenu()",
                '2': "GuestMenu()"}


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
        Admin = admin(connection,cursor)



        SuccessLog = False
        CurrentRole = None
        while SuccessLog == False:
            '''Log in'''
            print(colors.bg.green, "Log in", colors.reset)
            UserNameinput = input("Username: ")
            Passwordinput = input("Password: ")
            Search = "SELECT * FROM volunteer WHERE username = " + "'" + UserNameinput + "'" + " and password = " + "'" + Passwordinput + "'"
            cursor.execute(Search)


            if cursor.fetchone():

                if UserNameinput == 'admin':
                    print(colors.fg.green, "Welcome! Your role is Admin", colors.reset)
                    CurrentRole = '0'
                    SuccessLog = True


                elif UserNameinput == 'guest':
                    print(colors.fg.green, "Welcome! Your role is Guest", colors.reset)
                    CurrentRole = '2'
                    SuccessLog = True

                else:
                    print(colors.fg.green, "Welcome! Your role is Volunteer", colors.reset)
                    CurrentRole = '1'
                    SuccessLog = True

            else:
                print(colors.fg.red, "Invalid login", colors.reset)

        self.logqueue.append(self.afterlogin[CurrentRole])