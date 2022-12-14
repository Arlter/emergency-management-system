import datetime
from COMP0066.terminal.color_utilities import colors

##########################################database utility methods#######################################################
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




##########################################format utility methods########################################################
def bi_color_text(content, font_color='g'):
    return f"{colors.fg.green}✅ {content}{colors.reset}" if font_color == 'g' else f"{colors.fg.red}❌ {content}{colors.reset}"


def form_content(col_name:list, db_res):
    content = [col_name]
    content += [list(ele) for ele in db_res]
    return content

def make_table(content):
    # build the table
    rows=len(content)
    columns=len(content[0])

    # fix the type issue brought
    for i in range(len(content)):
        for j in range(len(content[i])):
            if type(content[i][j]) == datetime.date:
                content[i][j] = content[i][j].strftime("%Y-%m-%d")
            if type(content[i][j]) == datetime.datetime:
                content[i][j] = content[i][j].strftime("%Y-%m-%d")
            if type(content[i][j]) == type(None):
                content[i][j] = "None"
    table = ""
    # set the length of each column
    col_length = []
    # find the longest elements in each column
    for i in range(columns):
        col_length.append(0)
        for j in range(rows):
            if len(str(content[j][i])) > col_length[i]:
                col_length[i] = len(content[j][i])

    # create the first row of the table
    table += "+"
    for i in range(columns):
        for j in range(col_length[i] + 2):
            table += "="
        table += "+"
    table += "\n"

    # create the rest of the table
    for i in (range(rows)):
        for j in range(columns):
            if j == 0:
                table += "| "
            #table += str(content[i][j]) if type(content[i][j])!= "datetime.date" else datetime.datetime.strftime(content[i][j])
            table += str(content[i][j]).rjust(col_length[j])
            #for k in range(col_length[j] - len(content[i][j]) + 1):
            table += " "
            table += "| "
        table += "\n"

        # create the horizontal line between each row
        if i == 0:
            table += "+"
            for i in range(columns):
                for j in range(col_length[i] + 2):
                    table += "="
                table += "+"
            table += "\n"
            continue

        table += "+"
        for i in range(columns):
            for j in range(col_length[i] + 2):
                table += "-"
            table += "+"
        table += "\n"
    # return the table
    return table

def display_in_table(col_name:list,db_res):
    return make_table(form_content(col_name,db_res))