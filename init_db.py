import sqlalchemy
import sqlalchemy.orm
import models
import os
import database

db_url = os.getenv("DATABASE_URL")
# Add test users
def add_test_roster(session):
    user = models.Roster(user_netid='amkumar',
                        user_name='Arnav Kumar',
                        user_allergies='N/A',
                        user_admin=True,
                        user_cookday='M W F',
                        user_choreday='M',
                        notify_email = True,
                        coop_name='2d')
    session.add(user)
    user = models.Roster(user_netid='sy7',
                        user_name='Stephanie Yen',
                        user_allergies='N/A',
                        user_admin=True,
                        user_cookday='T W F',
                        user_choreday='T',
                        notify_email = False,
                        coop_name='2d')
    session.add(user)
    user = models.Roster(user_netid='petrino',
                        user_name='Erin Petrino',
                        user_allergies='Vegan',
                        user_admin=True,
                        user_cookday='T Th Sat Sun',
                        user_choreday='T',
                        notify_email = False,
                        coop_name='2d')
    session.add(user)
    user = models.Roster(user_netid='sarahep',
                        user_name='Sarah Pedersen',
                        user_allergies='Peanut Allergy',
                        user_admin=True,
                        user_cookday='M W F Sun',
                        user_choreday='M',
                        notify_email = False,
                        coop_name='2d')
    session.add(user)
    user = models.Roster(user_netid='thaldiya',
                        user_name='Tanvi Haldiya',
                        user_allergies='Soy Allergy',
                        user_admin=True,
                        user_cookday='M T Th F',
                        user_choreday='M',
                        notify_email = False,
                        coop_name='2d')
    session.add(user)
    user = models.Roster(user_netid='dpw',
                        user_name='David Walker',
                        user_allergies='N/A',
                        user_admin=True,
                        user_cookday='T W F',
                        user_choreday='T',
                        notify_email = False,
                        coop_name='brown')
    session.add(user)

#----------------------------------------------------------------------

# Add test shopping list
def add_test_shopping(session):
    # need Cinnamon and Broccoli for weeks of 2022-12-19, 2022-12-26, 2022-01-02
    item = models.ShoppingList(item_type="Food",
                            item_name="Cinnamon",
                            item_quantity="1 jar",
                            item_ordered=False,
                            for_shift = False,
                            item_reason='Cinnamon rolls',
                            requesting_user='sarahep',
                            food_type="Seasoning",
                            alt_request="",
                            upvoted_members=['amkumar'],
                            date_added="2022-12-19",
                            coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Food",
                        item_name="Cinnamon",
                        item_quantity="1 jar",
                        item_ordered=False,
                        for_shift = True,
                        item_reason='Cinnamon rolls',
                        requesting_user='sarahep',
                        food_type="Seasoning",
                        alt_request="",
                        upvoted_members=['sarahep'],
                        date_added="2022-12-26",
                        coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Food",
                        item_name="Cinnamon",
                        item_quantity="1 jar",
                        item_ordered=False,
                        for_shift = False,
                        item_reason='Cinnamon rolls',
                        requesting_user='sarahep',
                        food_type="Seasoning",
                        alt_request="",
                        upvoted_members=['sy7'],
                        date_added="2023-01-02",
                        coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Food",
                        item_name="Broccoli",
                        item_quantity="2 bags",
                        item_ordered=True,
                        for_shift = False,
                        item_reason='Ran out last week',
                        requesting_user='amkumar',
                        food_type="Produce",
                        alt_request="",
                        upvoted_members=['amkumar'],
                        date_added="2022-12-19",
                        coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Food",
                        item_name="Broccoli",
                        item_quantity="2 bags",
                        item_ordered=True,
                        for_shift = False,
                        item_reason='Ran out last week',
                        requesting_user='amkumar',
                        food_type="Produce",
                        alt_request="",
                        upvoted_members=['sy7'],
                        date_added="2022-12-26",
                        coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Food",
                    item_name="Broccoli",
                    item_quantity="2 bags",
                    item_ordered=True,
                    for_shift = True,
                    item_reason='Ran out last week',
                    requesting_user='amkumar',
                    food_type="Produce",
                    alt_request="",
                    upvoted_members=['petrino'],
                    date_added="2023-01-02",
                    coop_name='2d')
    session.add(item)

    # items for week of 2022-12-19
    item = models.ShoppingList(item_type="Food",
                        item_name="Coffee syrups",
                        item_quantity='3',
                        item_ordered=False,
                        for_shift = False,
                        item_reason='Lavender, pumpkin spice',
                        requesting_user='petrino',
                        food_type="Special",
                        alt_request="Creamer",
                        upvoted_members=['petrino'],
                        date_added="2022-12-19",
                        coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Equipment",
                            item_name="Nonstick Frying Pan",
                            item_quantity='1',
                            item_ordered=True,
                            for_shift = False,
                            item_reason='Old one broke, other pan too sticky',
                            requesting_user='sarahep',
                            food_type="Item",
                            alt_request="Stick Frying Pan",
                            upvoted_members=['sarahep'],
                            date_added="2022-12-19",
                            coop_name='2d')
    session.add(item)

    # items for week of 2022-12-26
    item = models.ShoppingList(item_type="Food",
                            item_name="Sriracha",
                            item_quantity='1',
                            item_ordered=True,
                            for_shift = True,
                            item_reason='One large bottle',
                            requesting_user='sy7',
                            food_type="Condiment",
                            alt_request="Tabasco",
                            upvoted_members=['sy7'],
                            date_added="2022-12-26",
                            coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Equipment",
                            item_name="Bread Roller",
                            item_quantity='1',
                            item_ordered=False,
                            for_shift = False,
                            item_reason='Want to make pizza one day',
                            requesting_user='thaldiya',
                            food_type="Item",
                            alt_request="Hammer",
                            upvoted_members=['thaldiya'],
                            date_added="2022-12-26",
                            coop_name='2d')
    session.add(item)
    
    # items for week of 2022-01-02
    item = models.ShoppingList(item_type="Food",
                            item_name="Half and Half",
                            item_quantity='1 pint',
                            item_ordered=False,
                            for_shift = False,
                            item_reason='For any coffee :)',
                            requesting_user='petrino',
                            food_type="Dairy",
                            alt_request="Creamer",
                            upvoted_members=['sarahep'],
                            date_added="2023-01-02",
                            coop_name='2d')
    session.add(item)
    item = models.ShoppingList(item_type="Equipment",
                            item_name="Computer",
                            item_quantity='10',
                            item_ordered=False,
                            for_shift = False,
                            item_reason='Turn Brown into computer hub',
                            requesting_user='sy7',
                            food_type="Special",
                            alt_request="Laptops",
                            upvoted_members=['petrino'],
                            date_added="2023-01-02",
                            coop_name='2d')
    session.add(item)

#----------------------------------------------------------------------

# Add test shifts
def add_test_shifts(session):
    shift = models.Shifts(shift_name='Going to Wegmans',
                        shift_type='Shopping',
                        shift_item='N/A',
                        shift_time='2022-11-03T03:30:00',
                        shift_recurring=False,
                        shift_day=[4],
                        shift_creator='amkumar',
                        shift_members=['amkumar', 'sy7'],
                        coop_name='2d')
    session.add(shift)
    shift = models.Shifts(shift_name='Brunch',
                        shift_type='Cooking',
                        shift_item='French Toast With Berries',
                        shift_time='2022-10-30T09:30:00',
                        shift_recurring=False,
                        shift_day=[0],
                        shift_creator='thaldiya',
                        shift_members=['thaldiya'],
                        coop_name='ifc')
    session.add(shift)

#----------------------------------------------------------------------

# Add test recipes
def add_test_recipes(session): 
    recipe = models.Recipes(recipe_author='sy7',
                            recipe_name='Cookie Pizza', 
                            recipe_type='Dessert',
                            recipe_link='https://sallysbakingaddiction.com/chocolate-chip-cookie-pizza/',
                            recipe_ingredients='See link',
                            recipe_instructions='See link', 
                            recipe_img='https://res.cloudinary.com/coapp/image/upload/v1669245543/temy5m0ejvyfs2iydsqc.jpg',
                            coop_name='2d')
    session.add(recipe)
    recipe = models.Recipes(recipe_author='petrino',
                            recipe_name='the best pad thai you will ever have', 
                            recipe_type='Dinner',
                            recipe_link='',
                            recipe_ingredients='See link',
                            recipe_instructions='See link', 
                            recipe_img='https://res.cloudinary.com/coapp/image/upload/v1669151022/prjhmx1wqmkxxzoypekd.png',
                            coop_name='scully')
    session.add(recipe)    

#----------------------------------------------------------------------

# Add test recipes
def add_test_signin(session): 
    signin = models.SignIn(
        netid = 'amkumar',
        coop_name = '2d',
        brunch = True,
        brunch_guests = 0,
        dinner = True,
        dinner_guests = 0
    )
    session.add(signin)
    signin = models.SignIn(
        netid = 'sy7',
        coop_name = '2d',
        brunch = False,
        brunch_guests = 0,
        dinner = True,
        dinner_guests = 2
    )
    session.add(signin)

#----------------------------------------------------------------------

def main():
    # Create engine and drop and recreate all tables
    engine = sqlalchemy.create_engine(db_url)
    # models.Base.metadata.drop_all(engine)
    # models.Base.metadata.create_all(engine)

    with sqlalchemy.orm.Session(engine) as session:
        # Add fake test data if needed
        # add_test_roster(session)
        # add_test_shopping(session)
        # add_test_shifts(session)
        # add_test_recipes(session)
        # add_test_signin(session)
        session.commit()
        
    engine.dispose()

if __name__ == '__main__':
    main()


