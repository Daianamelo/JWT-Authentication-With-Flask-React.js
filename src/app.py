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
from models import db, User, Usuario, Personajes, Planetas, Vehiculos, Favoritos
#from models import Person
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#aca empiezan los endpoints
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    print(user)
    
    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401
    # return jsonify({"msg": "ok"}), 200


    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


    # Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity

    
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    print(user.serialize())
    return jsonify({"msg":"ok", "user":user.serialize()}), 200

@app.route("/cuenta", methods=["GET"])
@jwt_required()
def get_cuenta():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()
    print(user.serialize())
    response_body = {"user":user.serialize()}

    return jsonify(response_body), 200 


    @app.route("/cuenta", methods=["GET"])
    @jwt_required()
    def get_cuenta():
    # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).first()
    print(user.serialize())
    response_body = {"user":user.serialize()}

    return jsonify(response_body), 200 




#consulta user todos
@app.route('/user', methods=['GET'])
def handle_hello():
    allusers=User.query.all()
    print(allusers)
    results=list(map(lambda item: item.serialize(),allusers))
    # print(results)
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(results), 200

#personajes
@app.route('/personajes', methods=['GET'])
def get_personajes():
    all_personajes= Personajes.query.all()
    results = list(map(lambda item: item.serialize(),all_personajes))

    return jsonify(results), 200

#solo un personaje
@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def select_personajes(personajes_id):
    personaje = Personajes.query.filter_by(id=personajes_id).first()
    return jsonify(personajes_id), 200



#consulta individual user

@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    # print(user_id)
    #peter = User.query.filter_by(username='peter').first()
    user= User.query.filter_by(id=user_id).first()
    # print(user.serialize())
    # allusers=User.query.all()
    # print(allusers)
    # results=list(map(lambda item: item.serialize(),allusers))
    # print(results)
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    return jsonify(user.serialize()), 200

    #consulta planetas
#1)cambiar por el nombre que necesito y fijarme si va get o otra cosa
@app.route('/Planetas', methods=['GET'])
def info_planetas():
    allplanetas=Planetas.query.all()
    results=list(map(lambda item: item.serialize(),allplanetas))
    response_body = {
        "msg": "Hello, this is your GET /planet response "
    }
    return jsonify(planetas.serialize()), 200

    # solo 1
    @app.route('/planetas/<int:planetas_id>', methods=['GET'])
    def select_planetas(planetas_id):
        planetas = Planetas.query.filter_by(id=planetas_id).first()
    return jsonify(planetas_id), 200

#vehiculos
    #consulta planetas
#1)cambiar por el nombre que necesito y fijarme si va get o otra cosa
@app.route('/Vehiculos', methods=['GET'])
def info_vehiculos():
    allvehiculos=Vehiculos.query.all()
    results=list(map(lambda item: item.serialize(),allvehiculos))
    response_body = {
        "msg": "Hello, this is your GET /vehiculos response "
    }
    return jsonify(Vehiculos.serialize()), 200

    # solo 1
    @app.route('/vehiculos/<int:vehiculos_id>', methods=['GET'])
    def select_vehiculos(vehiculos_id):
        vehiculos = Vehiculos.query.filter_by(id=vehiculos_id).first()
    return jsonify(vehiculos_id), 200



#los favoritos
@app.route('/usuario/<int:usuario_id>/favoritos', methods=['POST'])
def add_planetas_favoritos(usuario_id):
        request_body = request.json
        print(request_body)
        print(request_body["planetas_id"]) 
        new_favoritos= Favoritos(usuario_id = usuario_id,personajes_id= None, vehiculos_id= None, planetas_id= request_body['planetas_id']) 
        favoritos= Favoritos.query.filter_by(usuario_id = usuario_id, planetas_id= request_body['planetas_id']).first()
        print(favoritos)

        if favoritos is None:
            new_favoritos= Favoritos(usuario_id = usuario_id,personajes_id= None, vehiculos_id= None, planetas_id= request_body['planetas_id'] ) 
            db.session.add(new_favoritos)
            db.session. commit()

            return jsonify({'msg':'se agrego favorito'}), 200

        return jsonify({'msg':'se quito favortio'}), 400

@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['POST'])
def add_personajes_favoritos(usuario_id):

    request_body = request.json
    print(request_body)
    print(request_body['personajes_id'])

    new_favoritos_personajes = Favoritos(usuario_id = usuario_id, personajes_id = request_body['personajes_id'], vehiculos_id = None, planetas_id = None)

    favoritos = Favoritos.query.filter_by(usuario_id=usuario_id, personajes_id=request_body['personajes_id']).first()
    print(favoritos)

    if favoritos is None:
        new_favoritos_personajes = Favoritos(usuario_id = usuario_id, personajes_id = request_body['personajes_id'], vehiculos_id = None, planets_id = None)
        db.session.add(new_favoritos_personajes)
        db.session.commit()

        return jsonify({'msg': 'favorito agregado'}), 200    

    return jsonify({'msg': 'favorito existe'}), 400




#terminan endpoints
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
