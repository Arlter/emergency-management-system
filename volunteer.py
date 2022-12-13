import sqlite3
from database_utilities import *
from logging_configure import log_volunteer
import pandas as pd
from color_utilities import  *
from exceptions import *

# functions available: (name - corresponding function)
# 1. create refugee profile - create_refugee_profile
# 2. edit refugee profile - update_refugee_profile
# 3. display all information about certain camp name - list_emergency_profile
# 4. display all information about certain refugee - display_emergency_profile
# 5. edit volunteer's personal profile - edit_personal_profile
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
        self.cursor.execute("PRAGMA foreign_keys = 1")

    def bi_color_text(self, content, font_color='g'):
        return f"{colors.fg.green}✅ {content}{colors.reset}" if font_color == 'g' else f"{colors.fg.red}❌ {content}{colors.reset}"

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
            logger.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        except sqlite3.Error as e:
            logger.error(self.bi_color_text(f"{e}", font_color='r'))
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
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        except absent as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        else:
            return True

    def create_refugee_profile(self, **kwargs):
        """method[27]"""
        try:
            self.cursor.execute(insert_sql_generation("refugee_profile", **kwargs))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        else:
            log_volunteer.info(self.bi_color_text("The creation is successful."))
            return True

    def update_refugee_profile(self, attribute_name, new_val, refugee_ID):
        """method[28]"""
        try:
            self.cursor.execute(update_sql_generation("refugee_profile", attribute_name, new_val, refugee_ID))
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        else:
            log_volunteer.info(self.bi_color_text("The update is successful."))
            return True

    def list_emergency_profile(self, camp_name):
        """method[29]"""
        try:
            sql_cmd = select_sql_generation('refugee_profile', '*', camp_name = camp_name)
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res) != 0:
                for i in range(len(res)):
                    res[i] = list(res[i])
                    t = res[i][0]
                    res[i] = tuple([t] + res[i][2:])
                df = pd.DataFrame(res, columns = ['ID', 'Camp name', 'F. name', 'L. name', 'No. of family', 'Medical condition(s)', 'archived'])
                df.index = ['']*len(df)
                log_volunteer.info(self.bi_color_text("The operation is successful and here are the results: "))
                log_volunteer.info(f"\n{df}\n")
                return True
            else:
                log_volunteer.info(f'No refugee profiles found in the current camp {camp_name}.')
                return True
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False


    # def display_emergency_profile(self, camp_name, first_name ='*', last_name ='*', family_num = '*', medical_condition= '*'):
    #     """method[30]"""
    #     try:
    #         sql_cmd = select_sql_generation('refugee_profile', '*', camp_name = camp_name, first_name = first_name, last_name = last_name, family_num = family_num, medical_condition = medical_condition)
    #         res = self.cursor.execute(sql_cmd).fetchall()
    #         if len(res) != 0:
    #             for i in range(len(res)):
    #                 res[i] = list(res[i])
    #                 res[i] = tuple(res[i][2:])
    #             df = pd.DataFrame(res, columns = ['Camp name', 'First name', 'Last name', 'Number of family members', 'Medical condition(s)', 'archived'])
    #             df.index = ['']*len(df)
    #             log_volunteer.info(f'\n{df}\n')
    #         else:
    #             log_volunteer.info(f'No profiles found.')
    #     except sqlite3.Error as e:
    #             log_volunteer.error(e)
    #     else:
    #         return True

    def display_personal_profile(self, username_: str, logger=log_volunteer, no_extra=False,prompt = True) -> bool:
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
            if prompt:
                logger.info(self.bi_color_text("The operation is successful and here are the results: "))
            logger.info(f'\n{df}\n')
            return True
        except sqlite3.Error as e:
            logger.error(self.bi_color_text(f"{e}", font_color='r'))
            return False


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
            elif 'availability' in kwargs.keys():
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
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        else:
            logger.info(self.bi_color_text("The edit is successful."))
            return True

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
        if ('plan_name' in kwargs.keys()) and ('camp_name' in kwargs.keys()): # camp announcements, from both admin and volunteer
            sql = select_sql_generation("message", "message_id", "time", "username", "content", admin_exclusive="FALSE", **kwargs)
        elif admin_anno and ('plan_name' not in kwargs.keys()) and ('camp_name' not in kwargs.keys()): # admin public announcements
            sql = f"SELECT message_id,time,username,content FROM message WHERE admin_announced='TRUE' and admin_exclusive='FALSE' and plan_name IS NULL and camp_name IS NULL"
        elif admin_anno and ('plan_name' in kwargs.keys()) and ('camp_name' not in kwargs.keys()): # admin plan announcements
            sql = f"SELECT message_id,time,username,content FROM message WHERE admin_announced='TRUE' and admin_exclusive='FALSE' and plan_name='{kwargs['plan_name']}' and camp_name IS NULL"
            # print(sql
        #else:
            # print(1)
            #sql = select_sql_generation("message", "message_id", "time", "username", "content", admin_announced="TRUE", admin_exclusive="FALSE", **kwargs)
        try:
            # print(sql)
            result = self.cursor.execute(sql).fetchall()
            self.connection.commit()
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        if len(result) != 0:
            df = pd.DataFrame(result,columns=['    Message ID','       Time','    username','    Message Content'])
            df.index = [''] * len(df)
            log_volunteer.info(self.bi_color_text("The operation is successful and here are the results: "))
            log_volunteer.info(f"\n{df}\n")
            return True
        else:
            log_volunteer.info("No messages are found given specified information.")
            return True  #?
    
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
            sql = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES('{kwargs['plan_name']}', '{kwargs['camp_name']}','{vol_usrname}','FALSE', 'FALSE','{content}')"   
        elif admin_excl and len(kwargs) == 0:
            sql = f"INSERT INTO message(username,admin_announced,admin_exclusive,content) VALUES('{vol_usrname}', 'FALSE', 'TRUE', '{content}')"
        elif admin_excl and len(kwargs) != 0:
            log_volunteer.error(self.bi_color_text("Please do not specify the camp_name (or plan_name) and the admin_excl at the same time.", font_color='r'))
            return False
        # print(sql)
        try:
            result = self.cursor.execute(sql).fetchall()
            self.connection.commit()
            log_volunteer.info(self.bi_color_text("Message sent successfully."))
            return True
        except sqlite3.Error as e:
            log_volunteer.error(self.bi_color_text(f"{e}", font_color='r'))
            return False
        

if __name__ == "__main__":
    # test for edit_personal_profile and availability
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    vol1 = volunteer()
    # vol1.edit_personal_profile('vol8', first_name="123")
    # vol1.list_emergency_profile("camp1")
    # vol1.vols_send_message("vol8", "plan1", "hello", plan_name='plan2', camp_name='camp1')
    vol1.vols_display_message(True, plan_name='plan1')
    # vol1.availability_(1)
    # vol1.create_refugee_profile(plan_name="plan1", camp_name="camp2", first_name="art", last_name="wang", family_num="999", medical_condition="cold", archived="TRUE")
    # vol1.vols_send_message('vol1', "i love you too", True)
    # vol1.vols_send_message('vol9', "Art is a rolling king", plan_name="plan1", camp_name="camp2")
    # vol1.display_personal_profile("vol1")
