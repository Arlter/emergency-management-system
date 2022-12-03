import sqlite3
from volunteer import *
from exceptions import *
from logging_configure import *

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
    def __init__(self):
        self.Ifback = False
        self.queue = []
        # have to add new attributes?
        self.username = None
        self.plan = None
        self.camp = None

        self.volunteer_menu_dict = {
            "1": "self.display_camp()",
            "2": "self.manage_refugee_profile()",
            "3": "self.messaging_system()",
            "4": "self.manage_personal_profile()"}

        self.queue.append('self.volunteer_menu()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]

    def volunteer_menu(self):
        print("""
        Welcome! Your role is Volunteer
        [1] Display camp information
        [2] Manage refugee profile
        [3] Messaging System
        [4] Manage personal profile
        [q] Logout
        """)
        
        user_input = input("Please select an option: ")

        if user_input == "q":
            print("Goodbye!")
            pass  # always pass

        elif user_input == "b": #used for relogin
            self.Ifback = True
        else:
            try:
                self.queue.append(self.volunteer_menu_dict[user_input])

            except:
                print("Invalid option!")
                self.queue.append('self.volunteer_menu()')








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

        print("""
        Messaging System
        [1] Display admin announcements
        [2] Send message to admin
        [3] Display messages from your camp
        [4] Send message to your camp
        [b] Go back to previous page
        [q] Logout
        """)
        
        user_input = input("Please select an option: ")

        if user_input == "q":
            print("Goodbye!")
            pass  # always pass
        elif user_input == "b":
            self.Ifback = True  # how to use this?
            pass
        else:
            try:
                self.queue.append(self.messaging_system_dict[user_input])
            except Exception as e:  # what exception to use?
                print("Invalid option!")
                log_volunteer.error("Invalid input to messaging menu") 
                self.queue.append('self.messaging_system()')
        pass

    # 3.1 Display admin announcements
    def display_admin_announcements(self):
        try: 
            volunteer.vols_display_message(admin_anno = True)
            # insert "press b to go back" to avoid menu automatically popping up when displaying message?
            go_back = input("Enter b to go back to the messaging system menu: ")
            if go_back == "b":
                # self.Ifback = True
                self.queue.append('self.messaging_system()')
            else:
                pass  # or use while true loop? test later
        except Exception as e:
            print("Error, please try again")
            log_volunteer.error(e) 
            self.queue.append('self.messaging_system()')

    # 3.2 Send message to admin
    def send_message_to_admin(self):
        print("""
        Send message to admin
        (Enter b to go back)
        """)

        message_to_admin = input("Please enter your message for the admin: ")

        if message_to_admin == "b":
            self.Ifback = True  # how to use this?
        else:
            try:
                volunteer.vols_send_message(self.username, message_to_admin, admin_excl=True)
                print("Message sent to admin")
                self.queue.append('self.messaging_system()')
            except Exception as e:
                print("Error, please try again")
                log_volunteer.error(e) 
                self.queue.append('self.send_message_to_admin()')

    # 3.3 Display messages from your camp
    def display_camp_messages(self):
        try:
            volunteer.vols_display_message(plan_name = self.plan, camp_name = self.camp)
            # insert "press b to go back" to avoid menu automatically popping up when displaying message?
            go_back = input("Enter b to go back to the messaging system menu: ")
            if go_back == "b":
                # self.Ifback = True
                self.queue.append('self.messaging_system()')
            else:
                pass  # or use while true loop? test later
        except Exception as e:
            print("Error, please try again")
            log_volunteer.error(e) 
            self.queue.append('self.display_camp_messages()')

    # 3.4 Send message to your camp
    def send_message_to_camp(self):
        print("""
        Send message to your camp
        (Enter b to go back)
        """)
        try:
            if volunteer.__raise_error_for_inexistence("camp", plan_name = self.plan, camp_name = self.camp):
                message_to_camp = input("Please enter your message to your camp: ")
                if message_to_camp == "b":
                    self.Ifback = True  # how to use this?
                    pass
                else:
                    try:
                        volunteer.vols_send_message(self.username, message_to_camp, plan_name = self.plan, camp_name = self.camp)
                        print("Message sent to camp")
                        self.queue.append('self.messaging_system()')
                    except Exception as e:
                        print("Error, please try again")
                        log_volunteer.error(e) 
                        self.queue.append('self.send_message_to_camp()')
            else:
                raise absent("camp", plan_name = self.plan, camp_name = self.camp)
        except absent as e:
            log_volunteer.error(e)
            print("Camp is not found or closed")
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

        print("""
        Manage personal profile
        [1] Display personal profile
        [2] Edit personal profile
        [b] Go back to previous page
        [q] Logout
        """)
        
        user_input = input("Please select an option: ")

        if user_input == "q":
            print("Goodbye!")
            pass  # always pass
        elif user_input == "b":
            self.Ifback = True  # how to use this?
            pass
        else:
            try:
                self.queue.append(self.personal_profile_dict[user_input])
            except Exception as e:  # what exception to use?
                print("Invalid option!")
                log_volunteer.error("Invalid input to manauge personal profile menu") 
                self.queue.append('self.manage_personal_profile()')
        pass
        
    def display_vol_profile(self):
        try:
            volunteer.display_personal_profile(self.username)
        except Exception as e:
            print("Error, please try again")
            self.queue.append('self.manage_personal_profile()')
        pass

    def edit_vol_profile(self):
        try:
            volunteer.edit_personal_profile(self.username)
        except Exception as e:
            print("Error, please try again")
            log_volunteer.error(e) 
            self.queue.append('self.manage_personal_profile()')



if __name__ == "__main__":
    # test for edit_personal_profile and availability
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    #vol1 = volunteer(connection, cursor)
    #vol1.create_personal_profile("plan1", "camp1", "bill", "liu", "1234567", "Monday,1-12", "vol111", "111", "TRUE", "FALSE")
    