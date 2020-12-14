from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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




# Movie Schema
class MovieSchema(mv.Schema):
    class Meta:
        fields = ('id', 'title', 'overview', 'release_date', 'poster_path')


# Init schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


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
    return movie_schema.jsonify(new_movie)


# Get all Movies
@app.route('/movies', methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    result = movies_schema.dump(all_movies)
    return jsonify(result)


# # Get one product
# @app.route('/product/<id>', methods=['GET'])
# def get_product(id):
#     product = Product.query.get(id)
#     return product_schema.jsonify(product)


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
