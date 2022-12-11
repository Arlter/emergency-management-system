import sqlite3
from volunteer import *
from exceptions import *
from logging_configure import *
import database_utilities
from terminal.color_utilities import *


"""
Assumptions:
- one volunteer can only service one camp at a time
- one volunteer can only belong to one emergency plan
- one camp can only belong to one emergency plan
- one plan can have multiple camps
- one camp can have multiple volunteers
--> so we can assume a volunteer can only manage refugee profiles
    under their own camp
--> but still have to check camp existence before calling functions to avoid errors?


*** Some thoughts:
1. Since "verify camp existence" also verifies if a camp is active or closed,
if volunteers are allowed to check camps in a closed plan,
then don't verify existence in any "display" functions,
but only in "create/edit/update" functions.
Most functions have an inner check to see if sql query returns nothing anyways

2. Another approach is to show a different "inactive volunteer menu": 
check camp existence first, if camp does not exist/ is closed, 
display a menu that allows the displaying of info, but cannot edit/create/update

3. What about deactivated volunteers? Are they stopped after login?

4. If we use "b" as go back key, then technically you can't ever create a message with just "b"

5. How to get volunteer's username? Need it as an input for functions

6. [method 31: create_personal_profile] is probably irrelevant to volunteer menu
***


Structure: (feel free to review and make changes if necessary)

Volunteer menu:
[1] Display camp information  // maybe add a function to display plan information?
    [1] Check availability of volunteers in your camp
        - verify camp existence [method 26: __raise_error_for_inexistence]
        - display camp volunteer availability [method 34: availability]  
            // probably only allow volunteer to check camp-wise, not plan-wise, because plan should be out of scope for voluntters?

[2] Manage refugee profile
    [1] List all refugee profile in your camp
        - verify camp existence [method 26: __raise_error_for_inexistence]
        - list all refugee profiles in camp [method 29: list_emergency_profile]
    [2] Find refugee profile
        - verify camp existence [method 26: __raise_error_for_inexistence]
        - display refugee profile with chosen conditions [method 30: display_emergency_profile]  //confusing name
    [3] Create refugee profile  
        - verify plan and camp existence [method 26: __raise_error_for_inexistence]  // verify inputted camp is under inputted plan?
        - create refugee profile [method 27: create_refugee_profile]
    [4] Update refugee profile
        - verify refugee profile existence [method 26: __raise_error_for_inexistence]
        - update refugee profile [method 28: update_refugee_profile]

[3] Messaging system
    [1] Display admin announcements
        - display admin message [method 35: vols_display_message] *use corresponding inputs
    [2] Send message to admin
        - send message to admin [method 36: vols_send_message] *use corresponding inputs
    [3] Display messages from your camp
        - display admin message [method 35: vols_display_message] *use corresponding inputs
    [4] Send message to your camp
        - verify camp existence [method 26: __raise_error_for_inexistence]     
        - send message to admin [method 36: vols_send_message] *use corresponding inputs

[4] Manage personal profile
    [1] Display personal profile
        - display personal profile [method 32: display_personal_profile]
    [2] Edit personal profile
        - edit personal profile [method 33: edit_personal_profile]

In every menu:
[q] Logout
[b] Back (except in main menu)


"""

class VolunteerMenu:
    def __init__(self, username):
        self.Ifback = False
        self.queue = []
        self.vol_instance = volunteer() # input class of volunteer
        self.username = username

        plansql = select_sql_generation("volunteer", "plan_name", username = self.username)
        campsql = select_sql_generation("volunteer", "camp_name", username = self.username)

        self.plan = self.vol_instance.cursor.execute(plansql).fetchall()[0][0]
        self.camp = self.vol_instance.cursor.execute(campsql).fetchall()[0][0]
        self.vol_instance.connection.commit()


        self.volunteer_menu_dict = {
            "1": "self.manage_refugee_profile()",
            "2": "self.messaging_system()",
            "3": "self.manage_personal_profile()"}

        self.queue.append('self.volunteer_menu()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]

    def quit(self):
        self.vol_instance.connection.close()

    def volunteer_menu(self):
        # print(type(self.username),self.username)
        # print(type(self.plan),self.plan)
        # print(type(self.camp),self.camp)
        user_input = input("""
Volunteer Menu
[1] Manage refugee profile
[2] Messaging System
[3] Personal profile
[b] Go back to login menu
[q] Quit

Please select an option: """)

        if user_input == "q":
            log_volunteer.info(f"{colors.bg.green}Goodbye!{colors.reset}")
            self.queue.append('self.quit()')
            pass  # always pass
        elif user_input == "b": #used for relogin
            self.Ifback = True
        elif user_input in self.volunteer_menu_dict:
            self.queue.append(self.volunteer_menu_dict[user_input])
        else:
            log_volunteer.error(f"{colors.bg.red}Invalid option, please try again{colors.reset}")
            self.queue.append('self.volunteer_menu()')

    # Tim: manage refugee profile
    def manage_refugee_profile(self):
        option = input("""
[1] List all refugee profiles in your camp
[2] Create refugee profile
[3] Update refugee profile
[b] Back
Please select an option: """)

        if option == "1":
            '''List all refugee profiles in the camp'''
            # Verify that the camp exists
            '''self.vol_instance.raise_error_for_inexistence("camp", True, self.camp)'''
            # List all refugee profiles in the camp
            self.vol_instance.list_emergency_profile(self.camp)
            # insert "press b to go back" to avoid menu automatically popping up
            userinput = input("Enter b to go back to Manage refugee profile menu: ")
            while userinput != "b":
                log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
                userinput = input("Enter b to go back to Manage refugee profile menu: ")
            else:
                self.queue.append('self.manage_refugee_profile()')

        elif option == "2":
            '''Create a refugee profile'''
            # Verify that the camp and plan exists}
            '''self.vol_instance.__raise_error_for_inexistence("camp", True, self.camp)'''
            '''self.vol_instance.__raise_error_for_inexistence("plan", True, self.plan)'''

            # Create a refugee profile
            first_name = input("Enter the refugee's first name: ")
            last_name = input("Enter the refugee's last name: ")
            family_num = input("Enter the number of family members: ")
            medical_condition = input("Enter a description of any medical health conditions: ")
            create_string = f"self.vol_instance.create_refugee_profile(plan_name = self.plan, camp_name = self.camp"
            if len(first_name) != 0:
                create_string += f", first_name = first_name"
            if len(last_name) != 0:
                create_string += f", last_name = last_name"
            if len(family_num) != 0:
                create_string += f", family_num = family_num"
            if len(medical_condition) != 0:
                create_string += f", medical_condition = medical_condition"
            create_string += ")"
            eval(create_string)
            # insert "press b to go back" to avoid menu automatically popping up
            userinput = input("Enter b to go back to Manage refugee profile menu: ")
            while userinput != "b":
                log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
                userinput = input("Enter b to go back to Manage refugee profile menu: ")
            else:
                self.queue.append('self.manage_refugee_profile()')

        elif option == "3":
            '''Update a refugee profile'''
            # Verify that the refugee profile exists
            ref_ID = input("Please input the refugee's ID: ")
            '''self.vol_instance.__raise_error_for_inexistence("profile", True, ref_ID)'''

            # Update a refugee profile
            while True:
                attr_to_update = input("""
    [1] Update first name
    [2] Update last name
    [3] Update number of family members
    [4] Update medical condition(s)
    Please select an option: """)
                if attr_to_update in ('1','2','3','4'):
                    break
                else:
                    log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            possible_attrs = ['first_name','last_name','family_num','medical_condition']
            new_value = input("Please provide the updated value: ")
            self.vol_instance.update_refugee_profile(possible_attrs[int(attr_to_update)-1], new_value, ref_ID)
            # insert "press b to go back" to avoid menu automatically popping up
            userinput = input("Enter b to go back to Manage refugee profile menu: ")
            while userinput != "b":
                log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
                userinput = input("Enter b to go back to Manage refugee profile menu: ")
            else:
                self.queue.append('self.manage_refugee_profile()')

        elif option == "b":
            self.queue.append('self.volunteer_menu()')

        else:
            log_volunteer.error("Invalid input to Manage refugee profile menu")
            self.queue.append('self.manage_refugee_profile()')




    # Angel: messaging system, personal profile
    """
    [3] Messaging system
        [1] Display admin announcements
            - display admin message [method 35: vols_display_message] *use corresponding inputs
        [2] Send message to admin
            - send message to admin [method 36: vols_send_message] *use corresponding inputs
        [3] Display messages from your camp
            - verify camp existence [method 26: __raise_error_for_inexistence]
            - display admin message [method 35: vols_display_message] *use corresponding inputs
        [4] Send message to your camp
            - verify camp existence [method 26: __raise_error_for_inexistence]     
            - send message to admin [method 36: vols_send_message] *use corresponding inputs
    """ 

    # 3. Messaging system

    def messaging_system(self):

        self.messaging_system_dict = {
            "1": "self.display_admin_announcements()",
            "2": "self.send_message_to_admin()",
            "3": "self.display_camp_messages()",
            "4": "self.send_message_to_camp()"}
        
        user_input = input("""
Messaging System
[1] Display admin announcements
[2] Send message to admin
[3] Display messages from your camp
[4] Send message to your camp
[b] Go back to previous page
[q] Quit

Please select an option: """)

        if user_input == "q":
            log_volunteer.info(f"{colors.bg.green}Goodbye!{colors.reset}")
            self.queue.append('self.quit()')
        elif user_input == "b":
            self.queue.append('self.volunteer_menu()')
        elif user_input not in self.messaging_system_dict:
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            self.queue.append('self.messaging_system()')
        else:
            self.queue.append(self.messaging_system_dict[user_input])

    # 3.1 Display admin announcements
    def display_admin_announcements(self): 
        self.vol_instance.vols_display_message(admin_anno = True)
        # insert "press b to go back" to avoid menu automatically popping up when displaying message
        userinput = input("Enter b to go back to Messaging System menu: ")
        while userinput != "b":
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            userinput = input("Enter b to go back to Messaging System menu: ")
        else: 
            self.queue.append('self.messaging_system()')
        
    # 3.2 Send message to admin
    def send_message_to_admin(self):
        message_to_admin = input("""
Send message to admin
(Enter b to go back)

Please enter your message for the admin: """)

        if message_to_admin == "b":
            self.queue.append('self.messaging_system()')
        elif message_to_admin == "":
            log_volunteer.error(f"{colors.bg.red}Message to admin cannot be empty, please try again{colors.reset}")
            self.queue.append('self.send_message_to_admin()')
        else:
            if self.vol_instance.vols_send_message(self.username, self.plan, message_to_admin, admin_excl=True):
                log_volunteer.info(f"{colors.bg.green}Success! Message sent to admin{colors.reset}")
            self.queue.append('self.messaging_system()')


    # 3.3 Display messages from your camp
    def display_camp_messages(self):
        self.vol_instance.vols_display_message(plan_name = self.plan, camp_name = self.camp)
        # insert "press b to go back" to avoid menu automatically popping up when displaying message
        userinput = input("Enter b to go back to Messaging System menu: ")
        while userinput != "b":
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            userinput = input("Enter b to go back to Messaging System menu: ")
        else: 
            self.queue.append('self.messaging_system()')


    # 3.4 Send message to your camp
    def send_message_to_camp(self):

        # verify existence of camp
        

        message_to_camp = input("""
Send message to your camp
(Enter b to go back)

Please enter your message to your camp: """)
        if message_to_camp == "b":
            self.queue.append('self.messaging_system()')
        elif message_to_camp == "":
            log_volunteer.error(f"{colors.bg.red}Message to camp cannot be empty, please try again{colors.reset}")
            self.queue.append('self.send_message_to_admin()')
        else:
            if self.vol_instance.vols_send_message(self.username, self.plan, message_to_camp, plan_name = self.plan, camp_name = self.camp):
                log_volunteer.info(f"{colors.bg.green}Success! Message sent to your camp{colors.reset}")
            self.queue.append('self.messaging_system()')


    """
    [4] Manage personal profile
        [1] Display personal profile
            - display personal profile [method 32: display_personal_profile]
        [2] Edit personal profile
            - edit personal profile [method 33: edit_personal_profile]
    """

    # 4. Personal profile
    def manage_personal_profile(self):
        self.personal_profile_dict = {
            "1": "self.display_vol_profile()",
            "2": "self.edit_vol_profile()"}
        
        user_input = input("""
Personal profile
[1] Display personal profile
[2] Edit personal profile
[b] Go back to Volunteer Menu
[q] Quit

Please select an option: """)

        if user_input == "q":
            log_volunteer.info(f"{colors.bg.green}Goodbye!{colors.reset}")
            self.queue.append('self.quit()')
        elif user_input == "b":
            self.queue.append('self.volunteer_menu()')
        elif user_input not in self.personal_profile_dict:
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            self.queue.append('self.manage_personal_profile()')
        else:
            self.queue.append(self.personal_profile_dict[user_input])
        
    def display_vol_profile(self):
        self.vol_instance.display_personal_profile(self.username)
        # insert "press b to go back" to avoid menu automatically popping up when displaying message
        userinput = input("Enter b to go back to the Personal Profile menu, or enter e to edit profile: ")
        while userinput != "b" and userinput != "e":
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            userinput = input("Enter b to go back to the Personal Profile menu, or enter e to edit profile: ")
        else:
            if userinput == "b": 
                self.queue.append('self.manage_personal_profile()')
            elif userinput == "e":
                self.queue.append('self.edit_vol_profile()')


# not done yet
    def edit_vol_profile(self):  # FIXME: what data can volunteers edit by themselves?

        self.edit_vol_prof_dict = {
            "1": "first_name",
            "2": "last_name",
            "3": "phone_num",
            "4": "availability",
            "5": "password",
            "6": "display_personal_profile"}
        
        user_input = input("""
Edit personal profile
[1] First name
[2] Last name
[3] Phone number
[4] Availability
[5] Account password
[6] Display personal profile
[b] Go back to Personal Profile menu
[q] Quit

Please choose the personal detail you want to edit (1-5): """)

        
        if user_input == "q":
            log_volunteer.info(f"{colors.bg.green}Goodbye!{colors.reset}")
            self.queue.append('self.quit()')

        elif user_input == "b":
            self.queue.append('self.manage_personal_profile()')

        elif user_input not in self.edit_vol_prof_dict:
            log_volunteer.error(f"{colors.bg.red}Invalid input, please try again{colors.reset}")
            self.queue.append('self.edit_vol_profile()')

        elif user_input == "1":
            updated_data = input("Please input the new first name: ")
            if self.vol_instance.edit_personal_profile(self.username, first_name = updated_data):
                log_volunteer.info(f"{colors.bg.green}Edit success!{colors.reset}")
            self.queue.append('self.edit_vol_profile()')

        elif user_input == "2":
            updated_data = input("Please input the new last name: ")
            if self.vol_instance.edit_personal_profile(self.username, last_name = updated_data):
                log_volunteer.info(f"{colors.bg.green}Edit success!{colors.reset}")
            self.queue.append('self.edit_vol_profile()')

        elif user_input == "3":
            updated_data = input("Please input the new phone number: ")
            while not updated_data.isdigit():
                log_volunteer.error(f"{colors.bg.red}Phone number can only consists of numbers, please try again{colors.reset}")
                updated_data = input("Please input the new phone number: ")
            else:
                if self.vol_instance.edit_personal_profile(self.username, phone_num = updated_data):
                    log_volunteer.info(f"{colors.bg.green}Edit success!{colors.reset}")
                else:
                    log_volunteer.info(f"{colors.bg.red}Error, please try again{colors.reset}")
            self.queue.append('self.edit_vol_profile()')

        elif user_input == "4":
            weekdays = []
            while True:
                weekday = input("""
[1] Monday
[2] Tuesday
[3] Wednesday
[4] Thursday
[5] Friday
[6] Saturday
[7] Sunday
[8] I've finished selecting my available days. Update my records.
Please select your available week days. Input one at a time: """)
                if weekday in ('1','2','3','4','5','6','7'):
                    weekdays.append(str(weekday))
                elif weekday == '8':
                    break
                else:
                    log_volunteer.error(f"{colors.bg.red}Invalid day input, please try again{colors.reset}")
            if len(weekdays) != 0:
                self.vol_instance.edit_personal_profile(self.username, availability=','.join(sorted(list(set(weekdays)))))
                log_volunteer.info(f"{colors.bg.green}Edit success!{colors.reset}")
            #log_volunteer.info(f"{colors.bg.red}Error, please try again{colors.reset}")
            self.queue.append('self.edit_vol_profile()')
            
        elif user_input == "5":
            updated_data = input("Please input the new password: ")
            if self.vol_instance.edit_personal_profile(self.username, password = updated_data):
                log_volunteer.info(f"{colors.bg.green}Edit success!{colors.reset}")
            self.queue.append('self.edit_vol_profile()')
        
        elif user_input == "6":
            self.queue.append('self.display_vol_profile()')