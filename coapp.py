from hashlib import new
import flask
import database
import json
import models
#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

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
                                shift_creator=new_shift_vals[5],
                                shift_members=new_shift_vals[6],
                                coop_name=new_shift_vals[7]
                                )
        print(new_shift)
        database.add_shift(new_shift)
    shifts = database.get_shifts_for_coop(coop)
    event_json = []
    for shift in shifts: 
        data = {}
        data['start'] = shift.shift_time
        data['title'] = shift.shift_name
        data['type'] = shift.shift_type
        data['members'] = shift.shift_members
        data['item'] = shift.shift_item
        type = shift.shift_type
        if type == "Shopping":
            data['color'] = "#a5d4e8" # blue
        elif type == "Cooking":
            data['color'] = "#c4f5d3" # green
        else:
            data['color'] = "#f1d5f2" # pink
        event_json.append(data)
    coop_upper = database.get_upper_coop(coop)
    html_code = flask.render_template('calendar_initialize.html',
                events=event_json, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html_code)
    return response

# Co-op Roster
@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('roster.html',
            members=members, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

# Co-op Shopping List
@app.route('/<coop>/list', methods=['GET', 'POST'])
def list(coop):
    if flask.request.method == 'POST':
        data = flask.request.form 
        new_item_vals = [
            data['event_data[item_type]'],
            data['event_data[item_name]'],
            data['event_data[item_quantity]'],
            data['event_data[item_ordered]'],
            data['event_data[for_shift]'],
            data['event_data[item_reason]'],
            data['event_data[requesting_user]'],
            data['event_data[food_type]'],
            data['event_data[alt_request]'],
            coop
        ]
        new_item = models.ShoppingList(item_type=new_item_vals[0],
                                    item_name=new_item_vals[1],
                                    item_quantity=new_item_vals[2],
                                    item_ordered=new_item_vals[3],
                                    for_shift=new_item_vals[4],
                                    item_reason=new_item_vals[5],
                                    requesting_user=new_item_vals[6],
                                    food_type=new_item_vals[7],
                                    alt_request=new_item_vals[8],
                                    coop_name=new_item_vals[9]
                                    )
        print(new_item)
        database.add_item(new_item)

    items = database.get_shopping_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('shoppinglist.html',
            items=items, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------