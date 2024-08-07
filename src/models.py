from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    favorite = db.relationship('Favorite', backref='user', uselist=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def serialize_fav(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": list(map(lambda item: item.serialize(), self.favorite))
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    favorite = db.relationship('Favorite', backref='people', uselist=True)

    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    favorite = db.relationship('Favorite', backref='planet', uselist=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)
    planet_id =  db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)

   
    def serialize(self):
        return {
            "user_id":self.user_id,
            "planet_id":self.planet_id,
            "people_id":self.people_id
        }