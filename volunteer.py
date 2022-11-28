import sqlite3
from database_utilities import *
from logging_configure import log_volunteer
import pandas as pd
import logging
from exceptions import *

# functions available: (name - corresponding function)
# 1. create refugee profile - create_refugee_profile
# 2. edit refugee profile - update_refugee_profile
# 3. display all information about certain camp name - list_emergency_profile
# 4. display all information about certain refugee - display_emergency_profile
# 5. edit volunteer's personal profile - edit_personal_profile
# 6. create volunteer's personal profiel - create_personal_profile
# 7. check availability over certain period and certain camp or plan (if possible) - availability
# 8. send message as a volunteer (to other vols or to the admin) - vols_send_message
# 9. display message of other vols or announcements of admin - vols_display_message


class volunteer:

    def __init__(self, connection, cursor):
        """
        pass the connection and cursor to complete the operations on the db.
        :param connection: connection 
        :param cursor: cursor
        """
        self.connection = connection
        self.cursor = cursor

    def raise_error_for_existence(self, table_name,logger = log_volunteer, **kwargs) -> bool:
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
            logger.error(e)
            return False
        except sqlite3.Error as e:
            logger.error(e)
            return False
        else:
            return True

    def __raise_error_for_inexistence(self, table_name: str, edit_check=False, **kwargs) -> bool:
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

    def create_refugee_profile(self, plan_name, camp_name, first_name, last_name, family_number, medical_condition,
                                 profile_ID):
        try:
            self.cursor.execute(
                insert_sql_generation("refugee_profile", plan_name, camp_name, first_name, last_name, family_number,
                                      medical_condition, profile_ID))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        else:
            return True

    def update_refugee_profile(self, attribute_name, new_val, refugee_ID):
        try:
            self.cursor.execute(update_sql_generation("refugee_profile", attribute_name, new_val, refugee_ID))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        else:
            return True

    def list_emergency_profile(self, camp_name):
        try:
            sql_cmd = select_sql_generation('refugee_profile', '*', camp_name = camp_name)
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res, columns = ['Camp name', 'First name', 'Last name', 'Number of family members', 'Medical condition(s)'])
                df.index = ['']*len(df)
                log_volunteer.info(f"\n{df}\n")
            else:
                log_volunteer.info(f'*No refugee profiles found in the current camp {camp_name}')
        except sqlite3.Error as e:
            log_volunteer.error(e)
        else:
            return True

    def display_emergency_profile(self, camp_name, first_name ='*', last_name ='*', family_num = '*', medical_condition= '*'):
        try:
            sql_cmd = select_sql_generation('refugee_profile', '*', camp_name = camp_name, first_name = first_name, last_name = last_name, family_num = family_num, medical_condition = medical_condition)
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res, columns = ['Camp name', 'First name', 'Last name', 'Number of family members', 'Medical condition(s)'])
                df.index = ['']*len(df)
                log_volunteer.info(f'\n{df}\n')
            else:
                log_volunteer.info(f'No profiles found.')
        except sqlite3.Error as e:
                log_volunteer.error(e)
        else:
            return True

    def create_personal_profile(self, *attr):
        """
        Create a new personal profile
        :param *attr: the new volunteer information, with the order as: 
                    $plan_name, $camp_name, $first_name, $last_name, $phone_num, $availability, $username, $password, $activated, $reassignable
        NOTE: if you would like to specify availability, make sure that the string
              is formatted as "$which_day,$start_time-$end_time" without any space
              like "Monday,8-16"
        """
        try:
            if not self.raise_error_for_existence("volunteer", username=attr[6]):
                return False
            sql = insert_sql_generation("volunteer", *attr)
            res = self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        else:
            return True


    def edit_personal_profile(self, username: str, logger= log_volunteer, **kwargs) -> bool:
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

    def availability(self, time: str, logger=log_volunteer, plan_name=None, camp_name=None) -> list:
        """
        the function searches for volunteers fully available in a time period
        :param time: a string that should be formatted like "$which_day,$start_time-$end_time"
                     start time and end time can be same to make immediate sampling
                     there should be no space in the string
        :param plan_name: a string which specify the plan name, default none
        :param plan_name: a string which specify the camp name, default none
        :return: a list containing available volunteer usernames in given period
                 if there is error return false
        """
        res = []
        if ' ' in time:  # there should be no space in the string
            logger.error("Space detected in parameter 'time'")
            return False
        try:
            t_day, c = time.split(',')
            [t_start_time, t_end_time] = c.split('-')
        except ValueError as e:
            logger.error(e)
        if int(t_start_time) > int(t_end_time):
            logger.error("Invalid time period input")
            return False
        if t_day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            logger.error("Invalid day input")
            return False
        t_start_time = int(t_start_time)
        t_end_time = int(t_end_time)
        dic = {}
        if plan_name != None:
            dic['plan_name'] = plan_name
        if camp_name != None:
            dic['camp_name'] = camp_name
        sql = select_sql_generation("volunteer", "username", "availability", *dic)
        # print(sql)
        try:
            result = self.cursor.execute(sql).fetchall()[2:]  # [2:] is to exclude admin row
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(e)
            return False
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
        if len(res) == 0:
            logger.info("There is no satisfied volunteer in that period.")
            return res
        else:
            logger.info(f"In that period, The satisfied volunteers are {res}.")
            return res

    def vols_display_message(self, admin_anno = False, **kwargs) -> bool:
        """
        :param **kwargs: bindings that specify message from which channel.
        :param admin_anno: default false, if want to display announcements from admin, set it to true
        :param vol_usrname: the sender volunteer's username
        example: vols_display_message(plan_name = 'plan1', camp_name = 'camp1')
        displays message from camp1 and plan1
        example2: vols_display_message(admin_anno = True)
        displays message from admin
        NOTE: please do not set true to admin_anno and specify **kwargs at the same time
        """
        # print(not admin_anno)
        if not admin_anno:
            sql = select_sql_generation("message", "time", "message_id", "username", "content", **kwargs)
        elif admin_anno and len(kwargs) == 0:
            sql = select_sql_generation("message", "time", "message_id", "username", "content", admin_announced="TRUE", admin_exclusive="FALSE")
        elif admin_anno and len(kwargs) != 0:
            log_volunteer.error("Please do not specify the camp_name (or plan_name) and the admin_anno at the same time!")
            return False
        try:
            result = self.cursor.execute(sql).fetchall()
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        if len(result) != 0:
            df = pd.DataFrame(result,columns=['    Message ID','       time','    username','    Message Content'])
            df.index = [''] * len(df)
            log_volunteer.info(f"\n{df}\n")
            return True
        else:
            log_volunteer.info("* No messages are found given specified information.")
            return False
    
    def vols_send_message(self, vol_usrname: str, content: str, admin_excl=False, **kwargs) -> bool:
        """
        :param **kwargs: bindings that specify message from which channel. (plan_name and camp_name)
        :param admin_excl: default false, if want to send message to admin, set it to true
        example: vols_send_message(plan_name = 'plan1', camp_name = 'camp1')
        sends message from camp1 and plan1
        example2: vols_send_message(admin_anno = True)
        sends message from admin
        NOTE: please do not set true to admin_anno and specify **kwargs at the same time
        """
        if not self.__raise_error_for_inexistence("volunteer", username=vol_usrname):
            return False
        if not admin_excl:
            sql = f"""INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) 
                      VALUES('{kwargs['plan_name'] if 'plan_name' in kwargs.keys() else 'null'}', '{kwargs['camp_name'] if 'camp_name' in kwargs.keys() else 'null'}','{vol_usrname}','FALSE', 'FALSE','{content}')"""     
        elif admin_excl and len(kwargs) == 0:
            sql = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES(null, null, '{vol_usrname}', 'FALSE', 'TRUE', '{content}')"  
        elif admin_excl and len(kwargs) != 0:
            log_volunteer.error("Please do not specify the camp_name (or plan_name) and the admin_excl at the same time!")
            return False
        # print(sql)
        try:
            result = self.cursor.execute(sql).fetchall()
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        



if __name__ == "__main__":
    # test for edit_personal_profile and availability
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    vol1 = volunteer(connection, cursor)
    # vol1.create_personal_profile("plan1", "camp1", "bill", "liu", "1234567", "Monday,1-12", "vol111", "111", "TRUE", "FALSE")
    # vol1.vols_send_message('vol1', "i love you too", True)
    vol1.vols_send_message('vol9', "Art is a rolling king", plan_name="plan1", camp_name="camp2")
