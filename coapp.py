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
    print("brown calendar")

# Brown Roster
@app.route('/brown/roster', methods=['GET'])
def brown_roster():
    print("brown roster")

# Brown Shopping List
@app.route('/brown/list', methods=['GET'])
def brown_list():
    print("brown list")
    

#----------------------------------------------------------------------