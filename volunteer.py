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

    def __init__(self):
        """
        initialize
        """
        self.connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cursor = self.connection.cursor()

    def raise_error_for_existence(self, table_name,logger = log_volunteer, **kwargs) -> bool:
        """
        method [25]
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

    def raise_error_for_inexistence(self, table_name: str, edit_check=False, **kwargs) -> bool:
        """
        method[26]
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
            if edit_check and table_name == "emergency_plan" and "plan_name" in kwargs.keys() and self.cursor.execute(f"SELECT COUNT(*) FROM emergency_plan WHERE close_date <> '{'null'}' and plan_name = '{kwargs['plan_name']}'").fetchall()[0][0] > 0 :
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

    def create_refugee_profile(self, **kwargs):
        """method[27]"""
        try:
            self.cursor.execute(insert_sql_generation("refugee_profile", **kwargs))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        else:
            return True

    def update_refugee_profile(self, attribute_name, new_val, refugee_ID):
        """method[28]"""
        try:
            self.cursor.execute(update_sql_generation("refugee_profile", attribute_name, new_val, refugee_ID))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        else:
            return True

    def list_emergency_profile(self, camp_name):
        """method[29]"""
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
        """method[30]"""
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
        method[31]
        Create a new personal profile
        :param *attr: the new volunteer information, with the order as: 
                    $plan_name, $camp_name, $first_name, $last_name, $phone_num, $availability, $username, $password, $activated, $reassignable
        NOTE: if you would like to specify availability, make sure that the string
              is formatted as "1,2,3", which is translated to "Monday, Tuesday, Wednesday"
              in database. Split the string with comma and no space!
        """
        try:
            if not self.raise_error_for_existence("volunteer", username=attr[6]):
                return False
            attr_list = list(attr)
            t = attr[5].split(',')
            res = ''
            matched = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for ch in t:
                res += matched[int(ch) - 1] + ','
            attr_list[5] = res[0:-1]
            attr = tuple(attr_list)
            # print(attr)
            sql = insert_sql_generation("volunteer", *attr)
            res = self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
            return False
        else:
            return True

    def display_personal_profile(self, username_: str, logger=log_volunteer, no_extra=False) -> bool:
        """method[32]"""
        if not self.raise_error_for_inexistence("volunteer", username=username_):
            return False
        if no_extra:
            sql = select_sql_generation("volunteer", "*", username=username_)
        else:
            sql = select_sql_generation("volunteer", "plan_name", "camp_name", "first_name", "last_name", "phone_num", "availability", "username", "password", username=username_)
        try:
            res = self.cursor.execute(sql).fetchall()
            self.connection.commit()
            if no_extra:
                df = pd.DataFrame(res, columns = ['Plan name', 'Camp name', 'First name', 'Last name', 'Phone number', 'availability', 'username', 'password', 'activated', 'reassignable'])
            else:
                df = pd.DataFrame(res, columns = ['Plan name', 'Camp name', 'First name', 'Last name', 'Phone number', 'availability', 'username', 'password'])
            df.index = ['']*len(df)
            logger.info(f'\n{df}\n')
            # print(result)
        except sqlite3.Error as e:
            logger.error(e)
            return False
        else:
            return True


    def edit_personal_profile(self, username: str, logger= log_volunteer, **kwargs) -> bool:
        """
        method[33]
        Collect the info and update the volunteer table
        example: edit_personal_profile("vol4", plan_name="plan1", camp_name="camp2")
                 update plan name and camp name to be 'plan1' and 'camp2' respectively
                 to volunteer 'vol4'
        :param username: the volunteer's username who would like to make the update
        :param **kwargs: attribute = value bindings you would like to update
        NOTE: if you would like to update availability, make sure that the string
              is formatted as "1,2,3", which is translated to "Monday, Tuesday, Wednesday"
              database. Split the string with comma and space!
        """
        args = []
        for key, value in kwargs.items():
            if key != 'availability':
                args.append(key)
                args.append(value)
        # print(args)
        t = kwargs['availability'].split(',')
        res = ''
        matched = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for ch in t:
            res += matched[int(ch) - 1] + ','
        args.append("availability")
        args.append(res[0:-1])
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

    def availability_(self, time: int, plan_name=None, camp_name=None, logger=log_volunteer) -> list:
        """
        method[34]
        the function searches for volunteers fully available in certain day
        :param time: an integer that should be in range 1 - 7, for example, '1' for Monday, '2' for Tuesday
        :param plan_name: a string which specify the plan name, default none
        :param plan_name: a string which specify the camp name, default none
        :return: a list containing available volunteer usernames in given weekday
                 if there is error return false
        """
        res = []
        if time < 1 or time > 7:
            logger.error("Invalid time input, make sure it is in 1 - 7")
            return False
        matched = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_str = matched[time - 1]
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
            day = tuples[1].split(',')
            # print(day)
            if day_str in day:
                res.append(vol)
        if len(res) == 0:
            logger.info("There is no satisfied volunteer in that period.")
            return res
        else:
            logger.info(f"In that period, The satisfied volunteers are {res}.")
            return res

    def vols_display_message(self, admin_anno = False, **kwargs) -> bool:
        """
        method[35]
        :param **kwargs: bindings that specify message from which channel.
        :param admin_anno: default false, if want to display announcements from admin, set it to true
        example: vols_display_message(plan_name = 'plan1', camp_name = 'camp1')
        displays message from camp1 and plan1
        example2: vols_display_message(admin_anno = True)
        displays message from admin
        NOTE: please do not set true to admin_anno and specify **kwargs at the same time
        """
        # print(not admin_anno)
        if not admin_anno:
            sql = select_sql_generation("message", "message_id", "time", "username", "content", **kwargs)
        elif admin_anno and len(kwargs) == 0:
            sql = select_sql_generation("message", "message_id", "time", "username", "content", admin_announced="TRUE", admin_exclusive="FALSE")
        elif admin_anno and len(kwargs) != 0:
            log_volunteer.error("Please do not specify the camp_name (or plan_name) and the admin_anno at the same time!")
            return False
        try:
            result = self.cursor.execute(sql).fetchall()
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(e)
        if len(result) != 0:
            df = pd.DataFrame(result,columns=['    Message ID','       Time','    username','    Message Content'])
            df.index = [''] * len(df)
            log_volunteer.info(f"\n{df}\n")
            return True
        else:
            log_volunteer.info("* No messages are found given specified information.")
            return False
    
    def vols_send_message(self, vol_usrname: str, planname, content: str, admin_excl=False, **kwargs) -> bool:
        """
        method[36]
        :param vol_usrname: the volunteer who would like to send message
        :param content: the content you would like to send
        :param admin_excl: default false, if want to send message to admin, set it to true
        :param **kwargs: bindings that specify message from which channel. (plan_name and camp_name)
        example: vols_send_message("vol1", "I love u art", plan_name="plan1", camp_name="camp1")
        sends message to camp1 and plan1 from vol1
        example2: vols_send_message(admin_excl = True)
        sends message to admin
        NOTE: please do not set true to admin_anno and specify **kwargs at the same time
        """
        if not self.raise_error_for_inexistence("volunteer", edit_check=True, username=vol_usrname):
            return False
        if not admin_excl and not self.raise_error_for_inexistence("emergency_plan", edit_check=True, plan_name=planname):
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
    vol1 = volunteer()
    vol1.create_personal_profile('plan1', 'camp1', 'bill', 'liu', '123', '1,2,3', 'vol8', '111', 'TRUE', "FALSE")
    vol1.edit_personal_profile('vol8', availability="1,2,5")
    vol1.availability_(1)
    # vol1.create_refugee_profile(plan_name="plan1", camp_name="camp2", first_name="art", last_name="wang", family_num="999", medical_condition="cold", archived="TRUE")
    # vol1.create_personal_profile("plan1", "camp1", "bill", "liu", "1234567", "Monday,1-12", "vol111", "111", "TRUE", "FALSE")
    # vol1.vols_send_message('vol1', "i love you too", True)
    # vol1.vols_send_message('vol9', "Art is a rolling king", plan_name="plan1", camp_name="camp2")
    # vol1.display_personal_profile("vol1")
