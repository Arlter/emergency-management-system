import sqlite3
from database_utilities import *
from logging_configure import log_volunteer
import pandas as pd
import logging

class volunteer:
   
           
    def __init__(self):
        """
        pass the connection and cursor to complete the operations on the db.
        :param connection: connection
        :param cursor: cursor
        """
        # self.connection = connection
        # self.cursor = cursor
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

    def edit_personal_profile(self, username: str, logger: logging.Logger, **kwargs ) -> bool:
        """
        Collect the info and update the volunteer table
        example: edit_personal_profile("vol4", plan_name="plan1", camp_name="camp2")
                 update plan name and camp name to be 'plan1' and 'camp2' respectively
                 to volunteer 'vol4'
        :param username: the volunteer's username who would like to make the update
        :param **kwargs: attribute = value bindings you would like to update
        NOTE: if you would like to update availability, make sure that the string
              is formatted as "$which_day,$start_time-$end_time" without any space
              like "Monday,8-16"
        """
        args = []
        n = len(self.time_slots)
        for key, value in kwargs.items():
            args.append(key)
            args.append(value)
        # print(args)
        sql = update_sql_generation("volunteer", *args, username=username)
        # print(sql)
        try:
            self.cursor.execute(sql).fetchall()
            # print(result)
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(e)
            return False
        else:
            return True

        # self.cursor.execute(sql)
        # self.connection.commit()

    def availability(self, time: str, logger: logging.Logger, plan_name = None, camp_name = None) -> list:
        """
        the function searches for volunteers fully available in a time period
        :param time: a string that should be formatted like "$which_day,$start_time-$end_time"
                     start time and end time can be same to make immediate sampling
                     there should be no space in the string
        :param plan_name: a string which specify the plan name, default none
        :param plan_name: a string which specify the camp name, default none
        :return: a list containing available volunteer usernames in given period
        """
        res = []
        if ' ' in time: # there should be no space in the string
            logger.error("Space detected in parameter 'time'")
            return res
        try:
            t_day, c = time.split(',')
            [t_start_time, t_end_time] = c.split('-')
        except ValueError as e:
            logger.error(e)
        if int(t_start_time) > int(t_end_time):
            logger.error("Invalid time period input")
            return res
        if t_day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            logger.error("Invalid day input")
            return res
        t_start_time = int(t_start_time)
        t_end_time = int(t_end_time)
        dic = {}
        if plan_name != None:
            dic['plan_name'] = plan_name
        if camp_name != None:
            dic['camp_name'] = camp_name
        sql = select_sql_generation("volunteer", "username", "availability", *dic)
        # print(sql)
        result = self.cursor.execute(sql).fetchall()[2:] # [1:] is to exclude admin row and guest row
        self.connection.commit()
        # print(result)
        for tuples in result:
            vol = tuples[0]
            day, d = tuples[1].split(',')
            [start_time, end_time] = d.split('-')
            start_time = int(start_time)
            end_time = int(end_time)
            # print("tup:", day, start_time, end_time)
            # print("t:", t_day, t_start_time, t_end_time)
            if day == t_day and start_time <= t_start_time and end_time >= t_end_time:
                res.append(vol)
        return res

        

if __name__ == "__main__":
    #test for edit_personal_profile and availability
    vol1 = volunteer()
    vol1.edit_personal_profile('vol1', log_volunteer, availability="Monday,8-16")
    vol1.edit_personal_profile('vol2', log_volunteer, availability="Tuesday,9-10")
    vol1.edit_personal_profile('vol3', log_volunteer, availability="Wednesday,11-12")
    vol1.edit_personal_profile('vol4', log_volunteer, availability="Thursday,15-18")
    print(vol1.availability("Monday,8-15", log_volunteer))
    print(vol1.availability("Thursday,15-15", log_volunteer))

            
    