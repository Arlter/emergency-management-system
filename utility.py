import datetime

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