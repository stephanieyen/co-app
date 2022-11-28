import sqlalchemy.ext.declarative
import sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY

Base = sqlalchemy.ext.declarative.declarative_base()

# Roster table
class Roster (Base):
    __tablename__ = 'roster'
    user_netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_name = sqlalchemy.Column(sqlalchemy.String)
    user_allergies = sqlalchemy.Column(sqlalchemy.String)
    user_admin = sqlalchemy.Column(sqlalchemy.Boolean)
    user_cookday = sqlalchemy.Column(sqlalchemy.String)
    user_choreday = sqlalchemy.Column(sqlalchemy.String)
    notify_email = sqlalchemy.Column(sqlalchemy.Boolean)
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Shopping list table
class ShoppingList (Base):
    __tablename__ = 'shoppinglist'
    item_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    item_type = sqlalchemy.Column(sqlalchemy.String)
    item_name = sqlalchemy.Column(sqlalchemy.String)
    item_quantity = sqlalchemy.Column(sqlalchemy.String)
    item_ordered = sqlalchemy.Column(sqlalchemy.Boolean)
    for_shift = sqlalchemy.Column(sqlalchemy.Boolean)
    item_reason = sqlalchemy.Column(sqlalchemy.String)
    requesting_user = sqlalchemy.Column(sqlalchemy.String) # item_author
    food_type = sqlalchemy.Column(sqlalchemy.String)
    alt_request = sqlalchemy.Column(sqlalchemy.String)
    upvoted_members = sqlalchemy.Column(ARRAY(sqlalchemy.String))
    date_added = sqlalchemy.Column(sqlalchemy.String)
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Shifts table
class Shifts (Base):
    __tablename__ = 'shifts'
    shift_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    shift_name = sqlalchemy.Column(sqlalchemy.String)
    shift_type = sqlalchemy.Column(sqlalchemy.String)
    shift_item = sqlalchemy.Column(sqlalchemy.String)
    shift_time = sqlalchemy.Column(sqlalchemy.String)
    shift_recurring = sqlalchemy.Column(sqlalchemy.Boolean)
    shift_day = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
    shift_creator = sqlalchemy.Column(sqlalchemy.String) # shift_author
    shift_members = sqlalchemy.Column(ARRAY(sqlalchemy.String))
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Recipes table
class Recipes(Base): 
    __tablename__ = 'recipes'
    recipe_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    recipe_author = sqlalchemy.Column(sqlalchemy.String)
    recipe_name = sqlalchemy.Column(sqlalchemy.String)
    recipe_link = sqlalchemy.Column(sqlalchemy.String)
    recipe_ingredients = sqlalchemy.Column(sqlalchemy.String)
    recipe_instructions = sqlalchemy.Column(sqlalchemy.String)
    recipe_img = sqlalchemy.Column(sqlalchemy.String)
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Sign-in table
class SignIn(Base):
    __tablename__ = 'signin'
    netid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    coop_name = sqlalchemy.Column(sqlalchemy.String)
    brunch = sqlalchemy.Column(sqlalchemy.Boolean)
    brunch_guests = sqlalchemy.Column(sqlalchemy.Integer)
    dinner = sqlalchemy.Column(sqlalchemy.Boolean)
    dinner_guests = sqlalchemy.Column(sqlalchemy.Integer)

    