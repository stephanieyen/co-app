import flask
import database
import html
import json
import models
import helper
from flask import jsonify
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'coappemail@gmail.com'
# app.config['MAIL_PASSWORD'] = 'zdymxwgrisdsftkv'
app.config['MAIL_PASSWORD'] = os.getenv("APP_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# Sends email every day
def send_shift_emails():
    # Delete old shopping list items once a week
    database.delete_old_items()
    # Reset signin table
    database.reset_signin()
    members = database.get_shift_notifications()
    for member in members:
        with app.app_context():
            email = member + "@princeton.edu"
            msg = Message(
                body="You have a shift tomorrow for your coop! Check it out at https://co-app.onrender.com!",
                sender="coappemail@gmail.com",
                subject="Co-App Shift Reminder!",
                recipients=[email])
            mail.send(msg)

# Import after making auth since auth uses app
import auth

app.secret_key = os.getenv('SECRET_KEY')

#----------------------------------------------------------------------
# Co-App
#----------------------------------------------------------------------

# Home page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = flask.render_template('templates/index.html')
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# CAS Login Route
@app.route('/netID', methods=['GET'])
def netID():
    netid = auth.authenticate()
    if netid is None:
        return flask.redirect('/error')
    coop = flask.session.get('coop')
    newPage = '/' + coop
    return flask.redirect(newPage)

def check_coop(current_coop):
    netid = auth.authenticate()
    if netid is None:
        return ('Nonexistent', flask.redirect('/error'))
    coop = flask.session.get('coop')
    if coop != current_coop:
        newPage = '/' + coop
        return (False, flask.redirect(newPage))
    else:
        return (True, "")    

# Error page
@app.route('/error', methods=['GET'])
def error_page():
    #_ = auth.authenticate()
    status, redirect = check_coop('')
    if status == False:
        return redirect
    html = flask.render_template('templates/profile_error.html')
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# Co-Op Profile
#----------------------------------------------------------------------

@app.route('/<coop>/profile', methods=['GET'])
def profile(coop):
    '''
        Renders the Profile page of an authenticated Co-App user
        (who is a member or admin of the co-op in the specified route).
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # render Profile page HTML
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/profile.html',
            coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/profile/update', methods=['POST'])
def profile_update(coop):
    '''
        Updates the profile of an authenticated Co-App user, who can 
        edit their name, allergies, shift days, and/or notification 
        preferences.
    '''
    # get user to edit
    netid = auth.authenticate()
    old_user = database.get_user(netid)

    # get edited data
    data = json.loads(flask.request.form.to_dict()['event_data'])

    cookday = ''
    for day in data['user_cookday']:
        cookday += day + ' '
    cookday.strip()

    choreday = ''
    for day in data['user_choreday']:
        choreday += day + ' '
    choreday.strip()

    # update user info
    new_user = models.Roster(
        user_netid=netid,
        user_name=data['user_name'],
        user_allergies=data['user_allergies'],
        user_admin=old_user.user_admin,
        user_cookday=cookday,
        user_choreday=choreday,
        notify_email = data['notify_on'],
        coop_name=old_user.coop_name
    )
    database.update_user(netid, new_user)
    return json.dumps(new_user.user_name)

#----------------------------------------------------------------------

# @app.route('/<coop>/profile/shifts', methods=['GET'])
# def profile_shifts(coop):
#     '''
#         Get all the shifts for an authenticated user.
#     '''
#     # get user info + redirect if needed
#     netid = auth.authenticate()
#     status, redirect = check_coop(coop)
#     if status == False or status == "Nonexistent":
#         return redirect
    
#     shifts = database.get_user_shifts(netid)
#     return ""

#----------------------------------------------------------------------
# Co-Op Roster
#----------------------------------------------------------------------

@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    '''
        Renders the Roster page of the co-op in the specified route,
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # render Roster page HTML
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/roster.html',
            members=members, coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/roster/members', methods=['GET'])
def roster_members(coop):
    '''
        Fetches the Co-App members in the co-op and returns the HTML 
        code for the roster table that shows these members.
    '''
    # get user info + redirect if needed
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    
    # return roster table HTML
    members = database.get_roster_for_coop(coop)
    html_code = helper.gen_roster_table_html(members)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------
# Co-Op Edit Roster (admin-only)
#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit', methods=['GET'])
def edit_roster(coop):
    '''
        Renders the Edit Roster page (admin-only) of the co-op in the
        specified route.
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # redirect the user if not admin
    if not user.user_admin:
        newPage = '/' + coop + '/members'
        return (False, flask.redirect(newPage))
    
    # render Edit Roster page HTML
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/edit_roster.html',
            members=members, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit/add', methods=['POST'])
def add_user(coop):
    '''
        Adds new members to the co-op roster based on input netid(s).
    '''
    new_members = json.loads(flask.request.form.to_dict()['event_data'])
    for netid in new_members:
        # create empty user model 
        user = models.Roster(user_netid=netid,
                            user_name=netid,
                            user_allergies='',
                            user_admin=False,
                            user_cookday='',
                            user_choreday='',
                            coop_name=coop)
        status, message = database.add_user(user)
        if status == False:
            if 'duplicate key' in message:
                error_msg = "User is already in a co-op!"
                error_msg += " If you think this is a mistake, "
                error_msg += "ask them to delete their profile and then try adding them again!"
                return error_msg, 400
            else:
                return message, 400
        # send email notification
        email = netid + "@princeton.edu"
        msg = Message(
            body="You've been added to a co-op on co-app! Go log in and update your profile at https://co-app.onrender.com!",
            sender="coappemail@gmail.com",
            subject="Co-App Addition!",
            recipients=[email])
        mail.send(msg)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit/delete', methods=['POST'])
def roster_delete(coop):
    ''' 
        Deletes a member from the co-op roster.                 
    '''
    user_id = flask.request.args.get('id') # make sure it's netid
    database.delete_user(user_id)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/members/admin_view', methods=['GET'])
def roster_members_admin_view(coop):
    '''
        Fetches the Co-App members in the co-op and returns the HTML 
        code for the roster table that shows these members and 
        which has extra admin permissions:
            Add, Remove, Make Admin
    '''
    # get user info + redirect if needed
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    
    # return roster table (admin view) HTML
    members = database.get_roster_for_coop(coop)
    html_code = helper.gen_roster_table_admin_html(members)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit/makeadmin', methods=['POST'])
def make_admin(coop):
    '''
        Updates the admin status of a specified user in the co-op.
    '''
    # get user to edit
    user_id = flask.request.args.get('id') # make sure it's netid
    old_user = database.get_user(user_id)

    # update user admin status to True
    new_user = models.Roster(
        user_netid=user_id,
        user_name=old_user.user_name,
        user_allergies=old_user.user_allergies,
        user_admin= True,
        user_cookday=old_user.user_cookday,
        user_choreday=old_user.user_choreday,
        notify_email = old_user.notify_email,
        coop_name=old_user.coop_name
    )
    database.update_user(user_id, new_user)
    return ''

#----------------------------------------------------------------------
# Co-Op Calendar
#----------------------------------------------------------------------

@app.route('/<coop>', methods=['GET', 'POST'])
@app.route('/<coop>/calendar', methods=['GET', 'POST'])
def calendar(coop):
    ''' 
        Renders the Calendar page of the co-op in the specified route.
    '''
    # if POST request, add new shift to database
    if flask.request.method == 'POST':
        data = flask.request.form
        shift_recurring = True
        if data['event_data[shift_recurring]'] == 'false':
            shift_recurring = False
        # Turn members into a list
        members = data['event_data[shift_members]'].split(",")
        members = [m.strip() for m in members]
        members.pop()
        new_shift_vals = [
            data['event_data[shift_name]'],
            data['event_data[shift_type]'],
            data['event_data[shift_item]'],
            data['event_data[shift_time]'],
            data['event_data[shift_day]'],
            shift_recurring,
            data['event_data[shift_creator]'],
            members,
            coop
        ]
        new_shift = models.Shifts(
            shift_name=new_shift_vals[0],
            shift_type=new_shift_vals[1],
            shift_item=new_shift_vals[2],
            shift_time=new_shift_vals[3],
            shift_day=new_shift_vals[4],
            shift_recurring=new_shift_vals[5],
            shift_creator=new_shift_vals[6],
            shift_members=new_shift_vals[7],
            coop_name=new_shift_vals[8]
        )
        database.add_shift(new_shift)
    
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    members = database.get_names_for_coop(coop)
    # render Calendar page HTML
    coop_upper = database.get_upper_coop(coop)
    html_code = flask.render_template('templates/calendar_initialize.html',
                coop=coop, coop_upper=coop_upper, user=user, members=members)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/calendar/delete', methods=['POST'])
def calendar_delete(coop):
    ''' 
        Deletes a shift from the co-op calendar.     
    '''
    shift_id = flask.request.args.get('id')
    database.delete_shift(shift_id)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/calendar/update', methods=['POST'])
def calendar_update(coop):
    ''' 
        Updates a shift in the co-op calendar.
    '''
    shift_id = flask.request.args.get('id')
    old_shift = database.get_shift(shift_id)
    data = flask.request.form

    # Turn members into a list
    members = data['event_data[shift_members]'].split(",")
    members = [m.strip() for m in members]
    members.pop()
    
    new_shift_vals = [
        data['event_data[shift_name]'],
        data['event_data[shift_type]'],
        data['event_data[shift_item]'],
        data['event_data[shift_time]'],
        old_shift.shift_day,
        old_shift.shift_recurring,
        old_shift.shift_creator,
        members,
        old_shift.coop_name
    ]
    # jsdata = request.form['event_data']
    # print(json.loads(jsdata[0]))
    new_shift = models.Shifts(
        shift_name=new_shift_vals[0],
        shift_type=new_shift_vals[1],
        shift_item=new_shift_vals[2],
        shift_time=new_shift_vals[3],
        shift_day=new_shift_vals[4],
        shift_recurring=new_shift_vals[5],
        shift_creator=new_shift_vals[6],
        shift_members=new_shift_vals[7],
        coop_name=new_shift_vals[8]
    )
    database.update_shift(shift_id, new_shift)
    return ''

#----------------------------------------------------------------------
@app.route('/<coop>/events', methods=['GET'])
def events(coop):
    start_date = flask.request.args.get('start')[0:10]
    end_date = flask.request.args.get('end')[0:10]

    shifts = database.get_shifts_for_week(coop, start_date, end_date)
    event_json = []
    for shift in shifts: 
        extendedProps = {}
        extendedProps['type'] = shift.shift_type
        # Format members string to be nicer
        members_string = ""
        for member in shift.shift_members:
            members_string += member + ", "
        members_string = members_string[:-2]
        members_string.strip()
        extendedProps['members'] = members_string
        extendedProps['meal'] = html.escape(shift.shift_item)
        extendedProps['creator'] = shift.shift_creator

        data = {}
        data['id'] = shift.shift_id
        data['title'] = shift.shift_name

        # account for recurring events
        if shift.shift_recurring:
            data['daysOfWeek'] = shift.shift_day
            data['startRecur'] = shift.shift_time[0:10]
            data['startTime'] = shift.shift_time[11:]
        else:
            data['start'] = shift.shift_time

        data['extendedProps'] = extendedProps
        type = shift.shift_type
        if type == "Shopping":
            data['color'] = "#a5d4e8" # blue
        elif type == "Cooking":
            data['color'] = "#c4f5d3" # green
        else:
            data['color'] = "#FFDBE9" # light pink
        event_json.append(data)

    return jsonify(event_json)

#----------------------------------------------------------------------
# Co-Op Shopping List
#----------------------------------------------------------------------

@app.route('/<coop>/list', methods=['GET', 'POST'])
def list(coop):
    '''
        Renders the Shopping List page of the co-op in the specified
        route.
    '''
    # if POST request, add new item to database
    if flask.request.method == 'POST':
        data = json.loads(flask.request.form.to_dict()['event_data'])

        # What to display for "For Shift" - Yes/No
        today = str(datetime.now().strftime('%Y-%m-%d'))
        new_item = models.ShoppingList(
            item_type=data['item_type'],
            item_name=data['item_name'],
            item_quantity=data['item_quantity'],
            item_ordered=False,
            for_shift=data['for_shift'],
            item_reason=data['item_reason'],
            requesting_user=data['requesting_user'],
            food_type=data['food_type'],
            alt_request=data['alt_request'],
            upvoted_members=[data['requesting_user']],
            date_added=today,
            coop_name=coop
        )
        database.add_item(new_item)

    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # render Shopping List page HTML
    coop_upper = database.get_upper_coop(coop)
    html_code = flask.render_template('templates/list.html', 
                        coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/list/order', methods=['POST'])
def change_ordered(coop):
    ''' 
        Updates a shift whether an item was ordered after
        clicking checkbox                   
    '''
    item_id = flask.request.args.get('id')
    old_item = database.get_item(item_id)
    # Make new item with opposite ordered as old_item
    database.update_item_field(item_id, "item_ordered", not old_item.item_ordered)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/list/upvote', methods=['POST'])
def change_upvote(coop):
    ''' 
        Updates a shift whether an item was ordered after
        clicking checkbox                   
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    
    item_id = flask.request.args.get('id')
    old_item = database.get_item(item_id)
    old_upvotes = old_item.upvoted_members
    if netid in old_upvotes:
        old_upvotes.remove(netid)
    else:
        old_upvotes.append(netid)
    # Make new item with new upvotes list
    database.update_item_field(item_id, "upvoted_members", old_upvotes)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/list/delete', methods=['POST'])
def list_delete(coop):
    ''' 
        Deletes a shift from the co-op shopping list.              
    '''
    item_id = flask.request.args.get('id')
    database.delete_item(item_id)
    return ''

#----------------------------------------------------------------------

# TRIED TO MAKE A HELPER FUNCTION BUT IT DID NOT WORK
# def list_items(coop, is_food):
#     # get user info + redirect if needed
#     netid = auth.authenticate()
#     status, redirect = check_coop(coop)
#     if status == False or status == "Nonexistent":
#         return redirect
#     user = database.get_user(netid)

#     start_date = flask.request.args.get('startDate')
#     end_date = flask.request.args.get('endDate')

#     items = database.get_food_list_for_week(coop, start_date, end_date)
#     html_code = helper.gen_item_table_html(items, is_food, user.user_admin, 
#                                                         user.user_netid)
    
#     response = flask.make_response(html_code)
#     return response

#----------------------------------------------------------------------


@app.route('/<coop>/items/food', methods=['GET'])
def list_food_items(coop):
    # return list_items(coop, True)
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    start_date = flask.request.args.get('startDate')
    end_date = flask.request.args.get('endDate')

    items = database.get_food_list_for_week(coop, start_date, end_date)
    html_code = helper.gen_item_table_html(items, True, user.user_admin, 
                                                        user.user_netid)
    
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/items/equipment', methods=['GET'])
def list_equipment_items(coop):
    # return list_items(coop, False)
    # # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    start_date = flask.request.args.get('startDate')
    end_date = flask.request.args.get('endDate')

    items = database.get_equipment_list_for_week(coop, start_date, end_date)
    html_code = helper.gen_item_table_html(items, False, user.user_admin,
                                                        user.user_netid)
    
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------
# Co-Op Recipes
#----------------------------------------------------------------------

@app.route('/<coop>/recipes', methods=['GET','POST'])
def recipes(coop):
    '''
        Renders the Recipes page of the co-op in the specified route.
    '''

    # if POST request, add new recipe to database
    if flask.request.method == 'POST':
        data = json.loads(flask.request.form.to_dict()['event_data'])

        new_recipe = models.Recipes(
            recipe_author=data['recipe_author'],
            recipe_name=data['recipe_name'],
            recipe_type=data['recipe_type'],
            recipe_link=data['recipe_link'],
            recipe_ingredients=data['recipe_ingredients'],
            recipe_instructions=data['recipe_instructions'],
            recipe_img=data['recipe_img'],
            coop_name=coop
        )
        database.add_recipe(new_recipe)
        print(new_recipe)

     # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # render Recipe page HTML
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/recipes.html',
                            coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/recipes/gallery', methods=['GET'])
def recipes_carousel(coop):
    '''
        Fetches the recipes of the co-op and returns the HTML code
        for the recipe gallery that shows these recipes.
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # get meal type to generate according recipes
    meal_type = flask.request.args.get('meal')
    meal_type.strip()
    # print("meal = ", meal)
    if meal_type == "All":
        meal_type = "%"

    # return recipe gallery HTML
    recipes = database.get_recipes_for_coop(coop, meal_type)
    html_code = helper.gen_recipe_gallery_html(recipes)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/recipes/delete', methods=['POST'])
def recipes_delete(coop):
    ''' 
        Deletes a recipe from the co-op recipes.            
    '''
    recipe_id = flask.request.args.get('id')
    database.delete_recipe(recipe_id)
    return ''

#----------------------------------------------------------------------
# Co-Op Sign-in
#----------------------------------------------------------------------

@app.route('/<coop>/checkin', methods=['GET','POST'])
def sign_in(coop):
    '''
        Renders the Check In page of the co-op in the specified route.
    '''
    # if POST request, add new recipe to database
    if flask.request.method == 'POST':
        data = json.loads(flask.request.form.to_dict()['event_data'])
        new_signin = models.SignIn(
            netid = data['netid'],
            coop_name = coop,
            brunch = data['brunch'],
            brunch_guests = data['brunch_guests'],
            dinner = data['dinner'],
            dinner_guests = data['dinner_guests']
        )
        if database.get_signin(data['netid']) is not None:
            database.update_signin(data['netid'], new_signin)
        else:
            database.add_signin(new_signin)


    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    # render signin page HTML
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/check_in.html',
                            coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

@app.route('/<coop>/checkin/details', methods=['GET'])
def sign_in_details(coop):
    '''
        Sends data to signin page
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    signin = database.get_signin(netid)
    if signin is None:
        data = {}
        data['brunch'] = False
        data['brunch_guests'] = 0
        data['dinner'] = False
        data['dinner_guests'] = 0
        data['current_count_brunch'], data['current_count_dinner'] = database.get_total_guests(coop)
        return jsonify(data)
    data = {}
    data['brunch'] = signin.brunch
    data['brunch_guests'] = signin.brunch_guests
    data['dinner'] = signin.dinner
    data['dinner_guests'] = signin.dinner_guests
    data['current_count_brunch'], data['current_count_dinner'] = database.get_total_guests(coop)
    return jsonify(data)

#----------------------------------------------------------------------
# Co-Op About + Help Page
#----------------------------------------------------------------------

@app.route('/about', methods=['GET'])
def about():
    '''
        Renders About Page
    '''
    html = flask.render_template('templates/about.html')
    response = flask.make_response(html)
    return response
    

@app.route('/<coop>/help', methods=['GET'])
def help(coop):
    '''
        Renders Help Page
    '''
    # get user info + redirect if needed
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    # render signin page HTML
    coop_upper = database.get_upper_coop(coop)

    html = flask.render_template('templates/help.html', coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response