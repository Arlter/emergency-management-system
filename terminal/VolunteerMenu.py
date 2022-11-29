

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