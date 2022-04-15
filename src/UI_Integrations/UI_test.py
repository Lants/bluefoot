# Before running, set env variables:
# export FLASK_APP=UI.py
# export FLASK_DEBUG=1 for true, 0 for false
# [Navigate to bluefoot/src/UI_Integrations]
# flask run

# Now you can pull up localhost:5000 in your browser to view the webpage. Refresh to see changes.

# Note: DO NOT SET DEBUG MODE IF DEPLOYING PUBLICLY!!! ---------------------------------------------------
#   Debug mode allows for arbitrary code executions from the deployed site. log4j flashbacks...

# Disclaimer: A majority of this boilerplate was written alongside the YouTube tutorials by Corey Schafer

from flask import Flask, render_template, url_for
from turbo_flask import Turbo
from datetime import datetime, timedelta
from time import sleep
import threading

app = Flask(__name__)
turbo = Turbo(app)

def test_url(self):
    with app.app_context(), app.test_request_context():
        self.assertEqual('/', url_for('root.home'))

test_data = [
    {
        'id': 0,
        'content': 'data 0'
    },
    {
        'id': 1,
        'content': 'data 1'
    }
]


@app.route("/")
@app.route("/home")
@app.route("/index.html")
def home():
    return render_template("home.html")


@app.route("/smol")
def smol():
    return render_template("smol.html", test_data=test_data)

@app.route("/chungus")
def chungus():
    
    return render_template("chungus.html")

@app.route("/Upload")
def upload():

    return render_template("upload.html")

@app.route("/spotify")
def spotify():

    return render_template("spotify.html")

@app.route("/about")
def about():

    return render_template("about.html")


@app.context_processor
def inject_load():
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
        # NOTE: You must move time_elapsed to the inject_load function below for dynamic updates
        }
]

    # Add dictionaries for dynamic data here

    dynamic_vars['chungus_current_time'] = datetime.now().strftime("%H:%M:%S")
    dynamic_vars['spotify_data'] = spotify_data

    return dynamic_vars

def update_load():
    with app.app_context():
        while True:
            sleep(1)
            turbo.push(turbo.replace(render_template('chungus_display_1.html'), 'display-1')) # look into the "to" argument for client-specific updates

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()



# if __name__ == '__main__':
#     app.run(debug=True)
