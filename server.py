"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

import sqlite3

db_connection = sqlite3.connect("ratings.db", check_same_thread=False)
db_cursor = db_connection.cursor()

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/login_form')
def login():
    """shows login form"""

    return render_template("login_form.html")

@app.route('/login_submit')
def login_submit():
    email = request.args.get("email")
    password = request.args.get("password")

    current_users = User.query.filter_by(email=email).all()
    
    if email in current_users:
        response = "yes"
    else:
        response = "no"
        #SQL Statement entering user info
        user = User(email= email, 
                    password= password)

        db.session.add(user) 
        db.session.commit()
               

    # if user_id:
    #     session['user_id'] = user_id

    return  render_template("test.html", email=email, password=password, 
        current_users=current_users, response=response)   

    # $('#email').on
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()