import sqlite3
"""
    Assumptions:
        one volunteer can only service one camp at a time.
        one camp can only belong to one emergency plan.
"""

def initiate(connection,cursor):
    """
    used to initiate the database to create tables and triggers.
    :param cursor: pass a cursor to execute sql commands
    :return: nothing
    """
    cursor.execute("PRAGMA foreign_keys = 1") # VALIDATE FOREIGN CONSTRAINTS
    try:
        emergency_plan = """CREATE TABLE IF NOT EXISTS emergency_plan(
                plan_name          TEXT, 
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
                num_of_volunteers INTEGER DEFAULT 0, 
                num_of_refugees INTEGER DEFAULT 0,
                PRIMARY KEY(plan_name,camp_name),
                FOREIGN KEY(plan_name) REFERENCES emergency_plan(plan_name) ON UPDATE CASCADE
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
                activated TEXT,
                reassignable TEXT,
                PRIMARY KEY(username),
                FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name) ON UPDATE CASCADE
                )"""
        cursor.execute(volunteer)

        # initialize admin
        cursor.execute("INSERT INTO volunteer VALUES(null,null,null,null,null,null,'admin','111',null,null)")
        connection.commit()

        refugee_profile = """CREATE TABLE IF NOT EXISTS refugee_profile(
                profile_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_name           TEXT, 
                camp_name           TEXT,
                first_name          TEXT,
                last_name           TEXT,
                family_num          INTEGER,
                medical_condition   TEXT,
                FOREIGN KEY(plan_name,camp_name) REFERENCES camp(plan_name,camp_name) ON UPDATE CASCADE
                )"""
        cursor.execute(refugee_profile)

        # set the increment starting from 10000 for profile_id of refugee_profile .
        cursor.execute("INSERT INTO refugee_profile VALUES(null,null,null,null,null,null,null) ")
        cursor.execute("UPDATE sqlite_sequence SET seq = 9999 WHERE NAME = 'refugee_profile'")
        cursor.execute("DELETE FROM refugee_profile WHERE profile_id=1")

        # create trigger for updating camp volunteer numbers.
        camp_add_volnum_trigger = """CREATE TRIGGER camp_add_volnum_trigger AFTER INSERT ON volunteer
                BEGIN
                    UPDATE camp SET num_of_volunteers = num_of_volunteers+1  WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_add_volnum_trigger)

        camp_del_volnum_trigger = """CREATE TRIGGER camp_del_volnum_trigger AFTER DELETE ON volunteer
                    BEGIN
                        UPDATE camp SET num_of_volunteers = num_of_volunteers-1  WHERE plan_name= old.plan_name and camp_name = old.camp_name;
                    END
                    ;
                    """
        cursor.execute(camp_del_volnum_trigger)

        # create a trigger to prevent deleting admin
        prevent_admin_deletion_trigger = """CREATE TRIGGER prevent_admin_deletion_trigger BEFORE DELETE ON volunteer
                WHEN EXISTS(
                    SELECT * FROM volunteer
                    WHERE old.username = 'admin'
                )
                BEGIN
                    SELECT RAISE(ABORT,'Admin can not be deleted');
                END
                ;
                """
        cursor.execute(prevent_admin_deletion_trigger)

        # create trigger for updating camp refugee numbers.
        camp_add_refnum_trigger = """CREATE TRIGGER camp_add_refnum_trigger AFTER INSERT ON refugee_profile
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees + new.family_num WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_add_refnum_trigger)

        camp_del_refnum_trigger = """CREATE TRIGGER camp_del_refnum_trigger AFTER DELETE ON refugee_profile
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees- old.family_num WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_del_refnum_trigger)

        camp_update_refnum_trigger = """CREATE TRIGGER camp_update_refnum_trigger AFTER UPDATE OF family_num ON refugee_profile
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees + (new.family_num - old.family_num) WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_update_refnum_trigger)

        camp_update_refnum_camp_trigger = """CREATE TRIGGER camp_update_refnum_camp_trigger AFTER UPDATE OF camp_name ON refugee_profile
                BEGIN
                    UPDATE camp SET num_of_refugees = num_of_refugees - old.family_num WHERE plan_name= old.plan_name and camp_name = old.camp_name;
                    UPDATE camp SET num_of_refugees = num_of_refugees + new.family_num  WHERE plan_name= new.plan_name and camp_name = new.camp_name;
                END
                ;
                """
        cursor.execute(camp_update_refnum_camp_trigger)

        # create trigger for closed plans to free volunteers for reassignment
        close_plan_update_volunteer = """CREATE TRIGGER close_plan_update_volunteer AFTER UPDATE OF close_date ON emergency_plan
                WHEN new.close_date != 'NULL'
                BEGIN
                    UPDATE volunteer SET reassignable = 'True' WHERE plan_name= new.plan_name;
                END
                ;
                """
        cursor.execute(close_plan_update_volunteer)

    except sqlite3.IntegrityError as e:
        print("* Tables Have Been Initialized. Please Dont Do It Twice")
    except sqlite3.Error as e:
        print('SQLite error: %s' % (' '.join(e.args)))
    else:
        print("* DataBase Initialization Succeeded")



def test_initiate(connection,cursor):
    """
    used just for testing
    :param cursor:
    :return:
    """
    try:
        emergency_plan_list = [
            ("plan1", "earthquake", "bigone", "japan", "2022-08-01", "NULL"),
            ("plan2", "typhoon", "smailone", "tokyo", "2022-08-01", "NULL"),
            ("plan3", "earthquake", "bigone", "korea", "2022-08-01", "NULL")
        ]
        cursor.executemany("INSERT INTO emergency_plan VALUES(?,?,?,?,?,?)", emergency_plan_list)
        connection.commit()
        camp_list = [
            ("plan1", "camp1"),
            ("plan2", "camp1"),
            ("plan1", "camp2")
        ]
        cursor.executemany("INSERT INTO camp VALUES(?,?,0,0)", camp_list)
        connection.commit()
        volunter_list = [
            ("plan1", "camp1", "lily", "h", "12124124", "Monday to Friday", "vol1", "111", "True", "False"),
            ("plan2", "camp1", "tom", "y", "12124124", "Monday to Friday", "vol2", "111", "True", "False"),
            ("plan1", "camp2", "eat", "f", "12124124", "Monday to Friday", "vol3", "111", "True", "False"),
            ("plan1", "camp1", "sfw", "fas", "12124124", "Monday to Friday", "vol4", "111", "True", "False")
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

    except sqlite3.IntegrityError as e:
        print("* Test Tables Have Been Initialized. Please Dont Do It Twice")
    except sqlite3.Error as e:
        print('SQLite error: %s' % (' '.join(e.args)))
    else:
        print("* Test Insertions Have Been Initialized successfully")

