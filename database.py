import os
import sys
from typing import List
import psycopg2

from shift import Shift
from shoppingitem import ShoppingItem
from user import User

'''
Run this first in terminal
export DB_URL={Database URL from ElephantSQL}
'''
#----------------------------------------------------------------------
# Co-op info queries
#----------------------------------------------------------------------
# Get the entire roster for a given coop
def get_roster_for_coop(coop: str) -> List[User]:
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
                row = cursor.fetchone()
                users = []
                while row is not None:
                    user = User(row[0], row[1], row[2], row[3],
                            row[4], row[5])
                    users.append(user)
                    row = cursor.fetchone()
        return users
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Get the current shopping list for a co-op
def get_shopping_for_coop(coop: str) -> List[ShoppingItem]:
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
                row = cursor.fetchone()
                items = []
                while row is not None:
                    item = ShoppingItem(row[0], row[1], row[2], row[3],
                            row[4], row[5], row[6], row[7])
                    items.append(item)
                    row = cursor.fetchone()
        return items
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# Get the current shifts for a co-op
def get_shifts_for_coop(coop:str) -> List[Shift]:
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
                ''', (coop, )) 
                # Execute statement
                row = cursor.fetchone()
                shifts = []
                while row is not None:
                    shift = Shift(row[0], row[1], row[2], row[3], row[4],
                            row[5], row[6], row[7])
                    shifts.append(shift)
                    row = cursor.fetchone()
        return shifts
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#----------------------------------------------------------------------
# User queries
#----------------------------------------------------------------------
def add_user(user:User):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    INSERT INTO roster (user_email, user_name, 
                    user_allergies, user_admin, user_days, coop_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (user.get_email(), user.get_name(), 
                    user.get_allergies(), user.get_admin(), 
                    user.get_days(), user.get_coop())) 
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
# Get user from email
def get_user(email:str) -> User:
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    SELECT * FROM roster WHERE user_email=%s
                ''', (email, )) 
                # Execute statement
                row = cursor.fetchone()
                user = User(row[0], row[1], row[2], row[3],
                            row[4], row[5])
                return user
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
# Update a user's information (if updating profile, setting admin)
def update_user(user: User):
    try:
        # Get 
        db_url = os.getenv('DB_URL')
        # Connect to database
        with psycopg2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                # Get coop_name of user by user email
                cursor.execute('''
                    UPDATE roster 
                    SET user_name=%s,
                        user_allergies=%s,
                        user_admin=%s,
                        user_days=%s,
                        coop_name=%s
                    WHERE user_email=%s 
                ''', (user.get_name(), user.get_allergies(), 
                    user.get_admin(), user.get_days(), user.get_coop(),
                    user.get_email())) 
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
#----------------------------------------------------------------------

# Unit testing for these
def main():
    # Get 2D roster
    user_2D = get_roster_for_coop('2D')
    print(user_2D[0])
    email = user_2D[0].get_email()
    # Change allergies (bad syntax but wouldn't be done in actual site)
    user_2D[0]._allergies = "Hates Potatoes"
    update_user(user_2D[0])

    # See if update worked and test get_user
    user_2D_update = get_user(email)
    print(user_2D_update)

    # Get shifts for 2D
    shifts_2D = get_shifts_for_coop('2D')
    print(shifts_2D[0])

    # Get shopping list for Brown
    shopping_brown = get_shopping_for_coop('Brown')
    print(shopping_brown[0])

    # Add user
    new_user = User('watsonjia@princeton.edu', "Watson Jia", 'N/A', 
                False, 'M T W Th F', 'Brown')
    add_user(new_user)
    print(get_user('watsonjia@princeton.edu'))
if __name__ == '__main__':
    main()