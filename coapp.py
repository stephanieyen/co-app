import flask
import database
import json
import models
from flask import jsonify
#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

# Import after making auth since auth uses app
import auth

# Fake secret key ???
app.secret_key = b'\xbc>\xe0\xf8\xdf\x84\xe9aS\x02`i\x8e\xa1\xee\x92'
#----------------------------------------------------------------------

# Home page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = flask.render_template('index.html')
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# Routes for Co-ops
# Co-op Calendar
@app.route('/<coop>', methods=['GET', 'POST'])
@app.route('/<coop>/calendar', methods=['GET', 'POST'])
def calendar(coop):
    # If posting, create new shift and then load in shifts
    if flask.request.method == 'POST':
        data = flask.request.form
        new_shift_vals = [
            data['event_data[shift_name]'],
            data['event_data[shift_type]'],
            data['event_data[shift_item]'],
            data['event_data[shift_time]'],
            data['event_data[shift_day]'],
            data['event_data[shift_recurring'],
            data['event_data[shift_creator]'],
            [data['event_data[shift_members]']],
            coop
        ]
        # jsdata = request.form['event_data']
        # print(json.loads(jsdata[0]))
        new_shift = models.Shifts(shift_name=new_shift_vals[0],
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
    netid = auth.authenticate()
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    html_code = flask.render_template('calendar_initialize.html',
                coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html_code)
    return response

@app.route('/<coop>/events', methods=['GET'])
def events(coop):
    shifts = database.get_shifts_for_coop(coop)
    event_json = []
    for shift in shifts: 
        extendedProps = {}
        extendedProps['type'] = shift.shift_type
        extendedProps['members'] = shift.shift_members
        extendedProps['meal'] = shift.shift_item

        data = {}
        data['id'] = shift.shift_id
        data['start'] = shift.shift_time
        data['title'] = shift.shift_name
        data['extendedProps'] = extendedProps
        type = shift.shift_type
        if type == "Shopping":
            data['color'] = "#a5d4e8" # blue
        elif type == "Cooking":
            data['color'] = "#c4f5d3" # green
        else:
            data['color'] = "#f1d5f2" # pink
        event_json.append(data)
    print(jsonify(event_json))
    return jsonify(event_json)

# Co-op Roster
@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('roster.html',
            members=members, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

# Co-op Roster Update
@app.route('/<coop>/roster/info', methods=['GET'])
def roster_info(coop):
    netid = auth.authenticate()
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('profile.html',
            user=user, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

# Co-op Shopping List
@app.route('/<coop>/list', methods=['GET', 'POST'])
def list(coop):
    if flask.request.method == 'POST':
        data = json.loads(flask.request.form.to_dict()['event_data'])

        new_item = models.ShoppingList(item_type=data['item_type'],
                                    item_name=data['item_name'],
                                    item_quantity=data['item_quantity'],
                                    item_ordered=False,
                                    for_shift=False,
                                    item_reason=data['item_reason'],
                                    requesting_user=data['requesting_user'],
                                    food_type=data['food_type'],
                                    alt_request=data['alt_request'],
                                    coop_name=coop
                                    )
        print(new_item)
        database.add_item(new_item)

    items = database.get_shopping_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('shoppinglist.html',
            items=items, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

# Co-op Profile
@app.route('/<coop>/profile', methods=['GET'])
def profile(coop):
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('profile.html',
            coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# CAS Login Route
@app.route('/netID', methods=['GET'])
def netID():
    _ = auth.authenticate()
    coop = flask.session.get('coop')
    if coop == 'brown':
        return flask.redirect('/brown')
    elif coop == 'scully':
        return flask.redirect('/scully')
    elif coop == 'ifc':
        return flask.redirect('/ifc')
    elif coop == '2d':
        return flask.redirect('/2d')
    elif coop == 'realfood':
        return flask.redirect('/realfood')

