import sqlite3
import pandas as pd
"""
    Assumptions:
        one volunteer can only service one camp at a time.
        one camp can only belong to one emergency plan.
"""

def initiate(cursor):
    """
    used to initiate the database to create tables.
    :param cursor: pass a cursor to execute sql commands to create tables
    :return: nothing
    """
    cursor.execute("PRAGMA foreign_keys = 1") # VALIDATE FOREIGN CONSTRAINTS
    emergency_plan = """CREATE TABLE IF NOT EXISTS emergency_plan(
        plan_name          TEXT NOT NULL, 
        plan_type          TEXT,
        plan_description   TEXT,
        geo_area           TEXT,
        start_date         TEXT,
        close_date         TEXT,
        PRIMARY KEY(plan_name)
        )"""
    cursor.execute(emergency_plan)

    camp = """CREATE TABLE IF NOT EXISTS camp(
        plan_name TEXT, 
        camp_name TEXT,
        num_of_refugees INTEGER,
        num_of_volunteers INTEGER,
        PRIMARY KEY(plan_name,camp_name),
        FOREIGN KEY(plan_name) REFERENCES emergency_plan(plan_name)
        )"""
    cursor.execute(camp)

    volunteer = """CREATE TABLE IF NOT EXISTS volunteer(
        plan_name TEXT, 
        camp_name TEXT,
        first_name TEXT,
        last_name TEXT,
        phone_num TEXT,
        activated TEXT,
        username  TEXT,
        password  TEXT,
        PRIMARY KEY(username),
        FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name)
        )"""
    cursor.execute(volunteer)

    refugee_profile = """CREATE TABLE IF NOT EXISTS refugee_profile(
        plan_name           TEXT, 
        camp_name           TEXT,
        first_name           TEXT,
        last_name           TEXT,
        family_num          INTEGER,
        medical_condition   TEXT,
        profile_id          INTEGER,
        PRIMARY KEY(profile_id),
        FOREIGN KEY(plan_name) REFERENCES emergency_plan(plan_name),
        FOREIGN KEY(camp_name) REFERENCES camp(camp_name)
        )"""
    cursor.execute(refugee_profile)

def insert_sql_generation(table_name, *attr):
    """
    used to generate sql commands to insert rows
    :param table_name:
    :param attr: a tuple that stores or the values to pass into the command
    :return: sql cmd
    """
    return f"INSERT INTO {table_name} VAULES({','.join(list(map(str,attr)))})"

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


if __name__ == "__main__":
    connection = sqlite3.connect('db.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    initiate(cursor)

    def test_initiate():
        emergency_plan_list= [
            ("plan1","earthquake","bigone","japan","2022-08-01",""),
            ("plan2","typhoon","smailone","tokyo","2022-08-01",""),
            ("plan3","earthquake","bigone","korea","2022-08-01","")
        ]
        cursor.executemany("INSERT INTO emergency_plan VALUES(?,?,?,?,?,?)", emergency_plan_list)
        connection.commit()
        camp_list = [
            ("plan1", "camp1", 0, 0),
            ("plan2", "camp1", 0, 0),
            ("plan1", "camp2", 0, 0)
        ]
        cursor.executemany("INSERT INTO camp VALUES(?,?,?,?)", camp_list)
        connection.commit()
        volunter_list = [
            ("plan1", "camp1", "lily", "h", "12124124", "True", "a1", "111"),
            ("plan2", "camp1", "tom", "y", "12124124", "True", "a2", "111"),
            ("plan1", "camp2", "eat", "f", "12124124", "True", "a3", "111"),
            ("plan1", "camp1", "sfw", "fas", "12124124", "True", "a4", "111")
        ]
        cursor.executemany("INSERT INTO volunteer VALUES(?,?,?,?,?,?,?,?)", volunter_list)
        connection.commit()

    #test_initiate()
    res = cursor.execute("SELECT * FROM emergency_plan ")
    df = pd.DataFrame(res.fetchall(), columns=['1', '2','3','4','5','6'])
    print(df)
    print()

    res1 = cursor.execute("SELECT * FROM camp ")
    print(res1.fetchall())
    print()
    connection.commit()

    res2 = cursor.execute("SELECT * FROM volunteer")
    print(res2.fetchall())
    print()

    cmd = f"SELECT  *  FROM camp WHERE plan_name = 'plan1' "
    res3 = cursor.execute(cmd)
    df = pd.DataFrame(res3.fetchall(), columns=['1', '2', '3', '4'])
    #print(res3.fetchall())


