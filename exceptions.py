class already_exists(Exception):
    def __init__(self, table_name, **kwargs):
        self.message = f"* The tuple with the value {','.join([str(kwargs[key]) for key in kwargs])} has existed in the table {table_name}. Please enter another."
        super().__init__(self.message)

class absent(Exception):
    def __init__(self, table_name, **kwargs):
        self.message = f"* The tuple with the value {','.join([str(kwargs[key]) for key in kwargs])} is not found in the table {table_name}. Please enter another."
        super().__init__(self.message)

class closed_plan(Exception):
    def __init__(self):
        self.message = f"* The associated emergency plan has been closed and archived. Modifications to the pertinent data are not applicable.   "
        super().__init__(self.message)