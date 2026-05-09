from flask import Flask,jsonify
from models import db
from flask_jwt_extended import JWTManager
from routes.auth_route import auth_bp
from routes.notes_routes import note_bp
from routes.tag_routes import tag_bp
from datetime import timedelta
import os
import logging

logging.basicConfig(level=logging.INFO)

def createAapp():
     
     app = Flask(__name__)
  # 🔐 Config (env-based with fallback)
     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL", "sqlite:///notes.db"
    )
     
     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # saves memory
     app.config['JWT_SECRET_KEY'] = os.environ.get(
        "JWT_SECRET_KEY", "dev-secret"
     )
     app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

     db.init_app(app)
     JWTManager(app)

     app.register_blueprint(auth_bp, url_prefix = '/api/auth')
     app.register_blueprint(note_bp, url_prefix = '/api/notes')
     app.register_blueprint(tag_bp, url_prefix = '/api/tags')

     @app.errorhandler(404)
     def not_found(e):
          return jsonify({'error':'Endpoint not found'}),404
      
     # 🛢️ Create tables
     with app.app_context():
          db.create_all()

     return app

# 🔹 Create app instance
app = createAapp()

# 🔹 Run locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host="0.0.0.0", port=port)
