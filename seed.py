"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import Users, Ratings, Movies, connect_to_db, db
from server import app
import datetime
from datetime import datetime

def load_users():
    """Load users from u.user into database."""
    User_file = open('seed_data/u.user')
    
    for line in User_file:
        line.strip()
        row = line.split('|')
        # user_id = row[0]
        email = 'Null'
        password = 'Null'
        age = row[1]
        zip_code = row[4]

        user = Users(email= email, 
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
        # movie_id = row[0]
        movie_title = row[1]
        if "(" in movie_title:
            movie_title = movie_title[:-6]

        date = row[2]
        if len(date) > 1:
            release_date = datetime.strptime(date, '%d-%b-%Y')
        else:
            release_date = datetime.strptime("01-JAN-1000", '%d-%b-%Y')  
        IMDB_URL = row[3]

        

        movie = Movies(movie_title=movie_title,
                     release_date=release_date, IMDB_URL=IMDB_URL)

        db.session.add(movie) 
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""
    Ratings_file = open('seed_data/u.data')
    
    for line in Ratings_file:
        line.strip()
        row = line.split('\t')
        # ratings_id = 1
        movie_id = row[0]
        user_id = row[1]
        score = row[2]
        
        rate = Ratings(movie_id=movie_id, 
            user_id=user_id, score=score)

        db.session.add(rate) 
    db.session.commit() 

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_users()
    load_movies()
    load_ratings()