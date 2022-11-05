def insert_sql_generation(table_name, *attr, **kwargs):
    """
    used to generate sql commands to insert rows
    :param table_name:
    :param attr: a tuple that stores or the values to pass into the command
    :param kwargs: a dictionary used to insert rows with default values
    :return: sql cmd
    """
    # This means the table we try to insert includes default values
    if kwargs:
        k_list = [key for key in kwargs]
        v_list = list(map(lambda x:f"'{str(x)}'" if type(x)==str else str(x),[kwargs[key] for key in k_list]))
        return f"INSERT INTO {table_name}({','.join(k_list)}) VALUES({','.join(v_list)})"
    val = list(map(lambda x: f"'{str(x)}'", attr))
    return f"INSERT INTO {table_name} VALUES({','.join(val)})"

def update_sql_generation(table_name,*args,**kwargs):
    """
    used to generate sql commands to update tables.
    :param table_name: table name
    :param args: attribute_name and its value
    :param kwargs: mandatory constraints, the conditions after WHERE in sql commands.
    :return:
    """
    attribute = ','.join([f"{args[i]}='{args[i+1]}'" for i in range(0,len(args)-1,2)])
    constraint = ' and '.join([f"{key}='{kwargs[key]}'" for key in kwargs.keys()])
    return f"UPDATE {table_name} SET {attribute} WHERE {constraint}"

def select_sql_generation(table_name,*coulmn,**kwargs):
    """
    :param table_name: table name
    :param coulmn: columns you want to print out, it can also be sql functions.
    :param kwargs: optional parameters after WHERE
    :return:
    """
    attribute = ','.join([str(ele) for ele in coulmn])
    if len(kwargs) == 0:
        return f"SELECT {attribute} FROM {table_name}"
    else:
        constraint =  ' and '.join([f"{key}='{kwargs[key]}'" for key in kwargs.keys()])
        return f"SELECT {attribute} FROM {table_name} WHERE {constraint}"
