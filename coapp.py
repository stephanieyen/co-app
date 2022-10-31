import flask
import database
import json

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
@app.route('/<coop>', methods=['GET'])
@app.route('/<coop>/calendar', methods=['GET'])
def calendar(coop):
    # TO-DO: convert shifts to JSON for calendar API  
    shifts = database.get_shifts_for_coop(coop)
    event_json = []
    for shift in shifts: 
        data = {}
        data['start'] = shift.shift_time
        data['title'] = shift.shift_name
        data['type'] = shift.shift_type
        data['members'] = shift.shift_members
        event_json.append(data)

    html_code = flask.render_template('calendar_initialize.html', events=event_json, coop=coop)
    response = flask.make_response(html_code)
    return response

# Co-op Roster
@app.route('/<coop>/roster', methods=['GET'])
def roster(coop):
    members = database.get_roster_for_coop(coop)
    html = flask.render_template('roster.html', members=members, coop=coop)
    response = flask.make_response(html)
    return response

# Co-op Shopping List
@app.route('/<coop>/list', methods=['GET'])
def list(coop):
    items = database.get_shopping_for_coop(coop)
    print(items)
    html = flask.render_template('shoppinglist.html', items=items, coop=coop)
    response = flask.make_response(html)
    return response

#----------------------------------------------------------------------