import sqlite3
from datetime import datetime
from database_utilities import *
from logging_configure import log_admin
import pandas as pd
from exceptions import *
from terminal.color_utilities import  *
class admin:
    """
    Since the structure of the program is reformed, we now have to instantiate the admin as an object
    to use the methods of it. Also, be aware that no class methods exist now
    """
    def __init__(self,connection,cursor):
        """
        pass the connection and cursor to complete the operations on the db.
        :param connection: connection
        :param cursor: cursor
        """
        self.connection = connection
        self.cursor = cursor

#################################The following two methods for general single-value check ##############################
    def raise_error_for_existence(self,table_name,**kwargs) -> bool:
        """
        This method is called when you want to verify inexistence of a tuple. It will raise an exception if
        the tuple has existed and return False.

        :param table_name: table name
        :param kwargs:  pass in the form of attr_name = attr_value
        :return:true if the value does not exist, false otherwise.
        """
        try:
            sql_cmd = select_sql_generation(table_name, "COUNT(*)", **kwargs)
            sql_cmd = select_sql_generation(table_name, "COUNT(*)", **kwargs)
            res = self.cursor.execute(sql_cmd).fetchall()[0][0]
            if res != 0: # exists, raise an exception
                raise already_exists(table_name,**kwargs)
        except already_exists as e:
            log_admin.error(e)
            return False
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    def raise_error_for_inexistence(self, table_name:str, edit_check = False, **kwargs) -> bool:
        """
        This method is called when you want to verify existence of a tuple. It will raise an error if
        the tuple has not existed and return False.This method also adds a prohibitor(edit_check)to prevent attempts on editting
        a closed emergency plan.
        :param table_name: table name
        :param kwargs:  pass in the form of attr_name = attr_value
        :return:true if the value does not exist, false otherwise.
        """
        try:
            if edit_check and table_name == "emergency_plan" and "plan_name" in kwargs.keys() and self.cursor.execute(f"SELECT COUNT(*) FROM emergency_plan WHERE close_date <> null and plan_name = '{kwargs['plan_name']}'").fetchall()[0][0] > 0 :
                raise closed_plan()
            sql_cmd = select_sql_generation(table_name, "COUNT(*)", **kwargs)
            res = self.cursor.execute(sql_cmd).fetchall()[0][0]
            if res == 0: # does not exist, raise an exception
                raise absent(table_name,**kwargs)
        except closed_plan as e:
            log_admin.error(e)
            return False
        except absent as e:
            log_admin.error(e)
            return False
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

#################################The following Methods are for plan & camp management system############################
    # A method for plan management system
    def display_plan_summary(self,pl_name:str):
        """
        used to display the details of a specific plan by entering its name
        :param pl_name: the name of plan
        :return: True if the operation encounters no error, false otherwise
        """
        try:
            sql_cmd = select_sql_generation("camp","camp_name, num_of_volunteers, num_of_refugees", plan_name=pl_name)
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res,
                             columns=['       Camp Name', '    Volunteers Number', '   Refugees Number'])
                df.index = [''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info(f"* No details are found given the plan name {pl_name} ")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for plan management system
    def list_existing_plans(self):
        """
        list all the plans including archived ones
        :return: existing plans in a good string form that can be just printed
        """
        try:
            sql_cmd = select_sql_generation("emergency_plan","*")
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res,
                                  columns=['    Plan Name', '       Type', '     Description', '   Affected Area',
                                           '    Start Date ', '   Close Date'])
                df.index = [''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info(f"* No plans are found ")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for camp management system
    def add_camp(self,plan_name:str ,*camp_names):
        """
        used to add camp(s) to a plan
        :param plan_name: plan name
        :param camp_names: all camp names to be added
        :return: true if the operation is successful false otherwise
        """
        try:
            for name in camp_names:
                self.cursor.execute(insert_sql_generation("camp",plan_name=plan_name,camp_name=name))
                self.connection.commit()
        except sqlite3.IntegrityError as e:
            log_admin.error(e)
            return False
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The addition of {', '.join([name for name in camp_names])} to the plan {plan_name} is successful ")
            return True

    # A method for plan management system
    def add_emergency_plan(self, plan_name:str,type:str,description:str,geo_affected_area:str,start_date:str):
        """
        used to add emergency_plan. The last parameter from the table "close_date" is set to "NULL" by default.
        :param plan_name: plan name
        :param type: emergency type
        :param description: description
        :param geo_affected_area: location
        :param start_date: plan start date
        :return: true if the operation is successful; error msg otherwise
        """
        try:
            self.cursor.execute(insert_sql_generation("emergency_plan",plan_name=plan_name,plan_type=type,plan_description=description,geo_area=geo_affected_area))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The addition of the plan {plan_name} is successful ")
            return True

    # A method for plan management system
    def close_emergency_plan(self,pl_name:str):
        """
        used to close an emergency plan by specifying its close_dates
        :param pl_name: plan name
        :return:true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(update_sql_generation("emergency_plan","close_date",datetime.today().strftime('%Y-%m-%d'),plan_name = pl_name))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The close operation of the plan {pl_name} is successful ")
            return True

##########################The following Methods are for volunteer management system####################################
    # A method for volunteer management system
    def deactivate_volunteer(self, vol_usrname):
        """
        deactivate the account of the volunteer
        :param vol_usrname: the usrname of the volunteer
        :return:true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(update_sql_generation("volunteer","activated","False",username = vol_usrname))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The deactivation of the volunteer account {vol_usrname} is successful ")
            return True

    # A method for volunteer management system
    def activate_volunteer(self, vol_usrname):
        """
        activate the account of the volunteer
        :param vol_usrname: the username of the volunteer account
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            self.cursor.execute(update_sql_generation("volunteer","activated","True",username = vol_usrname))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The activation of the volunteer account {vol_usrname} is successful ")
            return True

    # A method for volunteer management system
    def delete_volunteer(self, vol_usrname):
        """
        delete the account of the volunteer
        :param vol_usrname:  the username of the volunteer account
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            self.cursor.execute(f"DELETE FROM volunteer WHERE username = '{vol_usrname}' ")
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The deletion of the volunteer account '{vol_usrname}' is successful")
            return True
##################################The following Methods are for message management system###############################
    # A method for message management system:
    def display_admin_exclusive_messages(self):
        """
        used to display all the messages exclusive to admin
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"{select_sql_generation('message', 'message_id','time','username','content', admin_exclusive='TRUE', admin_announced='FALSE')} ORDER BY message_id ASC"
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res,
                                  columns=['    Message ID','       time','    username','    Message Content'])
                df.index = [''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info("* No messages are found given the plan name and camp name ")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for message management system:
    def create_admin_announcement(self, announcement:str):
        """
        used to create an admin announcement by an admin. This annoucement should be visible by every volunteer
        :param announcement: string of the announcement
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES(null, null,'admin','TRUE','FALSE','{announcement}')"
            self.cursor.execute(sql_cmd)
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for message management system:
    def delete_admin_exclusive_messages(self):
        """
        used to delete all the admin_exclusive messages if they exist
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"DELETE FROM message WHERE admin_exclusive='TRUE' and admin_announced='FALSE'"
            self.cursor.execute(sql_cmd)
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for message management system:
    def display_messages_in_a_plan(self, plan_name):
        """
        used to display messages from the same emergency plan
        :param plan_name: plan name
        :return:True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"{select_sql_generation('message', 'time','username','plan_name','content', plan_name = plan_name,admin_exclusive='FALSE', admin_announced='FALSE')} ORDER BY message_id ASC"
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res,
                                  columns=['    Post Time','    Account','       Plan Name', '                Message Content'])
                df.index =[''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info("* No messages are found given the plan name and camp name ")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for message management system:
    def display_messages_from_a_camp(self, plan_name, camp_name):
        """
        used to display all the messages coming from the same camp
        :param plan_name: plan name
        :param camp_name: camp name
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"{select_sql_generation('message', 'time','username','plan_name','content', plan_name = plan_name, camp_name=camp_name,admin_exclusive='FALSE', admin_announced='FALSE')} ORDER BY message_id ASC"
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res)!=0:
                df = pd.DataFrame(res,
                                  columns=['    Post Time','    Account','      Plan Name','  Camp Name' '            Message Content'])
                df.index = [''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info(f"{colors.bg.green}* No messages are found given the plan name and camp name {colors.reset}")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

#######################################The following Methods are for logging management system#######################
    # A method for logging system
    def display_logs(self):
        """
        display the running logs from this time.
        :return: True if the operation encounters no exception, false otherwise
        """
        try:
            f = open ("logging.log", 'r')
        except FileNotFoundError:
            log_admin.info(f"File  is not found.  Aborting")
            return False
        except OSError:
            log_admin.info(f"OS error occurred trying to open 'logging.log'")
            return False
        except Exception as err:
            log_admin.info(f"Unexpected error opening 'logging.log' is", repr(err))
            return False
        else:
            with f:
                logs = f.readlines()
            log_admin.info(f"* The operation is successful. The logs will be displayed below \n")
            log_admin.info(''.join(logs))
            return True