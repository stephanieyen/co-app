from typing import List
import sqlalchemy
import sqlalchemy.orm
import models

# How to use env var for this???
db_url = 'postgresql://qqoyksvp:4DE2MIUDdxlcY8L66A5aMLj5ze4zaNbF@peanut.db.elephantsql.com/qqoyksvp'

#----------------------------------------------------------------------
# Co-op info queries
#----------------------------------------------------------------------
# Get the entire roster for a given coop
def get_roster_for_coop(session, coop) -> List[models.Roster]:
    coop_roster = session.query(models.Roster).filter(
        models.Roster.coop_name==coop).all()
    return coop_roster
        

# Get the current shopping list for a co-op
def get_shopping_for_coop(session, coop) -> List[models.ShoppingList]:
    coop_shopping = session.query(models.ShoppingList).filter(
        models.ShoppingList.coop_name==coop).all()
    return coop_shopping
    

# Get the current shifts for a co-op
def get_shifts_for_coop(session, coop) -> List[models.Shifts]:
    coop_shifts = session.query(models.Shifts).filter(
        models.Shifts.coop_name==coop).all()
    return coop_shifts
#----------------------------------------------------------------------
# User queries
#----------------------------------------------------------------------
# Add user to database
def add_user(session, user:models.Roster):
    session.add(user)
    session.commit()
# Get user from email
def get_user(session, email) -> models.Roster:
    # Make sure to only get one user
    user = session.query(models.Roster).filter(
        models.Roster.user_email == email).first()
    return user
# Update a user's information in field to newVal
def update_user(session, email, field, newVal):
    session.query(models.Roster).filter(
        models.Roster.user_email == email).update(
            {field: newVal}
        )
    session.commit()
#----------------------------------------------------------------------
# Shopping List queries
#----------------------------------------------------------------------
# Add item to list
def add_item(session, item: models.ShoppingList):
    session.add(item)
    session.commit()
# Get shopping list item from id
def get_item(session, id) -> models.ShoppingList:
    item = session.query(models.ShoppingList).filter(
        models.ShoppingList.item_id == id).first()
    return item
# Update a item's information
def update_item(session, id, field, newVal):
    session.query(models.ShoppingList).filter(
        models.ShoppingList.item_id == id).update(
            {field: newVal}
        )
    session.commit()
#----------------------------------------------------------------------
# Shift queries
#----------------------------------------------------------------------
# Add shift to calendar
def add_shift(session, shift: models.Shifts):
    session.add(shift)
    session.commit()
# Get shift from id
def get_shift(session, id) -> models.Shifts:
    shift = session.query(models.Shifts).filter(
        models.Shifts.shift_id == id).first()
    return shift
# Update a shift's information
def update_shift(session, id, field, newVal):
    session.query(models.Shifts).filter(
        models.Shifts.shift_id == id).update(
            {field: newVal}
        )
    session.commit()
#----------------------------------------------------------------------

# Unit testing for these
def main():
    # Create engine and drop and recreate all tables
    engine = sqlalchemy.create_engine(db_url)

    with sqlalchemy.orm.Session(engine) as session:
        users = get_roster_for_coop(session, '2D')
        list = get_shopping_for_coop(session, 'Brown')
        shifts = get_shifts_for_coop(session, 'IFC')
        # Test user functions
        user_1 = users[0]
        user_1_email = users[0].user_email
        update_user(session, user_1.user_email, 'user_allergies', 'Nut allergy')

        print(get_user(session, user_1_email).user_allergies)
        new_user = models.Roster(user_email='rdondero@cs.princeton.edu',
                        user_name='Bob Dondero',
                        user_allergies='JavaScript',
                        user_admin=True,
                        user_days='M T W Th F Sat Sun',
                        coop_name='Brown')
        add_user(session, new_user)
        # Test shopping list functions
        list_1 = list[0]
        update_item(session, list_1.item_id, 'item_accepted', False)
        print(get_item(session, list_1.item_id).item_accepted)
        new_item = models.ShoppingList(item_type=False,
                            item_name="Chairs",
                            item_quantity='100',
                            item_accepted=False,
                            item_reason='Guest seating',
                            requesting_user='rdondero@cs.princeton.edu',
                            food_type="Item",
                            alt_request="N/A",
                            coop_name='Brown')
        add_item(session, new_item)
        # Test shift functions
        shift_1 = shifts[0]
        update_shift(session, shift_1.shift_id, 'shift_time', '10 21 9 Friday')
        print(get_shift(session, shift_1.shift_id).shift_time)
        new_shift = models.Shifts(shift_name='Cooking Some Computers',
                        shift_type='Cooking',
                        shift_item='Macbooks',
                        shift_time='2022-10-31T16:00:00',
                        shift_day='Monday',
                        shift_creator='dpw@cs.princeton.edu',
                        shift_members=['dpw@cs.princeton.edu', 'rdondero@cs.princeton.edu'],
                        coop_name='Brown')
        add_shift(session, new_shift)
    engine.dispose()
if __name__ == '__main__':
    main()