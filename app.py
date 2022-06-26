# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource
from classes.Serialize import Serialize
import classes.Schemas as Schemas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movies_ns.route("/")
class MoviesDraw(Resource):
    def get(self):
        try:
            if request.values.get('director_id') is not None and request.values.get('genre_id') is not None:
                director_id = int(request.values.get('director_id'))
                genre_id = int(request.values.get("genre_id"))
                movies_serialize = Serialize(Schemas.MovieSchema)
                with db.session.begin():
                    query = db.session.query(Movie).filter(Movie.director_id == director_id,
                                                           Movie.genre_id == genre_id).all()
                result = movies_serialize.serialize(query)
                if result == []:
                    return jsonify({"Error": "Фильмов с такими актёрами и жанрами не было найдено"})
                return jsonify(result)
            elif request.values.get('director_id') is not None:
                req_id = int(request.values.get('director_id'))
                movies_serialize = Serialize(Schemas.MovieSchema)
                with db.session.begin():
                    query = db.session.query(Movie).filter(Movie.director_id == req_id).all()
                result = movies_serialize.serialize(query)
                if result == []:
                    return jsonify({"Error": "Фильмов с такими актёрами не было найдено"})
                return jsonify(result)
            elif request.values.get('genre_id') is not None:
                req_id = int(request.values.get('genre_id'))
                movies_serialize = Serialize(Schemas.MovieSchema)
                with db.session.begin():
                    query = db.session.query(Movie).filter(Movie.genre_id == req_id).all()
                result = movies_serialize.serialize(query)
                if result == []:
                    return jsonify({"Error": "Фильмов с таким жанром не нашлось"})
                return jsonify(result)
            else:
                movies_serialize = Serialize(Schemas.MovieSchema)
                result = movies_serialize.serialize_all(Movie())
                return jsonify(result)
        except:
            return jsonify({"Error": "Индекс должен содержать только цифры"})

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return '{"Answer": "Фильм успешно добавлен"}', 201


@movies_ns.route("/<int:pk>")
class MoviesDraw(Resource):
    def get(self, pk):
        try:
            movies_serialize = Serialize(Schemas.MovieSchema)
            result = movies_serialize.serialize_get(Movie, pk)
            if result == {}:
                return jsonify({"Error": "Такого фильма не существует"})
        except:
            return jsonify({"Error": "Индекс должен содержать только цифры"})
        else:
            return jsonify(result)

    def delete(self, pk):
        movie = Movie.query.get(pk)
        db.session.delete(movie)
        db.session.commit()
        db.session.close()
        return '{"Answer": "Фильм успешно удалён"}', 200


@director_ns.route("/")
class DirectorsDraw(Resource):
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return '{"Answer": "Актёр успешно добавлен"}', 201


@director_ns.route("/<int:pk>")
class DirectorsDraw(Resource):
    def put(self, pk):
        director = Director.query.get(pk)
        req_json = request.json
        director.name = req_json["name"]
        db.session.add(director)
        db.session.commit()
        db.session.close()
        return '{"Answer": "Актёр успешно изменён"}', 201

    def delete(self, pk):
        director = Director.query.get(pk)
        db.session.delete(director)
        db.session.commit()
        db.session.close()
        return '{"Answer": "Актёр успешно удалён"}', 200


@genre_ns.route("/")
class GenresDraw(Resource):
    def post(self):
        req_json = request.json
        new_genres = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genres)
        return '{"Answer": "Жанр успешно добавлен"}', 201


@genre_ns.route("/<int:pk>")
class GenresDraw(Resource):
    def put(self, pk):
        genre = Genre.query.get(pk)
        req_json = request.json
        genre.name = req_json["name"]
        db.session.add(genre)
        db.session.commit()
        db.session.close()
        return '{"Answer": "Жанр успешно изменён"}', 201

    def delete(self, pk):
        genre = Director.query.get(pk)
        db.session.delete(genre)
        db.session.commit()
        db.session.close()
        return '{"Answer": "Жанр успешно удалён"}', 200


if __name__ == '__main__':
    app.run(debug=True)
