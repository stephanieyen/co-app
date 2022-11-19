import flask
import database
import json
import models
import helper
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
from datetime import datetime, timedelta

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'coappemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'zdymxwgrisdsftkv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# Sends email every minute (WORKS)
def send_shift_emails():
    members = database.get_shift_notifications()
    for member in members:
        with app.app_context():
            email = member + "@princeton.edu"
            msg = Message(
                body="You have a shift tomorrow for your coop! Check it out!",
                sender="coappemail@gmail.com",
                subject="Co-App Addition!",
                recipients=[email])
            mail.send(msg)
            print("Email sent")

sched = BackgroundScheduler(daemon=True)
sched.add_job(send_shift_emails,'interval', minutes=1)
sched.start()

# Import after making auth since auth uses app
import auth

# Fake secret key ???
app.secret_key = b'\xbc>\xe0\xf8\xdf\x84\xe9aS\x02`i\x8e\xa1\xee\x92'
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
    _ = auth.authenticate()
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
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/profile.html',
            coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/profile/update', methods=['POST'])
def profile_update(coop):
    netid = auth.authenticate()
    old_user = database.get_user(netid)
    data = json.loads(flask.request.form.to_dict()['event_data'])
    cookday = ''
    for day in data['user_cookday']:
        cookday += day + ' '
    cookday.strip()
    choreday = ''
    for day in data['user_choreday']:
        choreday += day + ' '
    choreday.strip()
    new_user = models.Roster(
        user_netid=netid,
        user_name=data['user_name'],
        user_allergies=data['user_allergies'],
        user_admin=old_user.user_admin,
        user_cookday=cookday,
        user_choreday=choreday,
        coop_name=old_user.coop_name
    )
    database.update_user(netid, new_user)
    return json.dumps(new_user.user_name)

#----------------------------------------------------------------------

# Get all shifts for a given user
@app.route('/<coop>/profile/shifts', methods=['GET'])
def profile_shifts(coop):
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    shifts = database.get_user_shifts(netid)
    # for shift in shifts:
    #     print(shift.shift_members)
    return ""
    

#----------------------------------------------------------------------
# Co-Op Roster
#----------------------------------------------------------------------

@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    
    user = database.get_user(netid)

    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/roster.html',
            members=members, coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/members', methods=['GET'])
def roster_members(coop):
    # print("GET request for members")
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    members = database.get_roster_for_coop(coop)
    # for member in members:
    #     print(member.user_name)
    
    html_code = helper.genRosterHTML(members)

    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------
# Co-Op Edit Roster
#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit', methods=['GET'])
def edit_roster(coop):
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    if not user.user_admin:
        newPage = '/' + coop + '/members'
        return (False, flask.redirect(newPage))
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/edit_roster.html',
            members=members, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

# Add user
@app.route('/<coop>/roster/edit/add', methods=['POST'])
def add_user(coop):
    new_members = json.loads(flask.request.form.to_dict()['event_data'])
    for netid in new_members:
        user = models.Roster(user_netid=netid,
                            user_name='',
                            user_allergies='',
                            user_admin=False,
                            user_cookday='',
                            user_choreday='',
                            coop_name=coop)
        database.add_user(user)
        email = netid + "@princeton.edu"
        msg = Message(
            body="You've been added to a co-op on co-app! Go log in and update your profile!",
            sender="coappemail@gmail.com",
            subject="Co-App Addition!",
            recipients=["amkumar@princeton.edu", email])
        mail.send(msg)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit/delete', methods=['POST'])
def roster_delete(coop):
    ''' 
        Deletes a member from the roster of the co-op 
        in the specified route.                     
    '''
    user_id = flask.request.args.get('id') # make sure it's netid
    database.delete_user(user_id)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/members/overview', methods=['GET'])
def roster_overview(coop):
    # print("GET request for members")
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    members = database.get_roster_for_coop(coop)
    # for member in members:
    #     print(member.user_name)
    
    html_code = helper.genRosterOverviewHTML(members)

    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/roster/edit/makeadmin', methods=['POST'])
def make_admin(coop):
    user_id = flask.request.args.get('id') # make sure it's netid
    old_user = database.get_user(user_id)
    new_user = models.Roster(
        user_netid=user_id,
        user_name=old_user.user_name,
        user_allergies=old_user.user_allergies,
        user_admin= True,
        user_cookday=old_user.user_cookday,
        user_choreday=old_user.user_choreday,
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
    ''' Renders the calendar of the given co-op. '''
    # If posting, create new shift and then load in shifts
    if flask.request.method == 'POST':
        data = flask.request.form
        shift_recurring = True
        if data['event_data[shift_recurring]'] == 'false':
            shift_recurring = False
        # Turn members into a list
        members = data['event_data[shift_members]'].split(",")
        members = [m.strip() for m in members]
        # Deal with email notify
        email_notify = True
        new_shift_vals = [
            data['event_data[shift_name]'],
            data['event_data[shift_type]'],
            data['event_data[shift_item]'],
            data['event_data[shift_time]'],
            data['event_data[shift_day]'],
            shift_recurring,
            data['event_data[shift_creator]'],
            members,
            email_notify,
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
            notify_email=new_shift_vals[8],
            coop_name=new_shift_vals[9]
        )
        database.add_shift(new_shift)
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    # shifts_of_week = database.get_user_shifts('amkumar')
    # for shift in shifts_of_week:
    #     print(shift.shift_name)
    html_code = flask.render_template('templates/calendar_initialize.html',
                coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/calendar/delete', methods=['POST'])
def calendar_delete(coop):
    ''' 
        Deletes a shift from the calendar of the co-op 
        in the specified route.                     
    '''
    shift_id = flask.request.args.get('id')
    database.delete_shift(shift_id)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/calendar/update', methods=['POST'])
def calendar_update(coop):
    ''' 
        Updates a shift in the calendar of the co-op 
        in the specified route. 
    '''
    shift_id = flask.request.args.get('id')
    old_shift = database.get_shift(shift_id)
    data = flask.request.form

    # Turn members into a list
    members = data['event_data[shift_members]'].split(",")
    members = [m.strip() for m in members]
    # Update time
    shift_time = old_shift.shift_time[0:10]
    if data['event_data[shift_time]'] != "": 
        shift_time = shift_time + data['event_data[shift_time]']
    
    # GET NEW EMAIL NOTIFY VALUE
    email_notify = False
    # UPDATE THIS WHEN EMAIL NOTIFY ADDED
    new_shift_vals = [
        data['event_data[shift_name]'],
        data['event_data[shift_type]'],
        data['event_data[shift_item]'],
        shift_time,
        old_shift.shift_day,
        old_shift.shift_recurring,
        old_shift.shift_creator,
        members,
        email_notify,
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
        notify_email=new_shift_vals[8],
        coop_name=new_shift_vals[9]
    )
    database.update_shift(shift_id, new_shift)
    return ''

#----------------------------------------------------------------------
# UPDATE THIS WITH EMAIL NOTIFY
@app.route('/<coop>/events', methods=['GET'])
def events(coop):
    shifts = database.get_shifts_for_coop(coop)
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
        extendedProps['meal'] = shift.shift_item
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

    # get user info
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # items = database.get_shopping_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    # html = flask.render_template('templates/list.html',
    #         items=items, coop=coop, coop_upper=coop_upper)
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
        Deletes a shift from the shopping list of the co-op 
        in the specified route.                     
    '''
    item_id = flask.request.args.get('id')
    database.delete_item(item_id)
    return ''

#----------------------------------------------------------------------

# @app.route('/<coop>/items', methods=['GET'])
# def list_items(coop):
#     # print("GET request for items")
#     items = database.get_shopping_for_coop(coop)
#     # for item in items:
#     #     print(item.item_name)

#     html_code = helper.genItemTableHTML(items)
    
#     response = flask.make_response(html_code)
#     return response

#----------------------------------------------------------------------

@app.route('/<coop>/items/food', methods=['GET'])
def list_food_items(coop):
    # get user info
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # print("GET request for food items")
    items = database.get_food_list_for_coop(coop)
    # for item in items:
    #         print(item.item_name)

    html_code = helper.genItemTableHTML(items, True, user.user_admin, 
                                                        user.user_netid)
    
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/items/equipment', methods=['GET'])
def list_equipment_items(coop):
    # get user info
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # print("GET request for equipment items")
    items = database.get_equipment_list_for_coop(coop)
    # for item in items:
    #         print(item.item_name)

    html_code = helper.genItemTableHTML(items, False, user.user_admin,
                                                        user.user_netid)
    
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------
# Co-Op Recipes
#----------------------------------------------------------------------

@app.route('/<coop>/recipes', methods=['GET'])
def recipes(coop):
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/recipes.html',
                            coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/recipes/carousel', methods=['GET'])
def recipes_carousel(coop):
    # get user info
    netid = auth.authenticate()
    status, redirect = check_coop(coop)
    if status == False or status == "Nonexistent":
        return redirect
    user = database.get_user(netid)

    # print("GET request for food items")
    recipes = database.get_recipes_for_coop(coop)
    print(recipes)
    html_code = helper.genRecipeGalleryHTML(recipes)
    
    response = flask.make_response(html_code)
    return response
