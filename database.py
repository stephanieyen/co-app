from typing import List
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import SQLAlchemyError
import models
import helper
from datetime import datetime, timedelta
import os

# How to use env var for this???
db_url = os.getenv("DATABASE_URL")
# db_url = 'postgresql://qqoyksvp:4DE2MIUDdxlcY8L66A5aMLj5ze4zaNbF@peanut.db.elephantsql.com/qqoyksvp'
# Global engine to use
engine =  sqlalchemy.create_engine(db_url, pool_pre_ping=True)
#----------------------------------------------------------------------
# Co-op Info Queries
#----------------------------------------------------------------------
def get_upper_coop(coop):
    ''' returns the correctly-cased string of the input co-op name'''
    return helper.get_coop_names()[coop]

# Get the entire roster for a given coop
def get_roster_for_coop(coop) -> List[models.Roster]:
    '''
        Get and return the entire roster of the input co-op, 
        sorted by name.
    '''
    coop_roster = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_roster = session.query(models.Roster).filter(
            models.Roster.coop_name==coop).order_by(
                models.Roster.user_name
            ).all()
    return coop_roster

# Get the entire roster for a given coop
def get_names_for_coop(coop):
    '''
        Get and return the entire roster of the input co-op
        mapping names to netid
    '''
    coop_roster = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_roster = session.query(models.Roster).filter(
            models.Roster.coop_name==coop).order_by(
                models.Roster.user_name.desc()
            ).all()
        members = {}
        for member in coop_roster:
            members[member.user_name] = member.user_netid
    return members

# Get the current shopping list for a co-op
def get_shopping_for_coop(coop) -> List[models.ShoppingList]:
    coop_shopping = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop).all()
    return coop_shopping

def get_food_list_for_coop(coop) -> List[models.ShoppingList]:
    coop_shopping = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop,
            models.ShoppingList.item_type=="Food").order_by(
                models.ShoppingList.food_type.desc(),
                models.ShoppingList.item_name
            ).all()
    return coop_shopping

def get_equipment_list_for_coop(coop) -> List[models.ShoppingList]:
    coop_shopping = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop,
            models.ShoppingList.item_type=="Equipment").order_by(
                models.ShoppingList.item_name
            ).all()
    return coop_shopping

# Get the current shopping list for a co-op within 7 days of the passed in date
def get_shopping_for_week(coop, startDate, endDate) -> List[models.ShoppingList]:
    coop_shopping = []
    # startDate = datetime(year, month, day)
    # startOfWeek = startDate.strftime('%Y-%m-%d')
    # endOfWeek = (startDate + timedelta(7)).strftime('%Y-%m-%d')
    startOfWeek = str(startDate)
    endOfWeek = str(endDate)
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop,
            models.ShoppingList.date_added >= startOfWeek,
            models.ShoppingList.date_added <= endOfWeek
        ).order_by(
            models.ShoppingList.for_shift.desc(),
            models.ShoppingList.food_type.desc(),
            models.ShoppingList.item_name
        ).all()
    return coop_shopping

def get_food_list_for_week(coop, startDate, endDate) -> List[models.ShoppingList]:
    coop_shopping = []
    # startDate = datetime(year, month, day)
    # startOfWeek = startDate.strftime('%Y-%m-%d')
    # endOfWeek = (startDate + timedelta(7)).strftime('%Y-%m-%d')
    startOfWeek = str(startDate)
    endOfWeek = str(endDate)
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop,
            models.ShoppingList.item_type=="Food",
            models.ShoppingList.date_added >= startOfWeek,
            models.ShoppingList.date_added <= endOfWeek
        ).order_by(
            models.ShoppingList.for_shift.desc(),
            models.ShoppingList.food_type.desc(),
            models.ShoppingList.item_name
        ).all()
    return coop_shopping

def get_equipment_list_for_week(coop, startDate, endDate) -> List[models.ShoppingList]:
    coop_shopping = []
    # startDate = datetime(year, month, day)
    # startOfWeek = startDate.strftime('%Y-%m-%d')
    # endOfWeek = (startDate + timedelta(7)).strftime('%Y-%m-%d')
    startOfWeek = str(startDate)
    endOfWeek = str(endDate)
    with sqlalchemy.orm.Session(engine) as session:
        coop_shopping = session.query(models.ShoppingList).filter(
            models.ShoppingList.coop_name==coop,
            models.ShoppingList.item_type=="Equipment",
            models.ShoppingList.date_added >= startOfWeek,
            models.ShoppingList.date_added <= endOfWeek
        ).order_by(
            models.ShoppingList.for_shift.desc(),
            models.ShoppingList.item_name
        ).all()
    return coop_shopping

# Get the current shifts for a co-op
def get_shifts_for_coop(coop) -> List[models.Shifts]:
    coop_shifts = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_shifts = session.query(models.Shifts).filter(
            models.Shifts.coop_name==coop).all()
    return coop_shifts

# Get the current shifts for a co-op for a given week
def get_shifts_for_week(coop, startDate, endDate) -> List[models.Shifts]:
    coop_shifts = []
    # startDate = datetime(year, month, day)
    # startOfWeek = startDate.strftime('%Y-%m-%d')
    # endOfWeek = (startDate + timedelta(7)).strftime('%Y-%m-%d')
    startOfWeek = str(startDate)
    endOfWeek = str(endDate)
    with sqlalchemy.orm.Session(engine) as session:
        coop_shifts = session.query(models.Shifts).filter(
            sqlalchemy.or_(
                sqlalchemy.and_(
                    models.Shifts.coop_name==coop,
                    models.Shifts.shift_time >= startOfWeek,
                    models.Shifts.shift_time <= endOfWeek
                ),
                sqlalchemy.and_(
                    models.Shifts.shift_recurring,
                    models.Shifts.coop_name==coop,
                )
            )
        ).all()
    return coop_shifts

# Get the recipes for a co-op
def get_recipes_for_coop(coop, recipe_type) -> List[models.Recipes]:
    coop_recipes = []
    with sqlalchemy.orm.Session(engine) as session:
        coop_recipes = session.query(models.Recipes).filter(
            models.Recipes.coop_name==coop,
            models.Recipes.recipe_type.like(recipe_type)).order_by(
                models.Recipes.recipe_name
        ).all()
    return coop_recipes

#----------------------------------------------------------------------
# User queries
#----------------------------------------------------------------------
# Add user to database
def add_user(user:models.Roster):
    try:
        with sqlalchemy.orm.Session(engine) as session:
            session.add(user)
            session.commit()
        return True, ""
    except SQLAlchemyError as e:
        error = str(e.orig)
        return False, error
# Get user from netid
def get_user(netid) -> models.Roster:
    # Make sure to only get one user
    user = None
    with sqlalchemy.orm.Session(engine) as session:
        user = session.query(models.Roster).filter(
            models.Roster.user_netid == netid).first()
    return user

# Get shifts of user
def get_user_shifts(netid) -> List[models.Shifts]:
    today = str(datetime.now().strftime('%Y-%m-%d'))
    with sqlalchemy.orm.Session(engine) as session:
        shifts = session.query(models.Shifts).filter(
            sqlalchemy.or_(
                models.Shifts.shift_members.contains([netid]),
                models.Shifts.shift_creator == netid
            ),
            sqlalchemy.or_(
                models.Shifts.shift_time >= today,
                models.Shifts.shift_recurring
            )
        ).all()
    return shifts

# Update a user's information
def update_user(netid, new_user: models.Roster):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Roster).filter(
            models.Roster.user_netid == netid).update(
                {
                    'user_netid': new_user.user_netid,
                    'user_name': new_user.user_name,
                    'user_allergies': new_user.user_allergies,
                    'user_admin': new_user.user_admin,
                    'user_cookday': new_user.user_cookday,
                    'user_choreday': new_user.user_choreday,
                    'notify_email': new_user.notify_email,
                    'coop_name': new_user.coop_name,
                }
            )
        session.commit()
# Delete a user's information
def delete_user(netid):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Roster).filter(
            models.Roster.user_netid == netid).delete()
        session.commit()
#----------------------------------------------------------------------
# Shopping List queries
#----------------------------------------------------------------------
# Add item to list
def add_item(item: models.ShoppingList):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(item)
        session.commit()
# Get shopping list item from id
def get_item(id) -> models.ShoppingList:
    item = None
    with sqlalchemy.orm.Session(engine) as session:
        item = session.query(models.ShoppingList).filter(
            models.ShoppingList.item_id == id).first()
    return item
# Update a item's information
def update_item(id, new_item: models.ShoppingList):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.ShoppingList).filter(
            models.ShoppingList.item_id == id).update(
                {
                    'item_type': new_item.item_type,
                    'item_name': new_item.item_name,
                    'item_quantity': new_item.item_quantity,
                    'item_ordered': new_item.item_ordered,
                    'for_shift': new_item.for_shift,
                    'item_reason': new_item.item_reason,
                    'requesting_user': new_item.requesting_user,
                    'food_type': new_item.food_type,
                    'alt_request': new_item.alt_request,
                    'upvoted_members': new_item.upvoted_members,
                    'date_added': new_item.date_added,
                    'coop_name': new_item.coop_name
                }
            )
        session.commit()
# Update one field of an item
def update_item_field(id, field, new_val):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.ShoppingList).filter(
            models.ShoppingList.item_id == id).update(
                {
                    field: new_val
                }
            )
        session.commit()
# Delete a shift's information
def delete_item(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.ShoppingList).filter(
            models.ShoppingList.item_id == id).delete()
        session.commit()

# Delete a shift's information
def delete_old_items():
    today = datetime.now()
    weekday = today.weekday()
    twoweeksago = str(datetime.now() - timedelta(days = 14))
    if weekday != 6:
        return
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.ShoppingList).filter(
            models.ShoppingList.date_added <= twoweeksago,
        ).delete()
        session.commit()
#----------------------------------------------------------------------
# Shift queries
#----------------------------------------------------------------------
# Add shift to calendar
def add_shift(shift: models.Shifts):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(shift)
        session.commit()
# Get shift from id
def get_shift(id) -> models.Shifts:
    shift = None
    with sqlalchemy.orm.Session(engine) as session:
        shift = session.query(models.Shifts).filter(
            models.Shifts.shift_id == id).first()
    return shift
# Get shift from id
def get_shift_notifications():
    notification_shifts = []
    tomorrow = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    tomorrow = str(tomorrow)
    with sqlalchemy.orm.Session(engine) as session:
        notification_shifts = session.query(models.Shifts).filter(
            models.Shifts.shift_time.contains(tomorrow)
        ).all()
    notification_members = []
    for shift in notification_shifts:
        for member in shift.shift_members:
            if member not in notification_members:
                user = get_user(member)
                if user is None:
                    continue
                if user.notify_email:
                    notification_members.append(member)
        if shift.shift_creator not in notification_members:
            user = get_user(shift.shift_creator)
            if user is None:
                    continue
            if user.notify_email:
                notification_members.append(shift.shift_creator)
    return notification_members
# Update a shift's information
def update_shift(id, new_shift: models.Shifts):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Shifts).filter(
            models.Shifts.shift_id == id).update(
                {
                    'shift_name': new_shift.shift_name,
                    'shift_type': new_shift.shift_type,
                    'shift_item': new_shift.shift_item,
                    'shift_time': new_shift.shift_time,
                    'shift_recurring': new_shift.shift_recurring,
                    'shift_day': new_shift.shift_day,
                    'shift_creator': new_shift.shift_creator,
                    'shift_members': new_shift.shift_members,
                    'coop_name': new_shift.coop_name
                }
            )
        session.commit()
# Delete a shift's information
def delete_shift(id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Shifts).filter(
            models.Shifts.shift_id == id).delete()
        session.commit()
#----------------------------------------------------------------------
# Recipe queries
#----------------------------------------------------------------------
def add_recipe(recipe: models.Recipes):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(recipe)
        session.commit()

# Delete a user's information
def delete_recipe(recipe_id):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.Recipes).filter(
            models.Recipes.recipe_id == recipe_id).delete()
        session.commit()

#----------------------------------------------------------------------
# Signin queries
#----------------------------------------------------------------------
def get_signin(netid) -> models.SignIn:
    signin = None
    with sqlalchemy.orm.Session(engine) as session:
        signin = session.query(models.SignIn).filter(
            models.SignIn.netid == netid).first()
    return signin

def add_signin(signin: models.SignIn):
    with sqlalchemy.orm.Session(engine) as session:
        session.add(signin)
        session.commit()

# Update a user's information
def update_signin(netid, new_signin: models.SignIn):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.SignIn).filter(
            models.SignIn.netid == netid).update(
                {
                    'netid': new_signin.netid,
                    'brunch': new_signin.brunch,
                    'brunch_guests': new_signin.brunch_guests,
                    'dinner': new_signin.dinner,
                    'dinner_guests': new_signin.dinner_guests,
                    'coop_name': new_signin.coop_name
                }
            )
        session.commit()

# Delete a user's information
def delete_signin(netid):
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.SignIn).filter(
            models.SignIn.netid == netid).first().delete()
        session.commit()

def get_total_guests(coop):
    total_count_brunch = 0
    total_count_dinner = 0
    with sqlalchemy.orm.Session(engine) as session:
        total_signin = session.query(models.SignIn).filter(
            models.SignIn.coop_name == coop,
        ).all()
        for member in total_signin:
            if member.brunch:
                total_count_brunch += member.brunch_guests + 1
            if member.dinner:
                total_count_dinner += member.dinner_guests + 1
        return (total_count_brunch, total_count_dinner)

def reset_signin():
    with sqlalchemy.orm.Session(engine) as session:
        session.query(models.SignIn).delete()
        session.commit()
#----------------------------------------------------------------------

# Unit testing for these
def main():
    print("No testing available for this")
if __name__ == '__main__':
    main()