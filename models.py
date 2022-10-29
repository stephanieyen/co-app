import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

# Roster table
class Roster (Base):
    __tablename__ = 'roster'
    user_email = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_name = sqlalchemy.Column(sqlalchemy.String)
    user_allergies = sqlalchemy.Column(sqlalchemy.String)
    user_admin = sqlalchemy.Column(sqlalchemy.Boolean)
    user_days = sqlalchemy.Column(sqlalchemy.String)
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Shopping list table
class ShoppingList (Base):
    __tablename__ = 'shoppinglist'
    item_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    item_type = sqlalchemy.Column(sqlalchemy.String)
    item_name = sqlalchemy.Column(sqlalchemy.String)
    item_quantity = sqlalchemy.Column(sqlalchemy.String)
    item_accepted = sqlalchemy.Column(sqlalchemy.String)
    item_reason = sqlalchemy.Column(sqlalchemy.String)
    requesting_user = sqlalchemy.Column(sqlalchemy.String)
    food_type = sqlalchemy.Column(sqlalchemy.String)
    alt_request = sqlalchemy.Column(sqlalchemy.String)
    coop_name = sqlalchemy.Column(sqlalchemy.String)

# Shifts table
class Shifts (Base):
    __tablename__ = 'shifts'
    shift_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    shift_name = sqlalchemy.Column(sqlalchemy.String)
    shift_type = sqlalchemy.Column(sqlalchemy.String)
    shift_item = sqlalchemy.Column(sqlalchemy.String)
    shift_time = sqlalchemy.Column(sqlalchemy.String)
    shift_day = sqlalchemy.Column(sqlalchemy.String)
    shift_creator = sqlalchemy.Column(sqlalchemy.String)
    shift_members = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
    coop_name = sqlalchemy.Column(sqlalchemy.String)