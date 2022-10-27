import json


class account:
    """
    This class is used for 'create_or_update', 'login' and 'logout' operations for users
    All inputs should be in string format, and there are two valid roles: 'admin' and 'volunteer'
    """

    # user should specify the username and password when creating object
    def __init__(self, username: str, password: str, role: str):
        self.username = username
        self.password = password
        self.role = role
        self.status = False
        self.__check_empty_json()

    def create_or_update(self):
        """
        create an account according to role, username and password
        or update the password if previous record exists.
        NOTE: only one admin could exist, attempts to create two or more admin account would fail
        """
        self.__check_empty_json()
        accounts = open('files/accounts.json', 'r')
        acc_dict = json.load(accounts)
        if self.role == 'admin':
            try:
                bindings = acc_dict['admin']
            except KeyError:  # an error raised because it is the first time an admin being registered
                acc_dict['admin'] = {self.username: self.password}
                print("Your %s account has been created successfully, username: %s" % (self.role, self.username))
            else:  # if no error, only updating password is allowed
                if self.username != list(bindings.keys())[0]:
                    print("Sorry, there has been one administrator account created.")
                else:
                    bindings[self.username] = self.password  # !!!!!! maybe add new verification process here
                    print("You have successfully updated your password")
            finally:
                accounts.close()
                accounts = open('files/accounts.json', 'w')
                accounts.write(json.dumps(acc_dict, indent=4))
                accounts.close()
                return
        elif self.role == 'volunteer':
            try:
                bindings = acc_dict['volunteer']
            except KeyError:  # an error raised because it is the first time an admin being registered
                acc_dict['volunteer'] = {self.username: self.password}
                print("Your %s account has been created successfully, username: %s" % (self.role, self.username))
            else:  # if no error, add a new binding or update the password
                if self.username in list(bindings.keys()):
                    bindings[self.username] = self.password  # !!!!!! maybe add new verification process here
                    print("You have successfully updated your password")
                else:
                    bindings[self.username] = self.password
                    print("Your %s account has been created successfully, username: %s" % (self.role, self.username))
            finally:
                accounts.close()
                accounts = open('files/accounts.json', 'w')
                accounts.write(json.dumps(acc_dict, indent=4))
                accounts.close()
                return

    def login(self):
        """
        Login using the current username and password.
        If successful the status will become 'True'
        """
        self.__check_empty_json()
        accounts = open('files/accounts.json', 'r')
        acc_dict = json.load(accounts)
        if self.status:
            print("You are already online!")
            return
        if self.role == 'admin':
            try:
                bindings = acc_dict['admin']
            except KeyError:
                print("Login fails, please try again. Error: no such admin account")
            else:
                if self.username in list(bindings.keys()) and bindings[self.username] == self.password:
                    self.status = True
                    print("Login successful, your role is %s and you are %s. Welcome back!" % (self.role, self.username))
                else:
                    print("Login fails, please try again. Error: no such %s account" % self.role)
            finally:
                accounts.close()
        elif self.role == 'volunteer':
            try:
                bindings = acc_dict['volunteer']
            except KeyError:
                print("Login fails, please try again. Error: no such %s account" % self.role)
            else:
                if self.username in list(bindings.keys()) and bindings[self.username] == self.password:
                    self.status = True
                    print("Login successful, your role is %s, and you are %s. Welcome back!" % (self.role, self.username))
                else:
                    print("Login fails, please try again. Error: no such %s account" % self.role)
            finally:
                accounts.close()

    def logout(self):
        """
        Logout will turn the current status into 'False'
        """
        if self.status is True:
            self.status = False
            print("You have successfully logout. Art will be missing you. TAT ")
        else:
            print("Logout fails! You have not logged in")

    def __delete_all_account(self):
        # the operation needs admin privilege and is hidden for normal user
        if self.role == 'admin' and self.status is True:
            acc = open('files/accounts.json', 'w')
            acc.write('')
            acc.close()
            print("All accounts deleted successfully")
            return

    def __delete_one_account(self, role: str, username: str):
        # the operation needs admin privilege and is hidden for normal user
        if self.role == 'admin' and self.status is True:
            self.__check_empty_json()
            acc = open('files/accounts.json', 'r')
            acc_dict = json.load(acc)
            try:
                bindings = acc_dict[role]
            except KeyError:
                print("No such category of account created")
                return
            else:
                try:
                    bindings.pop(username)
                except KeyError:
                    print("No such user exists")
                    return
            finally:
                acc.close()
                acc = open('files/accounts.json', 'w')
                acc.write(json.dumps(acc_dict, indent=4))
                acc.close()

    # make sure json file contains a dictionary
    @staticmethod
    def __check_empty_json():
        accounts = open('files/accounts.json', 'r')
        if accounts.read() == '':
            accounts.close()
            accounts = open('files/accounts.json', 'w')
            accounts.write(json.dumps(dict(), indent=4))
            accounts.close()


if __name__ == "__main__":
    #tests
    new_acc_admin = account('administrator', '111', 'admin')
    new_acc_admin.create_or_update()                                # successful
    new_acc_admin.login()
    sec_acc_admin = account('admin2', '111', 'admin')
    sec_acc_admin.create_or_update()                                # unsuccessful - one admin account already exists
    new_acc_volun = account('Art', 'Art123', 'volunteer')
    new_acc_volun.create_or_update()
    new_acc_volun.login()                                           # successful
    new_acc_volun.logout()                                          # log out
    new_acc_volun2 = account('Art2', 'Art12345', 'volunteer')
    new_acc_volun2.login()                                          # attempt to log in without creating an account would fail
    new_acc_admin._account__delete_one_account('volunteer', 'Art')  # delete one specific account
    new_acc_volun.login()                                           # unsuccessful - deleted account
    new_acc_volun3 = account('paperwings2019', '111', 'volunteer')
    new_acc_volun3.create_or_update()
    new_acc_volun3.login()
    new_acc_volun3.logout()