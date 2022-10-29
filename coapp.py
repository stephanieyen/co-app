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
@app.route('/brown', methods=['GET'])
@app.route('/brown/calendar', methods=['GET'])
def brown_calendar():
    html_code = flask.render_template('calendar_initialize.html')
    response = flask.make_response(html_code)
    return response

# Brown Roster
@app.route('/brown/roster', methods=['GET'])
def brown_roster():
    print("brown roster")

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