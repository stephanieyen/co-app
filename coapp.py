import flask
import database

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
# Routes for Brown co-op

# Brown Calendar
@app.route('/calendar', methods=['GET'])
@app.route('/brown', methods=['GET'])
@app.route('/brown/calendar', methods=['GET'])
def brown_calendar():
    # TO-DO: convert shifts to JSON for calendar API  
    coop = 'Brown'
    shifts = database.get_shifts_for_coop(coop)

    html_code = flask.render_template('calendar_initialize.html')
    response = flask.make_response(html_code)
    return response

# Brown Roster
@app.route('/brown/roster', methods=['GET'])
def brown_roster():
    coop = 'Brown'
    members = database.get_roster_for_coop(coop)
    html = flask.render_template('roster.html', members=members)
    response = flask.make_response(html)
    return response

# Brown Shopping List
@app.route('/brown/list', methods=['GET'])
def brown_list():
    coop = 'Brown'
    items = database.get_shopping_for_coop(coop)
    print(items)
    html = flask.render_template('shoppinglist.html', items=items)
    response = flask.make_response(html)
    return response


#----------------------------------------------------------------------