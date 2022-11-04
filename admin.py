import sqlite3
from database_utilities import *
from logging_configure import log_admin
import pandas as pd
from exceptions import *
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
            if edit_check and table_name == "emergency_plan" and "plan_name" in kwargs.keys() and self.cursor.execute(f"SELECT COUNT(*) FROM emergency_plan WHERE close_date <> 'NULL' and plan_name = '{kwargs['plan_name']}'").fetchall()[0][0] > 0 :
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


    def display_plan_summary(self,pl_name:str):
        """
        used to display the details of a specific plan by entering its name
        :param pl_name: the name of plan
        :return: A string.  Depending on how terminals want to do with it, return values might change
        """
        sql_cmd = select_sql_generation("camp","camp_name, num_of_volunteers, num_of_refugees", plan_name=pl_name)
        df = pd.DataFrame(self.cursor.execute(sql_cmd).fetchall(),
                         columns=['       Camp Name', '    Volunteers Number', '   Refugees Number'])
        print(df)
        return df.to_string()


    def list_existing_plans(self):
        """
        list all the plans including archived ones
        :return: existing plans in a good string form that can be just printed
        """
        sql_cmd = select_sql_generation("emergency_plan","*")
        df = pd.DataFrame(self.cursor.execute(sql_cmd).fetchall(),
                          columns=['    Plan Name', '       Type', '     Description', '   Affected Area',
                                   '    Start Date ', '   Close Date'])
        print(df)
        return df.to_string()

    def add_camp(self,plan_name:str ,*camp_names):
        """
        used to add camps to a plan
        :param plan_name:
        :param camp_names: used for adding multiple camps at a time
        :return: true if the operation is successful false otherwise
        """
        try:
            for name in camp_names:
                self.cursor.execute(insert_sql_generation("camp",plan_name,name,0,0,"FALSE"))
                self.connection.commit()
        except sqlite3.IntegrityError as e:
            log_admin.error(e)
            return False
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

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

