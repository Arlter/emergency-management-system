from database import *
import sqlite3
from database_utilities import *
from logging_configure import log_volunteer
import pandas as pd
from exceptions import *

class refugee_profile:

    def __init__(self, plan_name, camp_name, first_name, last_name, family_number, medical_condition, profile_ID):
        self.plan_name = plan_name
        self.camp_name = camp_name
        self.first_name = first_name
        self.last_name = last_name
        self.family_number = family_number
        self.medical_condition = medical_condition
        self.profile_ID = profile_ID


class volunteer:

    def __init__(self,connection,cursor):
       """
       pass the connection and cursor to complete the operations on the db.
       :param connection: connection
       :param cursor: cursor
       """
       self.connection = connection
       self.cursor = cursor

    def raise_error_for_existence(self, table_name, **kwargs) -> bool:
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
            if res != 0:  # exists, raise an exception
                raise already_exists(table_name, **kwargs)
        except already_exists as e:
            log_volunteer.error(e)
            return False
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        else:
            return True

    def raise_error_for_inexistence(self, table_name: str, edit_check=False, **kwargs) -> bool:
        """
        This method is called when you want to verify existence of a tuple. It will raise an error if
        the tuple has not existed and return False.This method also adds a prohibitor(edit_check)to prevent attempts on editting
        a closed emergency plan.
        :param table_name: table name
        :param kwargs:  pass in the form of attr_name = attr_value
        :return:true if the value does not exist, false otherwise.
        """
        try:
            if edit_check and table_name == "refugee_profile" and "profile_id" in kwargs.keys() and self.cursor.execute(
                    f"SELECT COUNT(*) FROM refugee_profile WHERE profile_id = '{kwargs['profile_id']}'").fetchall()[
                0][0] > 0:
                raise closed_plan()
            sql_cmd = select_sql_generation(table_name, "COUNT(*)", **kwargs)
            res = self.cursor.execute(sql_cmd).fetchall()[0][0]
            if res == 0:  # does not exist, raise an exception
                raise absent(table_name, **kwargs)
        except closed_plan as e:
            log_volunteer.error(e)
            return False
        except absent as e:
            log_volunteer.error(e)
            return False
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        else:
            return True

    def add_emergency_plan(self, plan_name: str, type: str, description: str, geo_affected_area: str, start_date: str):
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
            self.cursor.execute(
                insert_sql_generation("emergency_plan", plan_name, type, description, geo_affected_area, start_date,
                                      "NULL"))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    def create_emergency_profile(self, plan_name, camp_name, first_name, last_name, family_number, medical_condition,profile_ID):
       try:
          self.cursor.execute(insert_sql_generation("refugee_profile", plan_name, camp_name, first_name, last_name,family_number, medical_condition, profile_ID))
          self.connection.commit()
        except sqlite3.Error as e:
          log_volunteer.error(e)
        else:
          return True

    def edit_emergency_profile(self):
       try:
          self.cursor.execute(update_sql_generation(refugee_profile,,,))
          self.connection.commit()
        except sqlite3.Error as e:
          log_volunteer.error(e)
        else:
          return True

    def view_emergency_profile(self):
       try:
          self.cursor.execute(update_sql_generation(refugee_profile, )
          self.connection.commit()
        except sqlite3.Error as e:
          log_volunteer.error(e)
        else:
          return True


    def edit_personal_profile(self, username: str, **kwargs) -> bool:
        """
        Collect the info and update the volunteer table
        example: edit_personal_profile("vol4", plan_name="plan1", camp_name="camp2")
        update plan name and camp name to be 'plan1' and 'camp2' respectively
        to volunteer 'vol4'
        :param username: the volunteer's username who would like to make the update
        :param **kwargs: attribute = value bindings you would like to update
        """
        args = []
        for key, value in kwargs.items():
            args.append(key)
            args.append(value)
        # print(args)
        sql = update_sql_generation("volunteer", *args, username=username)
        # print(sql)
        try:
            self.cursor.execute(sql).fetchall()
            print(result)
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        else:
            return True  # todo: check if the database is really updated as expected


def availability(self) -> bool:
    pass

