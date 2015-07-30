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

    current_users = db.session.query(User.email).filter_by(email=email, password=password).all()
    
    if len(current_users) >= 1:
        session_id = email
        
    else:
        if len(db.session.query(User.email).filter_by(email=email).all()) >= 1:
            
            return redirect('/login_form')

        else:
            
            #SQL Statement entering user info
            user = User(email= email, 
                    password= password)

            db.session.add(user) 
            db.session.commit()
            session_id = email
               

    if session_id:
        session['user_id'] = session_id
        user_id = db.session.query(User.user_id).filter_by(email=email).one()
        print user_id
        flash('You are logged in')

    return redirect('/users/' + str(user_id[0]))

@app.route('/logout')
def log_out():

    session.clear()
    flash('You are logged out.')
    return redirect('/')       

@app.route('/users/<int:id>')
def userinfo(id):

    user_info = User.query.filter_by(user_id = id).one()
    
    rating_list = db.session.query(Rating.score,
                                   Rating.movie_id,
                                   Movie.movie_title).join(Movie).filter(Rating.user_id == id).all()
    
    return render_template("user_info.html", user=user_info, movies_rated=rating_list)

@app.route('/movies')
def movies_list():
    """Show list of movies."""

    movies = Movie.query.all()
    return render_template("movies_list.html", movies=movies)

@app.route('/movies/<int:id>')
def movieinfo(id):

    movie_info = Movie.query.filter_by(movie_id = id).one()
    
    rating_list = db.session.query(Rating.score,
                                   Rating.user_id).filter(Rating.movie_id == id).all()

    return render_template('movie_info.html', movie=movie_info, movies_rated=rating_list)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()