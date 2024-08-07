"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Favorite, Planet
# import requests


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

    #lineas user

@app.route('/user', methods=['GET'])
def get_users():
    user = User()
    user = user.query.all()
    user = list(map(lambda item: item.serialize(), user))

    return jsonify(user), 200



    #lineas People

@app.route("/people", methods=["GET"])
def get_all_people():

    people = People()
    people = people.query.all()
    people = list(map(lambda item: item.serialize(), people))

    return jsonify(people), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_people(people_id):
    people = People()
    people = people.query.get(people_id)
    
    if people is None:
        raise APIException("People not found", status_code=404)
    else:
        return jsonify(people.serialize()), 200
    
     #lineas Planet

@app.route("/planet", methods=["GET"])
def get_all_planet():

    planet = Planet()
    planet = planet.query.all()
    planet = list(map(lambda item: item.serialize(), planet))

    return jsonify(planet), 200

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = Planet()
    planet = planet.query.get(planet_id)
    
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    else:
        return jsonify(planet.serialize()), 200

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_fav(people_id):
    user_id = 1

    fav = Favorite()
    fav.user_id = user_id
    fav.people_id = people_id
    
    db.session.add(fav)

    try:
        db.session.commit()
        return jsonify("success"), 201
    except Exception as error:
        db.session.rollback
        return jsonify("try again"), 201
    
    
@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_people_fav(people_id):
    user_id = 1

    fav = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    
    if fav:
        db.session.delete(fav)
        try:
            db.session.commit()
            return jsonify("se eliminó exitosamente"), 200
        except Exception as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 500
    else:
        return jsonify("favorito no encontrado"), 404
    
    #----------------
    

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_fav(planet_id):
    user_id = 1

    fav = Favorite()
    fav.user_id = user_id
    fav.planet_id = planet_id
    
    db.session.add(fav)

    try:
        db.session.commit()
        return jsonify("success"), 201
    except Exception as error:
        db.session.rollback
        return jsonify("try again"), 201
    
    
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet_fav(planet_id):
    user_id = 1

    fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    
    if fav:
        db.session.delete(fav)
        try:
            db.session.commit()
            return jsonify("se eliminó exitosamente"), 200
        except Exception as error:
            db.session.rollback()
            return jsonify({"error": str(error)}), 500
    else:
        return jsonify("favorito no encontrado"), 404
    




# @app.route("/people/population", methods=["GET"])
# def get_people_population():
#     response = requests.get("https://www.swapi.tech/api/people?page=1&limit=3")
#     response = response.json()
#     response = response.get("results")

#     for item in response:
#         result = requests.get(item.get("url")).json().get("result").get("properties")
#         people = People()
#         attributes = ["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender"]
        
#         for attr in attributes:
#             setattr(people, attr, result.get(attr))
#         db.session.add(people)

#     try:
#         db.session.commit()
#         return jsonify("populando listo"), 200
#     except Exception as error:
#         print(error)
#         db.session.rollback()
#         return jsonify("error"), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
