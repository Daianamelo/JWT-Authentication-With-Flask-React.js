from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Usuario(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     nombre = db.Column(db.String(250), nullable=False)
     apellido = db.Column(db.String(250), nullable=False)
     email = db.Column(db.String(250), nullable=False)

def __repr__(self):
        return '<Usuario %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido":self.apellido,
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250), nullable=False)
     climate = db.Column(db.String(250), nullable=False)
     gravity = db.Column(db.String(250), nullable=False)

def __repr__(self):
        return '<Planetas %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity":self.gravity,
            # do not serialize the password, its a security breach
        }

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    length = db.Column(db.String(250), nullable=False)

def __repr__(self):
        return '<Vehiculos %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "length":self.length,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.String(250), nullable=False)

def __repr__(self):
        return '<Personajes %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "homeworld":self.homeworld,
            # do not serialize the password, its a security breach
        }

class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id= db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personajes_id= db.Column(db.Integer, db.ForeignKey('personajes.id'))
    planetas_id= db.Column(db.Integer, db.ForeignKey('planetas.id'))
    vehiculos_id= db.Column(db.Integer, db.ForeignKey('vehiculos.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id,
            "vehiculos_id":self.vehiculos_id,
            # do not serialize the password, its a security breach
        }