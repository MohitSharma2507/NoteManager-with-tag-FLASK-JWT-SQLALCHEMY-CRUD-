from flask import Flask,Blueprint
from models import db
from flask_jwt_extended import JWTManager
from routes.auth_route import auth_bp
from routes.notes_routes import note_bp
from routes.tag_routes import tag_bp

def createAapp():
     
     app = Flask(__name__)

     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
     app.config['JWT_SECRET_KEY'] = 'supersecret-key'
     app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

     db.init_app(app)
     JWTManager(app)

     app.register_blueprint(auth_bp, url_prefix = '/api')
     app.register_blueprint(note_bp, url_prefix = '/api')
     app.register_blueprint(tag_bp, url_prefix = '/api')

     return app

app = createAapp()

if '__main__' == __name__:
     with app.app_context():
          db.create_all()
     app.run(debug=True, port=8000)

     


