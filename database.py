import os
import sys
import psycopg2

'''
Run this first in terminal
export DB_URL={Database URL from ElephantSQL}
'''

# Get the coop given the user's email
def get_coop_for_user(email):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    SELECT coop_name FROM roster WHERE user_email=%s
                ''', (email,)) 
                # Execute statement
                row = cursor.fetchone()
                if row is None:
                    return "This user is not currently in a co-op!"
                return row[0]

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Get the entire roster for a given coop
def get_roster_for_coop(coop):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    SELECT * FROM roster WHERE coop_name=%s
                ''', (coop,)) 
                # Execute statement
                row = cursor.fetchall()
                if row == []:
                    return "This is not a supported co-op!"
                return row

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Get the current shopping list for a co-op
def get_shopping_for_coop(coop):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    SELECT * FROM shoppinglist WHERE coop_name=%s
                ''', (coop,)) 
                # Execute statement
                row = cursor.fetchall()
                if row == []:
                    return "This co-op has no shopping list yet!"
                return row

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Get the current shifts for a co-op
def get_shifts_for_coop(coop):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    SELECT * FROM shifts WHERE coop_name=%s 
                    ORDER BY shift_time
                ''', (coop,)) 
                # Execute statement
                row = cursor.fetchall()
                if row == []:
                    return "This co-op has no shifts!"
                return row

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Unit testing for these
def main():
    # Testing get_coop_for_user
    #------------------------------------------------------------------
    print(get_coop_for_user('amkumar@princeton.edu'))
    print(get_coop_for_user('a@princeton.edu'))
    print(get_coop_for_user("amkumar@princeton.edu' OR 'x'='x"))
    print(get_coop_for_user('sarahep@princeton.edu'))
    #------------------------------------------------------------------
    # Testing get_roster_for_coop
    print(get_roster_for_coop('2D'))
    print(get_roster_for_coop('Real Food'))
    print(get_roster_for_coop("amkumar@princeton.edu' OR 'x'='x"))
    print(get_roster_for_coop('IFC'))
    print(get_roster_for_coop('Brown'))
    print(get_roster_for_coop('Scully'))
    #------------------------------------------------------------------
    # Testing get_shopping_for_coop
    print(get_shopping_for_coop('2D'))
    print(get_shopping_for_coop('Real Food'))
    print(get_shopping_for_coop("amkumar@princeton.edu' OR 'x'='x"))
    print(get_shopping_for_coop('IFC'))
    print(get_shopping_for_coop('Brown'))
    print(get_shopping_for_coop('Scully'))
    #------------------------------------------------------------------
    # Testing get_shifts_for_coop
    print(get_shifts_for_coop('2D'))
    print(get_shifts_for_coop('Real Food'))
    print(get_shifts_for_coop("amkumar@princeton.edu' OR 'x'='x"))
    print(get_shifts_for_coop('IFC'))
    print(get_shifts_for_coop('Brown'))
    print(get_shifts_for_coop('Scully'))
    #------------------------------------------------------------------

if __name__ == '__main__':
    main()