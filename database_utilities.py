def insert_sql_generation(table_name, *attr):
    """
    used to generate sql commands to insert rows
    :param table_name:
    :param attr: a tuple that stores or the values to pass into the command
    :return: sql cmd
    """
    val = list(map(lambda x: f"'{str(x)}'",attr))
    return f"INSERT INTO {table_name} VALUES({','.join(val)})"

def update_sql_generation(table_name,attribute_name,new_val,**kwargs):
    """
    Used to generate sql commands to update a row of a table
    :param table_name: the table where you want the update to occur
    :param attribute_name: the target column in the table
    :param new_val: the value to enter for updating
    :param kwargs: primary keys. can be composite keys
    :return: sql cmd
    """
    string = ' and '.join([f"{key}='{kwargs[key]}'" for key in kwargs.keys()])
    return f"UPDATE {table_name} SET {attribute_name} = '{new_val}' WHERE {string}"

def update_sql_generation(table_name,*args,**kwargs):
    """

    :param table_name:
    :param args: attribute_name and its value
    :param kwargs: constraints, the conditions after WHERE in sql commands.
    :return:
    """
    attribute = ','.join([f"{args[i]}='{args[i+1]}'" for i in range(len(args)-1)])
    constraint = ' and '.join([f"{key}='{kwargs[key]}'" for key in kwargs.keys()])
    return f"UPDATE {table_name} SET {attribute} WHERE {constraint}"