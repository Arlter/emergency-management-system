import sqlite3
from datetime import datetime
from database_utilities import *
from logging_configure import log_admin
import pandas as pd
from exceptions import *
from terminal.color_utilities import  *
from volunteer import volunteer
class admin(volunteer):

#################################The following two methods for general single-value check ##############################
    def raise_error_for_existence(self,table_name,**kwargs) -> bool:
        """
        Method[1] Overwrite the volunteer method
        :param table_name: table name
        :param kwargs:  pass in the form of attr_name = attr_value
        :return:true if the value does not exist, false otherwise.
        """
        return super(admin,self).raise_error_for_existence(table_name,logger = log_admin, **kwargs)

    def raise_error_for_inexistence(self, table_name:str, edit_check = False, **kwargs) -> bool:
        """
        Method[2] This method is called when you want to verify existence of a tuple. It will raise an error if
        the tuple has not existed and return False.This method also adds a prohibitor(edit_check)to prevent attempts on editting
        a closed emergency plan.
        :param table_name: table name
        :param kwargs:  pass in the form of attr_name = attr_value
        :return:true if the value does not exist, false otherwise.
        """
        try:
            if edit_check and table_name == "emergency_plan" and "plan_name" in kwargs.keys() and self.cursor.execute(f"SELECT COUNT(*) FROM emergency_plan WHERE close_date <> '{'null'}' and plan_name = '{kwargs['plan_name']}'").fetchall()[0][0] > 0 :
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

####################################The following for account management system #######################################
    # Method to be implemented,  change passwords of the account  either with accountId, or username
    def password_change(self, username: str, password: str) -> bool:
        """
        Method [3]
        Change volunteer's password
        :param username: volunteer's username
        :param password: new password 
        """
        try:
            sql = self.cursor.execute(update_sql_generation("volunteer", "password", password, username = username))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* Password successfully changed ")
            return True

#################################The following Methods are for plan & camp management system############################

    # A method for plan management system
    def add_emergency_plan(self, plan_name:str,type:str,description:str,geo_affected_area:str) -> bool:
        """
        Method[4] used to add emergency_plan. The last parameter from the table "close_date" is set to "NULL" by default.
        :param plan_name: plan name
        :param type: emergency type
        :param description: description
        :param geo_affected_area: location
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
    def list_existing_plans(self) -> bool:
        """
        Method[5] list all the plans including archived ones
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

    # A method for plan management system
    def display_plan_summary(self,pl_name:str) -> bool:
        """
        Method[6] used to display the details of a specific plan by entering its name
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

    # Method to be implemented, Edit a plan's information. For example, name, description etc.
    def edit_plan(self, pl_name: str, logger=log_admin, **kwargs,)-> bool:
        """
        Method[7]: This method is used to edit unclosed plans with verified infomation
        Collect the info and update the camp table
            example: edit_plan(pl_name: "plan1", plan_name= "plan2", plan_type="earthquake", plan_description="new description", geo_area = "japan")
            edit "plan1" to be named "plan2", change type to "earthquake", description to "new description" and geo_affected to "japan"
        :param pl_name: plan name to be edited
        :param **kwargs: attribute = values to be updated 
        :param return: true edit successful, false otherwise
        """
        if not super(admin,self).raise_error_for_existence("camp", archived=True, plan_name=pl_name):
            return False
        args = []
        for key, value in kwargs.items():
            args.append(key)
            args.append(value)
        sql = update_sql_generation("emergency_plan", *args, plan_name=pl_name)
        
        try:
            self.cursor.execute(sql).fetchall()
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(e)
            return False
        else:
            return True

    # A method for plan management system
    def close_emergency_plan(self,pl_name:str)-> bool:
        """
        Method[8]: used to close an emergency plan by specifying its close date. You do not have to enter a date mannually.
        The time when calling this function will become the end_date automatically.
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


    # A method for camp management system
    def add_camp(self,plan_name:str ,*camp_names) -> bool:
        """
        Method[9] used to add camp(s) to a plan.
        :param plan_name: plan name
        :param camp_names: all camp names to be added
        :return: true if the operation is successful false otherwise
        Example for camp_names: you can save names in a list/tuple like l = ['name1','name2'].
        And call the method this way: add_camp(*l)
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

    # A method for camp management system
    def edit_camp_name(self, pl_name:str, camp_name:str, new_camp_name: str)-> bool:
        """
        Method[10]: This method is used to change the name of a camp under a plan.
        :param pl_name: Plan name 
        :param camp_name: Camp name to be changed
        :param new_camp_name: New camp name 
        """
        try:
            sql = self.cursor.execute(update_sql_generation("camp", "camp_name", new_camp_name, plan_name = pl_name, camp_name = camp_name))
            self.connection.commit()
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* Camp name successfully changed ")
            return True

##########################The following Methods are for volunteer management system####################################
    def availability(self, time: int, plan_name=None, camp_name=None, logger=log_admin) -> list:
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
            day = tuples[1]
            # print(day)
            if day_str in day:
                res.append(vol)
        if len(res) == 0:
            logger.info("There is no satisfied volunteer in that period.")
            return res
        else:
            logger.info(f"In that period, The satisfied volunteers are {res}.")
            return res

    # A method to be implemented
    def create_volunteer(self, *attr)-> bool:
        """
        method[11]
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
            log_admin.error(e)
            return False
        else:
            return True

    # A method to be implemented
    def view_volunteer_details(self, username: str)-> bool:
        """
        Method[12]: with all infor collected, view a volunteer's details. Consider the usage of pandas
        :return:
        """
        return super(admin,self).display_personal_profile(username,logger = log_admin)

    def list_all_volunteers(self) -> bool:
        """
        Method[x]: list all volunteers including accounts which have been deactivated.
        """
        try:
            sql = select_sql_generation("volunteer", "*")
            res = self.cursor.execute(sql).fetchall()
            if len(res) != 0:
                df = pd.DataFrame(res,columns = ['Plan name','Camp name','First name','Last name','Phone number','availability', 'username', 'password','activated','reassignable'])
                df.index = ['']*len(df)
                log_admin.info(f'\n{df}\n')
            else:
                log_admin.info(f'* No volunteers found.')
            # print(result)
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True
        
        

    # A method to edit volunteer details
    def edit_volunteer_details(self, username: str, **kwargs) -> bool:
        """
        Method[13]: used to edit volunteers' detail
        :param username:  refer to edit_personal_profile in volunteer
        :param kwargs: refer to edit_personal_profile in volunteer
        :return: True edit successful, false otherwise
        """
        try:
            super(admin, self).edit_personal_profile(username,logger=log_admin, **kwargs)
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            log_admin.info(f"* The edition is successful ")
            return True


    # A method for volunteer management system
    def deactivate_volunteer(self, vol_usrname):
        """
        Method[14]: deactivate the account of the volunteer
        :param vol_usrname: the usrname of the volunteer
        :return:true if the operation is successful false otherwise
        """
        try:
            self.cursor.execute(update_sql_generation("volunteer","activated","FALSE",username = vol_usrname))
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
        Method[15]: activate the account of the volunteer
        :param vol_usrname: the username of the volunteer account
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            self.cursor.execute(update_sql_generation("volunteer","activated","TRUE",username = vol_usrname))
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
        Method[16]: delete the account of the volunteer
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
    def create_admin_announcement(self, announcement:str, **kwargs):
        """
        Method[17]: used to create an admin announcement by an admin. This annoucement could be only visible by all vols, or vols from a plan,  or a camp
        :param announcement: string of the announcement
        :param kwargs: In case admin wants to publish message to specific channel/camp
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            if not kwargs:
                sql_cmd = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES(null, null,'admin','TRUE','FALSE','{announcement}')"
            elif 'plan_name' in kwargs and 'camp_name' in kwargs:
                sql_cmd = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES('{kwargs['plan_name']}', '{kwargs['camp_name']}','admin','TRUE','FALSE','{announcement}')"
            elif 'plan_name' in kwargs:
                sql_cmd = f"INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES('{kwargs['plan_name']}', null,'admin','TRUE','FALSE','{announcement}')"
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
        Method[18]: used to display messages from the same emergency plan
        :param plan_name: plan name
        :return:True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"{select_sql_generation('message', 'time','username','plan_name','content', plan_name = plan_name,admin_exclusive='FALSE')} ORDER BY message_id ASC"
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
        Method[19]: used to display all the messages coming from the same camp
        :param plan_name: plan name
        :param camp_name: camp name
        :return: True if the operation encounters no exceptions, false otherwise.
        """
        try:
            sql_cmd = f"{select_sql_generation('message', 'time','username','plan_name','camp_name','content', plan_name = plan_name, camp_name=camp_name,admin_exclusive='FALSE')} ORDER BY message_id ASC"
            # print(sql_cmd)
            res = self.cursor.execute(sql_cmd).fetchall()
            if len(res)!=0:
                df = pd.DataFrame(res,
                                  columns=['    Post Time','    Account','      Plan Name','  Camp Name', '            Message Content'])
                df.index = [''] * len(df)
                log_admin.info(f"\n{df}\n")
            else:
                log_admin.info(f"{colors.bg.green}* No messages are found given the plan name and camp name {colors.reset}")
        except sqlite3.Error as e:
            log_admin.error(e)
            return False
        else:
            return True

    # A method for message management system:
    def display_admin_exclusive_messages(self):
        """
        Method[20]: used to display all the messages exclusive to admin
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
    def delete_admin_exclusive_messages(self):
        """
        Method[21]:used to delete all the admin_exclusive messages if they exist
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



#######################################The following Methods are for logging management system#######################
    # A method for logging system
    def display_logs(self)-> bool:
        """
        Method[22] display the running logs from this time.
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

    # A method for logging system to be implemented
    def reset_logs(self)-> bool:
        #Method[23]  basically just remove all the content in the file logging.log
        with open('logging.log', 'w'):
            pass

if __name__ == "__main__":
    ad = admin()
    ad.display_messages_from_a_camp('plan1', 'camp2')
    ad.create_volunteer('plan1', 'camp1', 'bill', 'liu', '123', '1,2,3', 'vol9', '111', 'TRUE', "FALSE")
    ad.availability(1)
