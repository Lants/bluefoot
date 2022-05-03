# Before running, set env variables:
# export FLASK_APP=UI.py
# export FLASK_DEBUG=1 for true, 0 for false
# [Navigate to bluefoot/src/UI_Integrations]
# flask run

# Now you can pull up localhost:5000 in your browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site. log4j flashbacks...

# Disclaimer: A majority of this boilerplate was written alongside the YouTube tutorials by Corey Schafer

from flask import Flask, render_template, url_for, flash, request, redirect, session
from flask_mysqldb import MySQL
from turbo_flask import Turbo
from datetime import datetime, timedelta
from time import sleep
import threading
import MySQLdb.cursors
import re

#app.secret_key = 'secret'

#URL = "http://localhost:9090"

#PARAMS = {'username': test,
#         'password': password}

#r = requests.get(url=URL, params = PARAMS);

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123qweasdzxc'
app.config['MYSQL_DB'] = 'bluefoot'

mysql = MySQL(app)

# WHEN DEPLOYING PUBLICLY, GENERATE A NEW ONE AND MAKE IT AN ENVIRONMENT VARIABLE OR SOMETHING INSTEAD,
#   OTHERWISE THIS KEY IS USELESS FOR PREVENTING SECURITY RISKS
app.config['SECRET_KEY'] = '1c54243c5e2a20c2fbcccee5f28ff349'
turbo = Turbo(app)

def test_url(self):
    with app.app_context(), app.test_request_context():
        self.assertEqual('/', url_for('root.home'))

test_data = [
    {
        'id': 0,
        'content': 'N/A'
    },
    {
        'id': 1,
        'content': 'data 1'
    }
]

preset = {'id': 1}

# Home page route
@app.route("/")
@app.route("/home")
@app.route("/index.html")

def home():
    return render_template("drawing-text.html")

# smol page route
@app.route("/smol", methods=['POST', 'GET'])
def smol():
    if request.method == 'POST':
        if request.form['On-Off Button'] == 'on':
            print("smol: On button pressed")
            test_data[0]['content'] = 'ON'
            turbo.push(turbo.replace(render_template('smol_button_status.html'), 'button_status'))
        elif request.form['On-Off Button'] == 'off':
            print("smol: Off button pressed")
            test_data[0]['content'] = 'OFF'
            turbo.push(turbo.replace(render_template('smol_button_status.html'), 'button_status'))
    
    return render_template("smol.html", title='smol')



# Chungus page route
@app.route("/chungus", methods=['POST', 'GET'])
def chungus():
    if request.method == 'POST':
        if request.form['display-preset'] == '1':
            preset['id'] = 1
            print("Preset 1")
            turbo.push(turbo.replace(render_template('preset_conditionals.html'), 'display-presets'))
        elif request.form['display-preset'] == '2':
            preset['id'] = 2
            print("Preset 2")
            turbo.push(turbo.replace(render_template('preset_conditionals.html'), 'display-presets'))
    return render_template("chungus.html", title='Chungus')

@app.route("/logerror", methods=['POST', 'GET'])
def logerror():
    return render_template('logerror.html')

@app.route("/regerror", methods=['POST', 'GET'])
def regerror():
    return render_template('regerror.html')

@app.route("/regsuc", methods=['POST', 'GET'])
def regsuc():
    return render_template('regsuc.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    #error = ''
    #if request.method == 'POST':
    #    if request.form['username'] != 'Bluefoot' or request.form['password'] != 'admin':
    #        error = 'Invalid credentials. Please try again!'
    #    else:
    #        return redirect(url_for('smol'))
    #return render_template("login_ming.html", title='login', error = error)
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            #return render_template('index.html', msg = msg)
            return redirect(url_for('smol'))
        else:
            return redirect(url_for('logerror'))
    return render_template('login_ming_2.html')


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            return redirect(url_for('regerror'))
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s)', (username, password, ))
            mysql.connection.commit()
            return redirect(url_for('regsuc'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register_ming_2.html', msg = msg)


# Set global data (be careful... this is necessary for avoiding javascript,
#   but global variables can be dangerous/messy)
@app.context_processor
def inject_data():
    dynamic_vars = {}

    # For Spotify, retrieve data and format it something like this:
    # spotify_API_retrieve = Spotify.retrieve() ... blablabla
    spotify_data = [
        {
        'title': 'Never Gonna Give You Up',
        'artist': 'Rick Astley',
        'album': 'Whenever You Need Somebody',
        'time_elapsed': str(timedelta(seconds=72)), # Replace 72 with spotify_API_retrieve.song_length or whatever
        'length': str(timedelta(seconds=212)), # Replace 212 with however many seconds long the song is
        }
]

    # Add dictionaries entries for dynamic data here
    dynamic_vars['chungus_current_time'] = datetime.now().strftime("%H:%M:%S")
    dynamic_vars['spotify_data'] = spotify_data
    dynamic_vars['test_data'] = test_data
    dynamic_vars['preset'] = preset

    return dynamic_vars

# Visually update chungus's display 1. Call from separate
#   thread in before_first_request(), as this runs in an infinite loop.
def update_chungus_d1():
    with app.app_context():
        while True:
            sleep(1)
            turbo.push(turbo.replace(render_template('chungus_display_1.html'), 'display-1')) # look into the "to" argument for client-specific updates



@app.before_first_request
def before_first_request():
    threading.Thread(target=update_chungus_d1).start()



# if __name__ == '__main__':
#     app.run(debug=True)