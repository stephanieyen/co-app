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
    html = flask.render_template('templates/index.html')
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
        new_shift_vals = [
            data['event_data[shift_name]'],
            data['event_data[shift_type]'],
            data['event_data[shift_item]'],
            data['event_data[shift_time]'],
            data['event_data[shift_day]'],
            shift_recurring,
            data['event_data[shift_creator]'],
            [data['event_data[shift_members]']],
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
    netid = auth.authenticate()
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    html_code = flask.render_template('templates/calendar_initialize.html',
                coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/calendar/delete', methods=['POST'])
def calendar_delete():
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
    # Once recurring done, do this
    # shift_recurring = True
    # if data['event_data[shift_recurring]'] == 'false':
    #     shift_recurring = False
    new_shift_vals = [
        data['event_data[shift_name]'],
        data['event_data[shift_type]'],
        data['event_data[shift_item]'],
        data['event_data[shift_time]'],
        old_shift.shift_day,
        old_shift.shift_recurring,
        old_shift.shift_creator,
        [data['event_data[shift_members]']],
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
    shifts = database.get_shifts_for_coop(coop)
    event_json = []
    for shift in shifts: 
        extendedProps = {}
        extendedProps['type'] = shift.shift_type
        extendedProps['members'] = shift.shift_members
        extendedProps['meal'] = shift.shift_item
        extendedProps['creator'] = shift.shift_creator

        data = {}
        data['id'] = shift.shift_id
        data['title'] = shift.shift_name

        # account for recurring events
        if shift.shift_recurring:
            data['daysOfWeek'] = shift.shift_day
            data['startRecur'] = shift.shift_time
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
# Co-Op Roster
#----------------------------------------------------------------------

@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    members = database.get_roster_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/roster.html',
            members=members, coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------
# Co-Op Shopping List
#----------------------------------------------------------------------

@app.route('/<coop>/list', methods=['GET', 'POST'])
def list(coop):
    if flask.request.method == 'POST':
        data = json.loads(flask.request.form.to_dict()['event_data'])

        # What to display for "For Shift" - Yes/No

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
            coop_name=coop
        )
        database.add_item(new_item)
        # print("checking if it actually added")
        # items = database.get_shopping_for_coop(coop)
        # for item in items:
        #     print(item.item_name)
        

    # items = database.get_shopping_for_coop(coop)
    coop_upper = database.get_upper_coop(coop)
    # html = flask.render_template('templates/list.html',
    #         items=items, coop=coop, coop_upper=coop_upper)
    html_code = flask.render_template('templates/list.html', coop=coop, coop_upper=coop_upper)
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/list/delete', methods=['POST'])
def list_delete():
    ''' 
        Deletes a shift from the shopping list of the co-op 
        in the specified route.                     
    '''
    item_id = flask.request.args.get('id')
    database.delete_item(item_id)
    return ''

#----------------------------------------------------------------------

@app.route('/<coop>/items', methods=['GET'])
def items(coop):
    print("GET request for items")
    items = database.get_shopping_for_coop(coop)
    for item in items:
            print(item.item_name)

    # with open("templates/list_table.html") as f:
    #     raw_lines = f.readlines()
    # html_code = ''.join(raw_lines) # str

    # create HTML code
    html_code = (
        '<table class="table" id="myTable" style="margin: 0;">'
        )
    
    html_code += ('<thead id="theader">')
    html_code += ('<tr><th scope="col">Item</th><th scope="col">Type</th>'
                '<th scope="col">Qty</th><th scope="col">Comments</th>'
                '<th scope="col">Alt Item</th><th scope="col">For Shift?</th>'
                '<th scope="col">Ordered?</th><th scope="col"> </th></tr>')
    html_code += ('</thead><tbody id="tbody">')
    
    for item in items:
        html_code += '<tr>'
        html_code += ('<th scope="row">{0}</th>'
                    '<td>{1}</td>'
                    '<td>{2}</td>'
                    '<td>{3}</td>'
                    '<td>{4}</td>').format(item.item_name,
                                        item.item_type,
                                        item.item_quantity,
                                        item.item_reason,
                                        item.alt_request
                                        )
        if item.for_shift is True:
            for_shift = "Yes"
        else:
            for_shift = "No"
        html_code += ('<td>{0}</td>').format(for_shift)
        html_code += ('<td><div class="form-check">'
        '<input class="form-check-input" type="checkbox" value="" id="order-check">')
        if item.item_ordered is True:
            ordered = "Yes"
        else:
            ordered = "No"
        html_code += ('<label class="form-check-label" for="order-check">{0}</label>').format(ordered)
        html_code += ('</div></td>')
        html_code += ('<td><button type="button" class="btn btn-secondary btn-sm" id="rm-btn">Remove</button></td>')
        # '<label class="form-check-label" for="order-check">{1}</label>'
        # '</div></td>').format(item.item_ordered)

                        # <td>
                        #   <div class="form-check">
                        #     <input class="form-check-input" type="checkbox" value="" id="order-check">
                        #     <label class="form-check-label" for="order-check">
                        #       {{item.item_ordered}}
                        #     </label>
                        #   </div>
                        # </td>
                        # <td>
                        #   <button type="button" class="btn btn-secondary btn-sm" id="rm-btn">Remove</button>
                        # </td>
        html_code += '</tr>'

        # if item.for_shift == True:
        #     for_shift = True
    
    # html_code += '</table>'

    # item_json = []
    # for item in items: 
        # data = {}
        # data['item_id'] = item.item_id
        # data['item_name'] = item.item_name

        # extendedProps = {}
        # extendedProps['item_type'] = item.item_type
        # extendedProps['item_quanitty'] = item.item_quantity
        # extendedProps['for_shift'] = item.for_shift
        # extendedProps['item_reason'] = item.item_reason
        # extendedProps['requesting_user'] = item.requesting_user
        # extendedProps['food_type'] = item.food_type
        # extendedProps['alt_request'] = item.alt_request
        # data['extendedProps'] = extendedProps

        # item_json.append(data)
    # return jsonify(item_json)
    html_code += ('</tbody></table>')
    response = flask.make_response(html_code)
    return response

#----------------------------------------------------------------------
# Co-Op Profile
#----------------------------------------------------------------------

@app.route('/<coop>/profile', methods=['GET'])
def profile(coop):
    netid = auth.authenticate()
    user = database.get_user(netid)
    coop_upper = database.get_upper_coop(coop)
    html = flask.render_template('templates/profile.html',
            coop=coop, coop_upper=coop_upper, user=user)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------

@app.route('/<coop>/profile/update', methods=['POST'])
def update_profile(coop):
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
    return ''
