import sqlite3
from logging_configure import log_general
"""
    Assumptions:
        one volunteer can only service one camp at a time.
        one volunteer can only belong to one emergency plan     .
        one camp can only belong to one emergency plan.
        one plan can have multiple camps
        one camp can have multiple volunteers
        
"""

def initiate(connection,cursor):
    """
    used to initiate the database to create tables and triggers.
    param cursor: pass a cursor to execute sql commands
    :return: nothing
    """
    # Note the data type DATE denotes the format of "YYYY-MM-YDD" in a string form
    cursor.execute("PRAGMA foreign_keys = 1") # VALIDATE FOREIGN CONSTRAINTS
    try:
        emergency_plan = """CREATE TABLE IF NOT EXISTS emergency_plan(
                plan_name          TEXT, 
                plan_type          TEXT,
                plan_description   TEXT,
                geo_area           TEXT,
                start_date         DATE DEFAULT (date('now','localtime')),
                close_date         DATE DEFAULT null,
                PRIMARY KEY(plan_name)
                )"""
        cursor.execute(emergency_plan)

        camp = """CREATE TABLE IF NOT EXISTS camp(
                plan_name TEXT, 
                camp_name TEXT,
                num_of_volunteers INTEGER DEFAULT 0, 
                num_of_refugees INTEGER DEFAULT 0,
                archived  TEXT DEFAULT 'FALSE',
                PRIMARY KEY(plan_name,camp_name),
                FOREIGN KEY(plan_name) REFERENCES emergency_plan(plan_name) ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        cursor.execute(camp)

        # availability is designed to have a selection list instead of user defined strings
        # reassignable by default is set to be False
        # activated by default is set to be True
        volunteer = """CREATE TABLE IF NOT EXISTS volunteer(
                plan_name TEXT, 
                camp_name TEXT,
                first_name TEXT,
                last_name TEXT,
                phone_num TEXT,
                availability TEXT,   
                username  TEXT,
                password  TEXT,
                activated TEXT DEFAULT 'TRUE',
                reassignable TEXT DEFAULT 'FALSE',
                PRIMARY KEY(username),
                FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name) ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        cursor.execute(volunteer)
        # initialize admin
        cursor.execute("INSERT INTO volunteer VALUES(null,null,null,null,null,null,'admin','111',null,null)")
        cursor.execute("INSERT INTO volunteer VALUES(null,null,null,null,null,null,'guest','111',null,null)")
        connection.commit()

        refugee_profile = """CREATE TABLE IF NOT EXISTS refugee_profile(
                profile_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_name           TEXT, 
                camp_name           TEXT,
                first_name          TEXT,
                last_name           TEXT,
                family_num          INTEGER,
                medical_condition   TEXT,
                archived  TEXT DEFAULT 'FALSE',
                FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name) ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        cursor.execute(refugee_profile)

        # set the increment starting from 10000 for profile_id of refugee_profile .
        cursor.execute("INSERT INTO refugee_profile VALUES(null,null,null,null,null,null,null,null) ")
        cursor.execute("UPDATE sqlite_sequence SET seq = 9999 WHERE NAME = 'refugee_profile'")
        cursor.execute("DELETE FROM refugee_profile WHERE profile_id=1")
        connection.commit()

        # admin_exclusive ['TRUE','FALSE']. True means the msg only visible to admins
        # admin_announced ['TRUE','FALSE']. True means the msg is posted by admin as public msgs to visible by all volunteers.
        # By combining the two attributes, the proposed features [1. plan/camp channel communications,
        # 2. admin public announcements 3. send a msg as a 'guest'] are implemented.
        message = """CREATE TABLE IF NOT EXISTS message(
                message_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                time                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                plan_name           TEXT, 
                camp_name           TEXT,
                username            TEXT,
                admin_announced     TEXT,
                admin_exclusive     TEXT,
                content             TEXT,
                FOREIGN KEY(username) REFERENCES volunteer(username) ON UPDATE CASCADE ON DELETE NO ACTION,
                FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name) ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        cursor.execute(message)

        # create trigger for updating camp volunteer number, insertion prevention has already been implemented in other way
        camp_add_volnum_trigger = """CREATE TRIGGER camp_add_volnum_trigger BEFORE INSERT ON volunteer
                WHEN EXISTS(
                    SELECT * FROM camp
                    WHERE camp_name = new.camp_name and archived = 'FALSE'
                )
                BEGIN
                    UPDATE camp SET num_of_volunteers = num_of_volunteers+1  WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_add_volnum_trigger)

        # create trigger for updating camp volunteer number at a deletion
        camp_del_volnum_trigger = """CREATE TRIGGER camp_del_volnum_trigger AFTER DELETE ON volunteer
                WHEN EXISTS(
                    SELECT * FROM camp
                    WHERE camp_name = old.camp_name and archived = 'FALSE'
                )
                BEGIN
                    UPDATE camp SET num_of_volunteers = num_of_volunteers-1  WHERE plan_name= old.plan_name and camp_name = old.camp_name;
                END
                ;
                """
        cursor.execute(camp_del_volnum_trigger)

        # create a trigger to update the num of volunteers and the camps
        camp_update_volnum_trigger = """CREATE TRIGGER camp_update_volnum_trigger BEFORE UPDATE OF camp_name ON volunteer
                WHEN EXISTS(
                    SELECT * FROM camp
                    WHERE camp_name = old.camp_name and archived = 'FALSE' and plan_name= old.plan_name
                )
                BEGIN
                    UPDATE camp SET num_of_volunteers = num_of_volunteers - 1 WHERE plan_name= old.plan_name and camp_name = old.camp_name;
                    UPDATE camp SET num_of_volunteers = num_of_volunteers + 1 WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_update_volnum_trigger)

        # create a trigger to update the num of volunteers and the campes
        archived_camp_update_volnum_trigger = """CREATE TRIGGER archived_camp_update_volnum_trigger BEFORE UPDATE OF plan_name ON volunteer
                WHEN EXISTS(
                    SELECT * FROM camp
                    WHERE camp_name = old.camp_name and archived = 'TRUE' and plan_name= old.plan_name
                )
                BEGIN
                    UPDATE camp SET num_of_volunteers = num_of_volunteers + 1 WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                    UPDATE volunteer SET reassignable = 'FALSE', plan_name= new.plan_name, camp_name = new.camp_name WHERE username=new.username;
                END
                ;
                """
        cursor.execute(archived_camp_update_volnum_trigger)

        # create archived trigger to prevent updates in refugee_profile
        archived_prevent_camp_update_trigger = """CREATE TRIGGER archived_prevent_camp_update_trigger Before UPDATE ON camp
                WHEN old.archived = 'TRUE'
                BEGIN
                     SELECT RAISE(ABORT, '* The camp registered in a closed plan so that it can not be edited');
                END
                ;
                """

        cursor.execute(archived_prevent_camp_update_trigger)


        # create a trigger to prevent deleting admin
        prevent_admin_deletion_trigger = """CREATE TRIGGER prevent_admin_deletion_trigger BEFORE DELETE ON volunteer
                WHEN EXISTS(
                    SELECT * FROM volunteer
                    WHERE old.username = 'admin'
                )
                BEGIN
                    SELECT RAISE(ABORT,'* Admin can not be deleted');
                END
                ;
                """
        cursor.execute(prevent_admin_deletion_trigger)

        # prevent closed plans from being modified.
        prevent_update_closed_plan_trigger = """CREATE TRIGGER prevent_update_closed_plan_trigger BEFORE update ON emergency_plan
                WHEN EXISTS(
                    SELECT * FROM emergency_plan
                    WHERE old.close_date IS NOT NULL
                )
                BEGIN
                    SELECT RAISE(ABORT,'* Closed plans can not be edited');
                END
                ;
                """
        cursor.execute(prevent_update_closed_plan_trigger)

        # create trigger for updating camp refugee numbers.
        camp_add_refnum_trigger = """CREATE TRIGGER camp_add_refnum_trigger BEFORE INSERT ON refugee_profile
                WHEN new.archived = 'FALSE'
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees + new.family_num WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_add_refnum_trigger)

        camp_del_refnum_trigger = """CREATE TRIGGER camp_del_refnum_trigger BEFORE DELETE ON refugee_profile
                WHEN old.archived = 'FALSE'
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees- old.family_num WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_del_refnum_trigger)

        camp_update_refnum_trigger = """CREATE TRIGGER camp_update_refnum_trigger BEFORE UPDATE OF family_num ON refugee_profile
                WHEN old.archived = 'FALSE'
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees + (new.family_num - old.family_num) WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_update_refnum_trigger)

        # create a trigger to update num of refugees
        update_refnum_camp_trigger = """CREATE TRIGGER camp_update_refnum_camp_trigger BEFORE UPDATE OF camp_name ON refugee_profile
                WHEN old.archived = 'FALSE'
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees - old.family_num WHERE plan_name= old.plan_name and camp_name = old.camp_name;
                    UPDATE camp SET num_of_refugees = num_of_refugees + new.family_num  WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(update_refnum_camp_trigger)

        # create archived trigger to prevent updates in refugee_profile
        archived_prevent_ref_update_trigger = """CREATE TRIGGER archived_prevent_ref_update_trigger Before UPDATE ON refugee_profile
                WHEN old.archived = 'TRUE'
                BEGIN
                     SELECT RAISE(ABORT, '* The refugee file registered in a closed plan so that it can not be edited');
                END
                ;
                """
        cursor.execute(archived_prevent_ref_update_trigger)

        # create trigger for closed plans to free volunteers for reassignment
        close_plan_update_volunteer = """CREATE TRIGGER close_plan_update_volunteer AFTER UPDATE OF close_date ON emergency_plan
                WHEN new.close_date IS NOT NULL
                BEGIN
                    UPDATE volunteer SET reassignable = 'TRUE' WHERE plan_name= old.plan_name;
                    UPDATE refugee_profile SET archived = 'TRUE' WHERE plan_name= old.plan_name;
                    UPDATE camp SET archived = 'TRUE' WHERE plan_name= old.plan_name;
                END
                ;
                """
        cursor.execute(close_plan_update_volunteer)

    except sqlite3.IntegrityError as e:
        log_general.info("* Tables have been initialized. Please don‘t do it twice")
    except sqlite3.Error as e:
        log_general.info('SQLite error: %s' % (' '.join(e.args)))
    else:
        log_general.info("* DataBase Initialization Succeeded")



def test_initiate(connection,cursor):
    """
    used just for testing
    :param cursor:
    :return:
    """

    try:
        emergency_plan_list = [
            ("plan1", "earthquake", "bigone", "japan"),
            ("plan2", "typhoon", "smailone", "tokyo"),
            ("plan3", "earthquake", "bigone", "korea")
        ]
        cursor.executemany("INSERT INTO emergency_plan(plan_name,plan_type,plan_description,geo_area) VALUES(?,?,?,?)", emergency_plan_list)
        connection.commit()
        camp_list = [
            ("plan1", "camp1"),
            ("plan2", "camp1"),
            ("plan1", "camp2"),
            ("plan2", "camp2"),
        ]
        cursor.executemany("INSERT INTO camp VALUES(?,?,0,0,'FALSE')", camp_list)
        connection.commit()
        volunter_list = [
            ("plan1", "camp1", "lily", "h", "12124124", "Monday", "vol1", "111", "TRUE", "FALSE"),
            ("plan2", "camp1", "tom", "y", "12124124", "Tuesday", "vol2", "111", "TRUE", "FALSE"),
            ("plan1", "camp2", "eat", "f", "12124124", "Thursday", "vol3", "111", "TRUE", "FALSE"),
            ("plan1", "camp1", "sfw", "fas", "12124124", "Friday", "vol4", "111", "TRUE", "FALSE")
        ]
        cursor.executemany("INSERT INTO volunteer VALUES(?,?,?,?,?,?,?,?,?,?)", volunter_list)
        connection.commit()
        refugee_profile_list = [
            ("plan1", "camp1", "lily", "h", 5, "cold"),
            ("plan2", "camp1", "tom", "y", 4, "cold"),
            ("plan1", "camp2", "eat", "f", 3, "cold"),
            ("plan1", "camp1", "sfw", "fas", 2, "cold")

        ]
        cursor.executemany(
            "INSERT INTO refugee_profile(plan_name,camp_name,first_name,last_name,family_num,medical_condition) VALUES(?,?,?,?,?,?)",
            refugee_profile_list)
        connection.commit()
        message_list = [
            (None, None, "guest", "FALSE","TRUE", "I FORGET MY PASSWORD, MY ACCOUNT NAME IS 'HEY'."),
            (None, None, "admin", "TRUE","FALSE","WELCOME TO THIS PROGRAM, VOLUNTEERS"),
            ("plan1", "camp2", "vol3", "FALSE", "TRUE","[COULD YOU HELP ME REMOVE TO ANOTHER PLAN, admin]"),
            ("plan1", "camp2", "vol3", "FALSE", "FALSE","[nice to see you guys]"),
        ]
        cursor.executemany(
            "INSERT INTO message(plan_name,camp_name,username,admin_announced,admin_exclusive,content) VALUES(?,?,?,?,?,?)",
            message_list)
        connection.commit()

    except sqlite3.IntegrityError as e:
        log_general.info("* Test tables have been initialized. Please don‘t do it twice")
    except sqlite3.Error as e:
        log_general.info('SQLite error: %s' % (' '.join(e.args)))
    else:
        log_general.info("* Test Insertions Have Been Initialized successfully")

