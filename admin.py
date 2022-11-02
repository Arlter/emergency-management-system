import sqlite3
from database_utilities import *
from logging_configure import log_admin
import pandas as pd

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
    def display_plan_summary(self,pl_name:str):
        """
        used to display the details of a specific plan by entering its name
        :param pl_name: the name of plan
        :return:
        """
        sql_cmd = f"SELECT camp_name, num_of_volunteers, num_of_refugees FROM camp WHERE plan_name = '{pl_name}'"
        df = pd.DataFrame(self.cursor.execute(sql_cmd).fetchall(),
                         columns=['       Camp Name', '    Volunteers Number', '   Refugees Number'])
        print(df)
        return df.to_string()

    def list_existing_plans(self):
        """
        list all the plans that not closed yet
        :return: existing plans in a good string form that can be just printed
        """
        sql_cmd = f"SELECT * FROM emergency_plan "
        df = pd.DataFrame(self.cursor.execute(sql_cmd).fetchall(),
                          columns=['    Plan Name', '       Type', '     Description', '   Affected Area',
                                   '    Start Date ', '   Close Date'])

        print(df)
        return df.to_string()


    def add_emergency_plan(self, plan_name:str,type:str,description:str,geo_affected_area:str,start_date:str):
        """
        used to add emergency_plan. The last parameter from the table "close_date" is set to "NULL" by default.
        :param plan_name:
        :param type:
        :param description:
        :param geo_affected_area:
        :param start_date:
        :return: true if the operation is successful; error msg otherwise
        """
        try:
            self.cursor.execute(insert_sql_generation("emergency_plan",plan_name,type,description,geo_affected_area,start_date,"NULL"))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    def close_emergency_plan(self, close_date:str ,pl_name:str):
        """
        used to close an emergency plan by specifying its close_dates
        :param close_date: close date,
        :param pl_name: plan name
        :return:true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(update_sql_generation("emergency_plan","close_date",close_date,plan_name = pl_name))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

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
            return True

    def activate_volunteer(self, vol_usrname):
        """
        activate the account of the volunteer
        :param vol_usrname: the usrname of the volunteer
        :return: true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(update_sql_generation("volunteer","activated","True",username = vol_usrname))
            self.connection.commit()

        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    def delete_volunteer(self, vol_usrname):
        """
        delete the account of the volunteer
        :param vol_usrname:  the usrname of the volunteer
        :return: true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(f"DELETE FROM volunteer WHERE username = '{vol_usrname}' ")
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

