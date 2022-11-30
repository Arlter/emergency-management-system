"""
Structure:

Volunteer menu:
[1] Display your camp's information
    - check input [method 26: raise_error_for_inexistence]
    - display camp info [method 29: list_emergency_profile]

[2] Manage refugee profile
    [1] Create refugee profile
        - check input [method 25: raise_error_for_existence]
        - create refugee [method 27: create_refugee_profile]
    [2] Display refugee profile
        - check input [method 26: raise_error_for_inexistence]
        - display refugee [method 30: display_emergency_profile] *confusing name
    [3] Update refugee profile
        - check input [method 26: raise_error_for_inexistence]
        - update refugee [method 28: update_refugee_profile]

[3] Messaging system
    [1] Display admin announcements
        - check existence [method 26: raise_error_for_inexistence]
        - display admin message [method 35: vols_display_message] *use corresponding inputs
    [2] Send message to admin
        - send message to admin [method 36: vols_send_message] *use corresponding inputs
    [3] Display messages from your camp
        - check existence [method 26: raise_error_for_inexistence]
        - display admin message [method 35: vols_display_message] *use corresponding inputs
    [4] Send message to your camp
        - send message to admin [method 36: vols_send_message] *use corresponding inputs

[4] Manage personal profile
    [1] Display personal profile
        - display personal profile [method 32: display_personal_profile]
    [2] Edit personal profile
        - edit personal profile [method 33: edit_personal_profile]

In every menu:
[q] Logout
[b] Back (except in main menu)

***probably don't have to use [method 31: create_personal_profile] and 
[method 34: availability] in the volunteer menu?

"""


class VolunteerMenu:
    def __init__(self):
        self.Ifback = False
        self.queue = []


        self.volunteer_menu_dict = {
            "1": "self.manage_emergency_system()",
            "2": "self.manage_refugee_profile()",
            "3": "self.edit_personal_profile()",
            "4": "self.messaging_system()"}

        self.queue.append('self.volunteer_menu()')

        while len(self.queue) != 0:
            eval(self.queue[0])
            self.queue = self.queue[1:]

    def volunteer_menu(self):
        print("Welcome! Your role is Volunteer")

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