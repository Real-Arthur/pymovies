from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
password = os.environ.get("password")

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{password}@localhost/cast_watch'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# init marshmallow
mv = Marshmallow(app)


# Movie class
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True)
    overview = db.Column(db.String(2000))
    release_date = db.Column(db.String(12))
    poster_path = db.Column(db.String(60))

    def __init__(self, title, overview, release_date, poster_path):
        self.title = title
        self.overview = overview
        self.release_date = release_date
        self.poster_path = poster_path


# User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(1000))

    def __init__(self, username, password):
        self.username = username
        self.password = password


# User_Movie class
class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id


# Movie Schema
class MovieSchema(mv.Schema):
    class Meta:
        fields = ('id', 'title', 'overview', 'release_date', 'poster_path')

# User Schema
class UserSchema(mv.Schema):
    class Meta:
        fields = ('id', 'username')

# User_Movie Schema
class UserMovieSchema(mv.Schema):
    class Meta:
        fields = ('id', 'user_id', 'movie_id')


# Init schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
# user_movie_schema = UserMovieSchema()
user_movie_schema = UserMovieSchema(many=True)


# Create a Movie
@app.route('/movies', methods=['POST'])
def add_movie():
    title = request.json['title']
    overview = request.json['overview']
    release_date = request.json['release_date']
    poster_path = request.json['poster_path']
    new_movie = Movie(title, overview, release_date, poster_path)
    db.session.add(new_movie)
    db.session.commit()
    return user_movie_schema.jsonify(new_movie)


# Create new User
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


# Add a movie to the user's collection
@app.route('/library/<userId>', methods=['POST'])
def add_to_collection(userId):
    movie_id = request.json['movie_id']
    user_id = int(userId)
    new_entry = UserMovie(user_id, movie_id)
    db.session.add(new_entry)
    db.session.commit()
    return user_movie_schema.dump(new_entry)


# Get all Movies
@app.route('/movies', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    print(all_movies)
    result = movies_schema.dump(all_movies)
    print(result)
    return jsonify(result)


# Get all Users
@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    print(all_users)
    result = users_schema.dump(all_users)
    print(result)
    return jsonify(result)


# Get one user
@app.route('/user/<userId>', methods=['GET'])
def get_user(userId):
    user = User.query.get(userId)
    return user_schema.jsonify(user)


# All movies by user Id 
@app.route('/library/<userId>', methods=['GET'])
def get_user_movies(userId):
    all_movies = UserMovie.query.filter(UserMovie.user_id == text(userId)).all()
    print(all_movies)
    return user_movie_schema.jsonify(all_movies)


# # Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#     product = Product.query.get(id)
#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']
#     product.name = name
#     product.description = description
#     product.price = price
#     product.qty = qty
#     db.session.commit()
#     return product_schema.jsonify(product)


# # Delete Products
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#     product = Product.query.get(id)
#     db.session.delete(product)
#     db.session.commit()
#     return product_schema.jsonify(product)


# run server
if __name__ == '__main__':
    app.run(debug=True)
