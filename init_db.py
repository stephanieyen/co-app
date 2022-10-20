import os
import sys
import psycopg2

'''
Tutorial for Env Variables - 
https://phoenixnap.com/kb/set-environment-variable-mac

Tutorial for PostgreSQL + Flask - 
https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

Run this first in terminal
export DB_URL={Database URL from ElephantSQL}
'''

def create_table_roster(cursor):
    cursor.execute("DROP TABLE IF EXISTS roster")
    cursor.execute("CREATE TABLE roster "
                    + "(user_email TEXT PRIMARY KEY, user_name TEXT, " 
                    + "user_allergies TEXT, user_admin BOOLEAN, "
                    + "user_days TEXT, coop_name TEXT)")

def create_table_shopping(cursor):
    # True for item_type = food, false = equipment
    cursor.execute("DROP TABLE IF EXISTS shoppinglist")
    cursor.execute("CREATE TABLE shoppinglist "
                    + "(item_id SERIAL PRIMARY KEY, item_type BOOLEAN, " 
                    + "item_name TEXT, item_quantity TEXT, "
                    + "item_accepted BOOLEAN, item_reason TEXT, "
                    + "requesting_user TEXT, coop_name TEXT)")
def create_table_shifts(cursor):
    # Shift time is month + date + nearest hour + day
    cursor.execute("DROP TABLE IF EXISTS shifts")
    cursor.execute("CREATE TABLE shifts "
                    + "(shift_id SERIAL PRIMARY KEY, shift_name TEXT, " 
                    + "shift_type TEXT, shift_item TEXT, "
                    + "shift_time TEXT, shift_creator TEXT, "
                    + "shift_members TEXT[], coop_name TEXT)")
def add_test_roster(cursor):
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('amkumar@princeton.edu','Arnav Kumar',"
                    + "'N/A', false, 'M W F', '2D')")
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('sy7@princeton.edu','Stephanie Yen',"
                    + "'N/A', true, 'T W F', '2D')")
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('petrino@princeton.edu','Erin Petrino',"
                    + "'Vegan', false, 'T Th Sat Sun', 'Scully')")
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('sarahep@princeton.edu','Sarah Pedersen',"
                    + "'Peanut Allergy', false, 'M W F Sun', 'Real Food')")
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('thaldiya@princeton.edu','Tanvi Haldiya',"
                    + "'Soy Allergy', false, 'M T Th F', 'IFC')")
    cursor.execute("INSERT INTO roster (user_email, user_name, "
                    + "user_allergies, user_admin, user_days, "
                    + "coop_name) "
                    + "VALUES ('dpw@cs.princeton.edu','David Walker',"
                    + "'N/A', true, 'T W F', 'Brown')")

def add_test_shopping(cursor):
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (true,'Avocadoes',"
                    + "'N/A', true, 'For breakfast', "
                    + "'amkumar@princeton.edu', '2D')")
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (true,'Sriracha',"
                    + "'1', true, 'One large bottle', "
                    + "'sy7@princeton.edu', '2D')")
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (true, 'Coffee syrups',"
                    + "'3', true, 'Lavender, pumpkin spice', "
                    + "'petrino@princeton.edu', 'Scully')")
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (false, 'Nonstick Frying Pan',"
                    + "'1', true, 'Old one broke, other pan too sticky', "
                    + "'sarahep@princeton.edu', 'Real Food')")
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (false, 'Bread Roller',"
                    + "'1', false, 'Want to make pizza one day', "
                    + "'thaldiya@princeton.edu', 'IFC')")
    cursor.execute("INSERT INTO shoppinglist (item_type, item_name, "
                    + "item_quantity, item_accepted, item_reason, "
                    + "requesting_user, coop_name) "
                    + "VALUES (false, 'Computer',"
                    + "'10', false, 'Turn Brown into computer hub', "
                    + "'dpw@cs.princeton.edu', 'Brown')")   
def add_test_shifts(cursor):
    cursor.execute("INSERT INTO shifts (shift_name, shift_type, "
                    + "shift_item, shift_time, shift_creator, "
                    + "shift_members, coop_name) "
                    + "VALUES ('Going to Wegmans','Shopping',"
                    + "'N/A', '10 20 9 Thursday', " 
                    + "'amkumar@princeton.edu', "
                    + "'{amkumar@princeton.edu, sy7@princeton.edu}', '2D')")
    cursor.execute("INSERT INTO shifts (shift_name, shift_type, "
                    + "shift_item, shift_time, shift_creator, "
                    + "shift_members, coop_name) "
                    + "VALUES ('Brunch','Cooking',"
                    + "'French Toast With Berries', '10 23 11 Sunday', " 
                    + "'thaldiya@princeton.edu', "
                    + "'{thaldiya@princeton.edu}', 'IFC')")

# Method to reset database with test users
def main():
    # Setup connection and cursor
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:

            with connection.cursor() as cursor:
                # Create tables
                #------------------------------------------------------
                create_table_roster(cursor)
                create_table_shopping(cursor)
                create_table_shifts(cursor)
                #------------------------------------------------------
                # Add test data to tables
                #------------------------------------------------------
                add_test_roster(cursor)
                add_test_shopping(cursor)
                add_test_shifts(cursor)
                #------------------------------------------------------
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()