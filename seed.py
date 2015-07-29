"""Utility file to seed ratings database from MovieLens data in seed_data/"""

# makes data tables and ancilary programs avaialable.
from model import User, Rating, Movie, connect_to_db, db
from server import app

from datetime import datetime

def load_users():
    """Load users from u.user into database."""
    User_file = open('seed_data/u.user')
    
    for line in User_file:
        # prepare line for reading data
        line.strip()
        row = line.split('|')
        #sets variables to correct data
        user_id = row[0]
        email = 'Null'
        password = 'Null'
        age = row[1]
        zip_code = row[4]

        user = User(user_id=user_id,
                    email= email, 
                    password= password, age=age, 
                    zipcode=zip_code[0:6])

        db.session.add(user) 
    db.session.commit()  
  

def load_movies():
    """Load movies from u.item into database."""
    Movie_file = open('seed_data/u.item')
    
    for line in Movie_file:
        line.strip()
        row = line.split('|')
        movie_id = row[0]
        movie_title = row[1]
        # finding movie titles with trailing dates in () and removing the year.
        if "(" in movie_title:
            movie_title = movie_title[:-7]

        date = row[2]
        # finding if there were instances 
        # where release date was null and accounting for them.
        if len(date) > 1:
            release_date = datetime.strptime(date, '%d-%b-%Y')
        else:
            release_date = None
        IMDB_URL = row[3]

        movie = Movie(movie_id = movie_id, movie_title=movie_title,
                     release_date=release_date, IMDB_URL=IMDB_URL)

        db.session.add(movie) 
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""
    Ratings_file = open('seed_data/u.data')
    
    for line in Ratings_file:
        line.strip()
        row = line.split('\t')
        # ratings_id = 1 - this is kept out so the database will create the id as info is added.
        movie_id = row[0]
        user_id = row[1]
        score = row[2]
        
        rate = Rating(movie_id=movie_id, 
            user_id=user_id, score=score)

        db.session.add(rate) 
    db.session.commit() 

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_users()
    load_movies()
    load_ratings()