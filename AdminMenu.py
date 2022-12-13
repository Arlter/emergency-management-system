from color_utilities import *
from admin import *
from exceptions import *
from logging_configure import *
from title import *

class AdminMenu:
    def __init__(self):
        self.Ifback = False
        self.queue = []


        self.Admin = admin()

        self.admin_menu_dict = {
            "1": "self.account_management()",
            "2": "self.manage_emergency_plan_system()",
            "3": "self.manage_volunteer_system()",
            "4": "self.manage_messaging_system()",
            "5": "self.display_log()",
            "b": "logout",
            "q": "self.quit()"
        }


        self.account_management_dict = {
            "1": "self.change_password()",
            "b": "self.admin_menu()",
            "q": "self.quit()"
        }


        self.manage_emergency_system_dict = {
            "1": "self.create_a_plan()",
            "2": "self.list_existing_plans()",
            "3": "self.view_a_plan()",
            "4": "self.edit_a_plan()",
            "5": "self.close_a_plan()",
            "6": "self.manage_camps()",
            "b": "self.admin_menu()",
            "q": "self.quit()"
        }
        self.manage_camps_dict = {
            "1": "self.add_camps()",
            "2": "self.change_camp_names()",
            "b": "self.manage_emergency_plan_system()",
            "q": "self.quit()"
        }



        self.manage_volunteer_system_dict = {
            "1": "self.create_a_volunteer()",
            "2": "self.list_existing_volunteers()",
            "3": "self.view_a_volunteer()",
            "4": "self.edit_a_volunteer()",
            "5": "self.deactivate_a_volunteer_account()",
            "6": "self.activate_a_volunteer_account()",
            "7": "self.delete_a_volunteer()",
            "8": "self.check_availability()",
            "b": "self.admin_menu()",
            "q": "self.quit()"
        }

        self.manage_messaging_system_dict = {
            "1": "self.create_public_announcements()",
            "2": "self.create_regional_announcements()",
            "3": "self.display_plan_messages()",
            "4": "self.display_camp_messages()",
            "5": "self.display_admin_exclusive_messages()",
            "6": "self.delete_admin_exclusive_messages()",
            "b": "self.admin_menu()",
            "q": "self.quit()"
        }


        self.queue.append('self.admin_menu()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]



    def quit(self):
        self.Admin.connection.close()

    def back(self,arg:str,next:str):
        if arg == 'b':
            self.queue.append(next)
            return True
        else:
            return False

###################################################### admin menu ######################################################
    def admin_menu(self):
        user_input = input("========================================\n"
                           "               Admin Menu\n"
                           "\n"
              "(1) Account management\n"
              "(2) Manage emergency plan system\n"
              "(3) Manage volunteer system\n"
              "(4) Manage messaging system\n"            
              "(5) Display the log\n"
              "(b) Log out\n"
              "(q) Quit\n"
              "\n---➤ "
        )

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.admin_menu_dict[user_input])
                # always pass
            elif user_input == 'b':
                self.Ifback = True

            elif user_input in list(self.admin_menu_dict.keys()):
                self.queue.append(self.admin_menu_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.admin_menu()')


################################################## account management ##################################################
    def account_management(self):
        user_input = input("________________________________________\n"
                           "         Account Management\n"
                           "\n"
              "(1) Change the password\n"
              "(b) Back to Admin Menu\n"
              "(q) Quit\n"
              "\n---➤ "
        )

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.account_management_dict[user_input])
                # always pass
            elif user_input in list(self.account_management_dict.keys()):
                self.queue.append(self.account_management_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.account_management()')

### change password ###
    def change_password(self):
        print('\n')
        self.Admin.list_all_volunteers(prompt=False)
        user_input1 = input("Please complete the following information or Input b to back\n"
            "Input the username: ")
        if self.back(user_input1,'self.account_management()'):
            return

        elif self.Admin.raise_error_for_inexistence("volunteer",edit_check=False,username = user_input1):
            new_password = input("Please enter the new password: ")
            if new_password != "b":
                self.Admin.password_change(user_input1,new_password)
                self.queue.append('self.account_management()')
            else:
                self.queue.append('self.account_management()')
        else:
            self.queue.append('self.change_password()')


############################################# manage emergency plan system #############################################
    def manage_emergency_plan_system(self):
        user_input = input("________________________________________\n"
                           "      Manage emergency plan system\n"
                           "\n"
              "(1) Create a plan\n"
              "(2) List existing plans\n"
              "(3) View a plan\n"
              "(4) Edit a plan\n"
              "(5) Close a plan\n"
              "(6) Manage camps\n"
              "(b) Back to Admin Menu\n"
              "(q) Quit\n"
              "\n---➤ "
        )

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.manage_emergency_system_dict[user_input])
                # always pass
            elif user_input in list(self.manage_emergency_system_dict.keys()):
                self.queue.append(self.manage_emergency_system_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.manage_emergency_plan_system()')

### create a plan ###
    def create_a_plan(self):
        print('\n')
        self.Admin.list_existing_plans(prompt=False)
        new_plan_name = input("Please complete the following information or Input b to back\n"
                                     "Plan name: ")
        '''check existence of new plan'''
        if self.back(new_plan_name,'self.manage_emergency_plan_system()'):
            return

        elif self.Admin.raise_error_for_existence("emergency_plan", plan_name=new_plan_name):
            new_plan_type = input("Type: ")
            if self.back(new_plan_type, 'self.manage_emergency_plan_system()'):
                return

            new_plan_description = input("Description: ")
            if self.back(new_plan_description, 'self.manage_emergency_plan_system()'):
                return

            new_plan_geo_affected_area = input("Affected area: ")
            if self.back(new_plan_geo_affected_area, 'self.manage_emergency_plan_system()'):
                return


            self.Admin.add_emergency_plan(new_plan_name,new_plan_type,new_plan_description,new_plan_geo_affected_area)
            self.queue.append('self.manage_emergency_plan_system()')

        else:
            self.queue.append('self.create_a_plan()')

### List existing plans ###
    def list_existing_plans(self):
        print('\n')
        self.Admin.list_existing_plans()
        self.queue.append('self.manage_emergency_plan_system()')

### View a plan ###
    def view_a_plan(self):
        print("\n")
        self.Admin.list_existing_plans(prompt=False)
        plan_viewed = input(
                            "Please complete the following information or Input b to back\n"
                           "Please enter the plan name to be viewed: " )

        if self.back(plan_viewed,'self.manage_emergency_plan_system()'):
            return
        elif self.Admin.raise_error_for_inexistence("emergency_plan",edit_check=False,plan_name=plan_viewed):

            self.Admin.display_plan_summary(plan_viewed)

            self.queue.append('self.manage_emergency_plan_system()')
        else:
            self.queue.append('self.view_a_plan()')

### Edit a plan ###
    def edit_a_plan(self):
        print("\n")
        self.Admin.list_existing_plans(prompt=False)

        plan_edited = input("Please complete the following information or Input b to back\n"
                           "Please select a plan: ")
        if self.back(plan_edited,'self.manage_emergency_plan_system()'):
            return
        elif self.Admin.raise_error_for_inexistence("emergency_plan",edit_check=True,plan_name=plan_edited):
            self.Admin.display_plan_summary(plan_edited,prompt=False)

            plan_dict = {
                '1': "plan_name",
                '2': "plan_type",
                '3': "plan_description",
                '4': "geo_area",
                '5': "display the plan summary again"
            }

            selection_loop = True
            while selection_loop:
                for i in range(len(plan_dict)):
                    print(list(plan_dict.keys())[i], ": ", list(plan_dict.values())[i].replace("_", ' '))
                index_selected = input("\n"
                                       "Select from the above options: ")

                try:
                    if self.back(index_selected, 'self.manage_emergency_plan_system()'):
                        return
                    elif index_selected in plan_dict.keys():

                        #plan type, plan description, geo area
                        if index_selected in ['2','3','4']:
                            updated_inf = input(
                                "Input the new " + plan_dict[index_selected].replace("_", ' ') + ": ")
                            if self.back(updated_inf, 'self.manage_emergency_plan_system()'):
                                return
                            eval('self.Admin.edit_plan(plan_edited,'+plan_dict[index_selected]+'=updated_inf)')
                        #plan name
                        elif index_selected == '1':
                            updated_inf = input(
                                "Input the new " + plan_dict[index_selected].replace("_", ' ') + ": ")
                            if self.back(updated_inf, 'self.manage_emergency_plan_system()'):
                                return
                            elif self.Admin.raise_error_for_existence('emergency_plan',plan_name=updated_inf):
                                self.Admin.edit_plan(plan_edited,plan_name=updated_inf)
                            else:
                                continue

                        elif index_selected == '5':
                            self.Admin.display_plan_summary(plan_edited)
                            continue

                        selection_loop = False

                    else:
                        raise option_not_existed

                except option_not_existed as e:
                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            self.queue.append('self.manage_emergency_plan_system()')
        else:
            self.queue.append('self.edit_a_plan()')

### close a plan ###
    def close_a_plan(self):
        print("\n")
        self.Admin.list_existing_plans(prompt=False)
        plan_closed = input("Please select a plan or Input b to back:  ")

        if self.back(plan_closed,'self.manage_emergency_plan_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check= True,plan_name=plan_closed):
            self.Admin.close_emergency_plan(plan_closed)
            self.queue.append('self.manage_emergency_plan_system()')
        else:
            self.queue.append('self.close_a_plan()')
### Manage camps ###
    def manage_camps(self):
        user_input = input("________________________________________\n"
                           "             Manage camps\n"
                           "\n"
                           "(1) Add camps\n"
                           "(2) Change camp names\n"
                           "(b) back to last menu\n"
                           "(q) quit\n"
                           "\n---➤ ")

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.manage_camps_dict[user_input])
                # always pass
            elif user_input in list(self.manage_camps_dict.keys()):
                self.queue.append(self.manage_camps_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.manage_camps()')

    ### add camps ###
    def add_camps(self):
        print('\n')
        self.Admin.list_existing_plans(prompt=False)
        plan_selected = input("Please complete the following information or Input b to back\n"
                                     "Plan name: ")
        if self.back(plan_selected,'self.manage_camps()'):
            return
        elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check= True,plan_name=plan_selected):
            self.Admin.display_plan_summary(plan_selected,prompt=False)

            newcamp_inputloop = True
            while newcamp_inputloop:
                new_camp = input("Please input the new camp names splitted by comma\n"
                    "New camp name: ").split(',')

                if self.back(new_camp[0],'self.manage_camps()'):
                    return

                '''DoubleCheck the new_camp input'''
                print("Is this the camp name you would like to add?")
                for i in range(len(new_camp)):
                    print('[',i+1,'] ',new_camp[i])

                doublecheckloop = True
                while doublecheckloop:
                    doublecheck = input("Please input y for Yes or n for No: ")
                    try:
                        if self.back(doublecheck, 'self.manage_camps()'):
                            return
                        elif doublecheck == 'y':
                            newcamp_inputloop = False
                            doublecheckloop = False
                        elif doublecheck == 'n':
                            newcamp_inputloop = True
                            doublecheckloop = False
                        else:
                            raise option_not_existed
                    except option_not_existed as e:
                        log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            for j in new_camp:
                if self.Admin.add_camp(plan_selected,j):
                    pass
                else:
                    self.queue.append('self.add_camps()')
                    return

            self.queue.append('self.manage_camps()')
        else:
            self.queue.append('self.add_camps()')

    ### change camp names ###
    def change_camp_names(self):
        print('\n')
        self.Admin.list_existing_plans(prompt=False)
        plan_selected = input("Please complete the following information or Input b to back\n"
                              "Plan name: ")

        if self.back(plan_selected,'self.manage_camps()'):
            return
        elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check= True,plan_name=plan_selected):
            self.Admin.display_plan_summary(plan_selected,prompt=False)


            campselect_loop = True
            while campselect_loop:
                camp_selected = input("Please select a camp to change the name: ")
                if self.back(camp_selected, 'self.manage_camps()'):
                    return
                elif self.Admin.raise_error_for_inexistence('camp',edit_check= False,camp_name=camp_selected,plan_name=plan_selected):

                    newname_loop = True
                    while newname_loop:
                        new_camp = input("Please input a new camp name: ")
                        if self.back(new_camp, 'self.manage_camps()'):
                            return
                        elif self.Admin.edit_camp_name(plan_selected,camp_selected,new_camp):
                            newname_loop = False
                        else:
                            newname_loop = True
                    campselect_loop = False
                else:
                    campselect_loop = True

            self.queue.append('self.manage_camps()')
        else:
            self.queue.append('self.change_camp_names()')


############################################### manage volunteer system ################################################
    def manage_volunteer_system(self):
        user_input = input("__________________________________________\n"
                           "          Manage volunteer system\n"
                           "\n"
              "(1) Create a volunteer\n"
              "(2) List existing volunteers\n"
              "(3) view a volunteer\n"
              "(4) Edit a volunteer\n"
              "(5) Deactivate a volunteer account\n"
              "(6) Activate a volunteer account\n"
              "(7) Delete a volunteer\n"
              "(8) Check availability of volunteers\n"
              "(b) Back to Admin Menu\n"
              "(q) Quit\n"
              "\n---➤ "
        )

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.manage_volunteer_system_dict[user_input])
                # always pass
            elif user_input in list(self.manage_volunteer_system_dict.keys()):
                self.queue.append(self.manage_volunteer_system_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.manage_volunteer_system()')

### create a volunteer ###
    ''' $plan_name, $camp_name, $first_name, $last_name, $phone_num, $availability, $username, $password, $activated, $reassignable'''
    def create_a_volunteer(self):
        new_volun_profile_dict = {
            "[1]": "Plan name: ",
            "[2]": "Camp name: ",
            "[3]": "First name: ",
            "[4]": "Last name: ",
            "[5]": "Phone number: ",
            "[6]": "Availability: ",
            "[7]": "Username: ",
            "[8]": "Password: ",
            "[9]": "Activated: ",
            "[10]": "Reassignable: "
        }
        day_dict = {
            '1': "Monday",
            '2': "Tuesday",
            '3': "Wednesday",
            '4': "Thursday",
            '5': "Friday",
            '6': "Saturday",
            '7': "Sunday",
        }
        print("\n"
              "Please complete the following information or Input b to back")
        self.Admin.list_existing_plans(prompt=False)
        plan_selected = input(new_volun_profile_dict['[1]'])
        if self.back(plan_selected, 'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check= True,plan_name=plan_selected):
            self.Admin.display_plan_summary(plan_selected,prompt=False)

            pd.options.display.max_columns = None
            campselect_loop = True
            while campselect_loop:
                camp_selected = input(new_volun_profile_dict['[2]'])
                if self.back(camp_selected, 'self.manage_volunteer_system()'):
                    return
                elif self.Admin.raise_error_for_inexistence('camp',edit_check= False,camp_name=camp_selected,plan_name=plan_selected):

                    print('\n'
                          "Now complete the profile for new volunteer: ")
                    new_volun_firstname = input("First name: ")
                    if self.back(new_volun_firstname, 'self.manage_volunteer_system()'):
                        return
                    new_volun_lastname = input("Lats name: ")
                    if self.back(new_volun_lastname,'self.manage_volunteer_system()'):
                        return
                    new_volun_phone_num = input("Phone number: ")
                    if self.back(new_volun_phone_num,'self.manage_volunteer_system()'):
                        return

                    '''availability is in particular form'''
                    availability_loop = True
                    while availability_loop:
                        new_volun_availability = input("Availability(Weekday number 1-7 splitted by comma e.g.'1,2' for 'Monday,Tuesday' ): ")
                        if self.back(new_volun_availability,'self.manage_volunteer_system()'):
                            return
                        else:
                            new_volun_availability = new_volun_availability.split(',')
                            try:
                                for i in new_volun_availability:
                                    if i not in day_dict.keys():
                                        raise Invalid_value
                                else:
                                    new_volun_availability = [day_dict[i] for i in new_volun_availability]
                                    new_volun_availability = ','.join(new_volun_availability)
                                    availability_loop = False
                            except Invalid_value as e:
                                log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))


                    '''Check if username existed already'''
                    new_volun_name_inputloop = True
                    while new_volun_name_inputloop:
                        new_volun_username = input("Username: ")
                        if self.back(new_volun_username,'self.manage_volunteer_system()'):
                            return
                        elif self.Admin.raise_error_for_existence('volunteer',username = new_volun_username):
                            new_volun_name_inputloop = False
                        else:
                            pass

                    new_volun_password = input("Password: ")
                    if self.back(new_volun_password,'self.manage_volunteer_system()'):
                        return


                    '''activated is in particular form'''
                    boolean_dict ={
                        '1': "TRUE",
                        '2': "FALSE"
                    }
                    new_volun_activated_inputloop = True
                    while new_volun_activated_inputloop:
                        new_volun_activated_key = input("Activated: \n"
                                                    "[1]TRUE\n"
                                                    "[2]FALSE\n"
                                                    "Select from above: ")
                        try:
                            if self.back(new_volun_activated_key,'self.manage_volunteer_system()'):
                                return
                            elif new_volun_activated_key in boolean_dict.keys():
                                new_volun_activated = boolean_dict[new_volun_activated_key]
                                new_volun_activated_inputloop = False
                            else:
                                raise option_not_existed
                        except option_not_existed as e:
                            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

                    new_volun_profile=[plan_selected,camp_selected,new_volun_firstname,new_volun_lastname,new_volun_phone_num,new_volun_availability,new_volun_username,new_volun_password,new_volun_activated,"FALSE"]

                    '''DoubleCheck the new_camp input'''
                    print('\n'
                        "Is this the volunteer profile you would like to create?")
                    for i in range(len(new_volun_profile)-1):
                        print(new_volun_profile_dict[f'[{i+1}]'], new_volun_profile[i])

                    doublecheckloop = True
                    while doublecheckloop:
                        doublecheck = input("Please input y for Yes or n for No: ")
                        try:
                            if self.back(doublecheck,'self.manage_volunteer_system()'):
                                return
                            elif doublecheck == 'y':
                                campselect_loop = False
                                doublecheckloop = False
                            elif doublecheck == 'n':
                                self.queue.append('self.create_a_volunteer()')
                                return
                            else:
                                raise option_not_existed
                        except option_not_existed as e:
                            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            self.Admin.create_volunteer(*new_volun_profile)
            self.queue.append('self.manage_volunteer_system()')

        else:
            self.queue.append('self.create_a_volunteer()')

### list existing volunteers ###
    def list_existing_volunteers(self):
        print('\n')
        self.Admin.list_all_volunteers()
        self.queue.append('self.manage_volunteer_system()')

### view a volunteer ###
    def view_a_volunteer(self):
        print("\n")
        self.Admin.list_all_volunteers(prompt=False)
        volunteer_selected = input(
                              "Please complete the following information or Input b to back\n"
                              "Volunteer name: ")
        if self.back(volunteer_selected,'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('volunteer', edit_check=False,username=volunteer_selected):
            self.Admin.view_volunteer_details(volunteer_selected)
            self.queue.append('self.manage_volunteer_system()')
        else:
            self.queue.append('self.view_a_volunteer()')

### edit a volunteer ###
    '''editing plan name for a volunteer is only allowed when the plan this volunteer worked in has been closed'''
    '''editing camp name for a volunteer is only allowed when the plan this volunteer is working for is open'''
    '''change of username and reassignable is not allowed'''
    '''change of activated status is not in this section'''
    def edit_a_volunteer(self):
        print("\n")
        self.Admin.list_all_volunteers(prompt=False)
        volunteer_selected = input(
                              "Please complete the following information or Input b to back\n"
                              "Volunteer name: ")
        if self.back(volunteer_selected,'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('volunteer',edit_check=True,username=volunteer_selected):
            self.Admin.view_volunteer_details(volunteer_selected,prompt=False)

            profile_dict = {
                '1': "plan_name",
                '2': "camp_name",
                '3': "first_name",
                '4': "last_name",
                '5': "phone_num",
                '6': "availability",
                '7': "password",
                '8': "display the profile again"
            }


            selection_inputloop = True
            while selection_inputloop:
                for i in range(len(profile_dict)):
                    print(list(profile_dict.keys())[i], ": ", list(profile_dict.values())[i].replace("_", ' '))
                index_selected = input("\n"
                                           "Select from the above options: ")
                try:
                    if self.back(index_selected,'self.manage_volunteer_system()'):
                        return
                    elif index_selected in profile_dict.keys():

                        #firt last name, phone number check
                        if index_selected in ['3','4','5','7']:
                            updated_inf = input(
                                "Input the new " + profile_dict[index_selected].replace("_", ' ') + ": ")
                            if self.back(updated_inf, 'self.manage_volunteer_system()'):
                                return
                            eval('self.Admin.edit_volunteer_details(username=volunteer_selected,'+profile_dict[index_selected]+'=updated_inf)')

                        #plan check
                        elif index_selected == '1':
                            self.Admin.list_existing_plans(prompt=False)
                            updated_inf = input(
                                "Input the new " + profile_dict[index_selected].replace("_", ' ') + ": ")
                            if self.back(updated_inf, 'self.manage_volunteer_system()'):
                                return

                            elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check=True,plan_name=updated_inf):
                                try:
                                    '''to check if volunteer is reassignable'''
                                    if self.Admin.raise_error_for_inexistence('volunteer',edit_check=False,username=volunteer_selected,reassignable="TRUE"):
                                        self.Admin.display_plan_summary(updated_inf,prompt=False)

                                        camp_updated = input("Which camp in "+updated_inf+" you would like to assign this volunteer to: ")
                                        if self.back(camp_updated,'self.manage_volunteer_system()'):
                                            return
                                        elif self.Admin.raise_error_for_inexistence('camp',edit_check=True,plan_name=updated_inf,camp_name=camp_updated):
                                            self.Admin.edit_volunteer_details(username=volunteer_selected,plan_name=updated_inf,camp_name=camp_updated)
                                        else:
                                            continue

                                    else:
                                        raise unable_change_plan
                                except unable_change_plan as e:
                                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
                                    continue
                            else:
                                continue

                        #camp check
                        elif index_selected == '2':
                            connection = sqlite3.connect('db.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
                            cursor = connection.cursor()
                            query = "SELECT plan_name FROM volunteer WHERE username="+ "'" + volunteer_selected +"'"
                            cursor.execute(query)
                            a = cursor.fetchone()
                            planname_selected_volun = a[0]
                            self.Admin.display_plan_summary(planname_selected_volun,prompt=False)
                            connection.close()

                            updated_inf = input(
                                "Input the new " + profile_dict[index_selected].replace("_", ' ') + ": ")
                            if self.back(updated_inf, 'self.manage_volunteer_system()'):
                                return

                            elif self.Admin.raise_error_for_inexistence('camp',edit_check=False,camp_name=updated_inf,plan_name=planname_selected_volun):
                                try:
                                    '''check if volunteer can be moved to other camps'''
                                    if self.Admin.raise_error_for_inexistence('volunteer',edit_check=True,username=volunteer_selected,reassignable="FALSE"):
                                        self.Admin.edit_volunteer_details(username=volunteer_selected,camp_name=updated_inf)
                                    else:
                                        raise unable_change_camp
                                except unable_change_camp as e:
                                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
                                    continue
                            else:
                                continue

                        #availability check
                        elif index_selected == '6':
                            day_dict = {
                                '1': "Monday",
                                '2': "Tuesday",
                                '3': "Wednesday",
                                '4': "Thursday",
                                '5': "Friday",
                                '6': "Saturday",
                                '7': "Sunday",
                            }
                            updated_inf = input(
                                "Input the new " + profile_dict[index_selected].replace("_", ' ') +" (Weekday number 1-7 splitted by comma e.g.'1,2' for 'Monday,Tuesday')"+ ": ")
                            if self.back(updated_inf, 'self.manage_volunteer_system()'):
                                return
                            else:
                                updated_inf = updated_inf.split(',')
                                try:
                                    for i in updated_inf:
                                        if i not in day_dict.keys():
                                            raise Invalid_value
                                    else:
                                        updated_inf = [day_dict[i] for i in updated_inf]
                                        updated_inf = ','.join(updated_inf)
                                        self.Admin.edit_volunteer_details(username=volunteer_selected,availability=updated_inf)
                                except Invalid_value as e:
                                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
                                    continue


                        ###display the profile again
                        elif index_selected == '8':
                            self.Admin.view_volunteer_details(volunteer_selected,prompt=False)
                            continue


                        selection_inputloop = False
                    else:
                        raise option_not_existed
                except option_not_existed as e:
                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))


            self.queue.append('self.manage_volunteer_system()')
        else:
            self.queue.append('self.edit_a_volunteer()')

### deactivate a volunteer account ###
    def deactivate_a_volunteer_account(self):
        volunteer_selected = input("\n"
                                   "Please complete the following information or Input b to back\n"
                                   "Volunteer name: ")
        if self.back(volunteer_selected, 'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('volunteer',edit_check=True,username=volunteer_selected):
            self.Admin.view_volunteer_details(volunteer_selected,prompt=False)

            doublecheck_loop = True
            while doublecheck_loop:
                doublecheck = input("Do you want to deactivate this volunteer?: \n"
                                "Input y for yes and n for no: ")
                try:
                    if self.back(doublecheck,'self.manage_volunteer_system()'):
                        return
                    elif doublecheck == 'y':
                        self.Admin.deactivate_volunteer(volunteer_selected)
                        doublecheck_loop = False
                    elif doublecheck == 'n':
                        self.queue.append('self.deactivate_a_volunteer_account()')
                        return
                    else:
                        raise option_not_existed
                except option_not_existed as e:
                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            self.queue.append('self.manage_volunteer_system()')
        else:
            self.queue.append('self.deactivate_a_volunteer_account()')

### activate a volunteer account ###
    def activate_a_volunteer_account(self):
        volunteer_selected = input("\n"
                                   "Please complete the following information or Input b to back\n"
                                   "Volunteer name: ")
        if self.back(volunteer_selected, 'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('volunteer', edit_check=True, username=volunteer_selected):
            self.Admin.view_volunteer_details(volunteer_selected,prompt=False)

            doublecheck_loop = True
            while doublecheck_loop:
                doublecheck = input("Do you want to activate this volunteer?: \n"
                                    "Input y for yes and n for no: ")
                try:
                    if self.back(doublecheck, 'self.manage_volunteer_system()'):
                        return
                    elif doublecheck == 'y':
                        self.Admin.activate_volunteer(volunteer_selected)
                        doublecheck_loop = False
                    elif doublecheck == 'n':
                        self.queue.append('self.activate_a_volunteer_account()')
                        return
                    else:
                        raise option_not_existed
                except option_not_existed as e:
                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            self.queue.append('self.manage_volunteer_system()')
        else:
            self.queue.append('self.activate_a_volunteer_account()')

### delete a volunteer ###
    def delete_a_volunteer(self):
        volunteer_selected = input("\n"
                                   "Please complete the following information or Input b to back\n"
                                   "Volunteer name: ")
        if self.back(volunteer_selected, 'self.manage_volunteer_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('volunteer', edit_check=True, username=volunteer_selected):
            self.Admin.view_volunteer_details(volunteer_selected,prompt=False)
            doublecheck_loop = True
            while doublecheck_loop:
                doublecheck = input("Do you want to activate this volunteer?: \n"
                                    "Input y for yes and n for no: ")
                try:
                    if self.back(doublecheck, 'self.manage_volunteer_system()'):
                        return
                    elif doublecheck == 'y':
                        self.Admin.delete_volunteer(volunteer_selected)
                        doublecheck_loop = False
                    elif doublecheck == 'n':
                        self.queue.append('self.delete_a_volunteer()')
                        return
                    else:
                        raise option_not_existed
                except option_not_existed as e:
                    log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))

            self.queue.append('self.manage_volunteer_system()')

        else:
            self.queue.append('self.delete_a_volunteer()')

### check availability of volunteers ###
    def check_availability(self):
        try:
            try:
                slot_check = input("\n"
                                       "Please complete the following information or Input b to back\n"
                                           "Input the time slot to check availability(in the form of int 1-7 as Monday-Sunday): ")

                if self.back(slot_check,'self.manage_volunteer_system()'):
                    return
                else:
                    slot1 = int(slot_check)
                    plan_selected = input("Input the plan to search(Default Null): ")
                    if self.back(plan_selected,'self.manage_volunteer_system()'):
                        return
                    elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check=True,plan_name=plan_selected):

                        camp_selected = input("Input the camp to search(Default Null): ")
                        if self.back(camp_selected, 'self.manage_volunteer_system()'):
                            return
                        elif self.Admin.raise_error_for_inexistence('camp', edit_check=True, plan_name=plan_selected,camp_name=camp_selected):
                            pass
                        else:
                            camp_selected = None
                    else:
                        plan_selected = None
                        camp_selected = None



                    self.Admin.availability(slot1,plan_name=plan_selected,camp_name=camp_selected)

                self.queue.append('self.manage_volunteer_system()')

            except:
                raise Invalid_value
        except Invalid_value as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.check_availability()')


################################################ Manage messaging system ###############################################
    def manage_messaging_system(self):
        user_input = input("________________________________________\n"
                           "         Manage messaging system\n"
                           "\n"
              "(1) Create a public announcement\n"
              "(2) Create a regional announcement\n"
              "(3) Display a plan message\n"
              "(4) Display a camp message\n"
              "(5) Display admin exclusive messages\n"
              "(6) Delete admin exclusive messages\n"
              "(b) Back to Admin Menu\n"
              "(q) Quit\n"
              "\n---➤ "
        )

        try:
            if user_input == "q":
                goodbye()
                self.queue.append(self.manage_messaging_system_dict[user_input])
                # always pass
            elif user_input in list(self.manage_messaging_system_dict.keys()):
                self.queue.append(self.manage_messaging_system_dict[user_input])
            else:
                raise option_not_existed
        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.manage_messaging_system()')

### Create a public announcement ###
    def create_public_announcements(self):
        announce = input("\n"
                                   "Please complete the following information or Input b to back\n"
                                   "New announcement: ")
        if self.back(announce,'self.manage_messaging_system()'):
            return
        else:
            self.Admin.create_admin_announcement(announce)
        self.queue.append('self.manage_messaging_system()')

### Create a reginal announcement ###
    def create_regional_announcements(self):
        where_publish = input("\n"
                                   "Please complete the following information or Input b to back\n"
                                   "(1) Plan announcement\n"
                              "(2) Camp announcement\n"
                              "Select the type of announcement:")

        try:
            if self.back(where_publish,'self.manage_messaging_system()'):
                return


            # plan announcement
            elif where_publish == '1':

                plan_selection_loop = True
                while plan_selection_loop:
                    self.Admin.list_existing_plans(prompt=False)
                    plan_selected = input("Please choose the plan to publish announcement: ")
                    if self.back(plan_selected,'self.manage_messaging_system()'):
                        return
                    elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check=True,plan_name=plan_selected):
                        announce = input("New announcement: ")
                        if self.back(announce,'self.manage_messaging_system()'):
                            return
                        else:
                            self.Admin.create_admin_announcement(announce,plan_name=plan_selected)
                    else:
                        continue
                    plan_selection_loop = False



            # camp announcement
            elif where_publish == '2':

                plan_selection_loop = True
                while plan_selection_loop:
                    self.Admin.list_existing_plans(prompt=False)
                    plan_selected = input("Please choose the plan to publish camp announcement: ")
                    if self.back(plan_selected, 'self.manage_messaging_system()'):
                        return
                    elif self.Admin.raise_error_for_inexistence('emergency_plan', edit_check=True,plan_name=plan_selected):

                        camp_selection_loop = True
                        while camp_selection_loop:
                            self.Admin.display_plan_summary(plan_selected,prompt=False)
                            camp_selected = input("Please choose the camp to publish announcement: ")
                            if self.back(camp_selected,'self.manage_messaging_system()'):
                                return

                            elif self.Admin.raise_error_for_inexistence('camp',plan_name=plan_selected,camp_name=camp_selected):

                                announce = input("New announcement: ")
                                if self.back(announce, 'self.manage_messaging_system()'):
                                    return
                                else:
                                    self.Admin.create_admin_announcement(announce, plan_name=plan_selected,camp_name=camp_selected)
                            else:
                                continue
                            camp_selection_loop = False

                    else:
                        continue
                    plan_selection_loop = False

            else:
                raise option_not_existed

            self.queue.append('self.manage_messaging_system()')

        except option_not_existed as e:
            log_admin.error(self.Admin.bi_color_text(f"{e}", font_color='r'))
            self.queue.append('self.create_regional_announcements()')

### Display a plan message ###
    def display_plan_messages(self):
        print("\n")
        self.Admin.list_existing_plans(prompt=False)
        plan_selected = input(
                                   "Please complete the following information or Input b to back\n"
                                   "Plan name: ")

        if self.back(plan_selected,'self.manage_messaging_system()'):
            return
        elif self.Admin.raise_error_for_inexistence('emergency_plan',edit_check=True,plan_name=plan_selected):
            self.Admin.display_messages_in_a_plan(plan_selected)
            self.queue.append('self.manage_messaging_system()')
        else:
            self.queue.append('self.display_plan_messages()')

### Display a camp message ###
    def display_camp_messages(self):
        print("\n")
        self.Admin.list_existing_plans(prompt=False)
        plan_selected = input(
                                   "Please complete the following information or Input b to back\n"
                                   "Plan name: ")

        if self.back(plan_selected, 'self.manage_messaging_system()'):
            return

        elif self.Admin.raise_error_for_inexistence('emergency_plan', edit_check=True, plan_name=plan_selected):

            camp_selection_loop = True
            while camp_selection_loop:
                self.Admin.display_plan_summary(plan_selected,prompt=False)
                camp_selected = input("Camp name: ")
                if self.back(camp_selected,'self.manage_messaging_system()'):
                    return

                elif self.Admin.raise_error_for_inexistence('camp',edit_check=True,plan_name=plan_selected,camp_name=camp_selected):
                    self.Admin.display_messages_from_a_camp(plan_selected,camp_selected)

                else:
                    continue
                camp_selection_loop = False

            self.queue.append('self.manage_messaging_system()')
        else:
            self.queue.append('self.display_camp_messages()')

### Display admin exclusive message ###
    def display_admin_exclusive_messages(self):
        print('\n')
        self.Admin.display_admin_exclusive_messages()
        self.queue.append('self.manage_messaging_system()')

### Delete admin exclusisve message ###
    def delete_admin_exclusive_messages(self):
        print('\n')
        self.Admin.delete_admin_exclusive_messages()
        self.queue.append('self.manage_messaging_system()')


################################################# Manage logging system ################################################


### display the log ###
    def display_log(self):
        print('\n')
        self.Admin.display_logs()
        self.queue.append('self.admin_menu()')


### Reset the log ###
    # def reset_log(self):
    #     pass
    #     self.queue.append('self.manage_logging_system()')
