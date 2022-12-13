class already_exists(Exception):
    def __init__(self, table_name, **kwargs):
        self.message = f"The tuple with the value {','.join([str(kwargs[key]) for key in kwargs])} has existed in the table {table_name}. Please enter another."
        super().__init__(self.message)

class absent(Exception):
    def __init__(self, table_name, **kwargs):
        self.message = f"The tuple with the value {','.join([str(kwargs[key]) for key in kwargs])} is not found in the table {table_name}. Please enter another."
        super().__init__(self.message)

class closed_plan(Exception):
    def __init__(self):
        self.message = f"The associated emergency plan has been closed and archived. Modifications to the pertinent data are not applicable.   "
        super().__init__(self.message)

class option_not_existed(Exception):
    def __init__(self):
        self.message = f"Invalid option. Please select from the menu."
        super().__init__(self.message)

class Invalid_value(Exception):
    def __init__(self):
        self.message = f"Invalid value. Please input in the correct format."
        super().__init__(self.message)

class unable_change_plan(Exception):
    def __init__(self):
        self.message = f"The volunteer can not be reassigned as his plan is ongoing."
        super().__init__(self.message)

class unable_change_camp(Exception):
    def __init__(self):
        self.message = f"The volunteer can not be reassigned to as his plan has been closed."
        super().__init__(self.message)

class invalid_login(Exception):
    def __init__(self):
        self.message = f"Invalid login, please try again."
        super().__init__(self.message)