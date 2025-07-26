from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from auth_routes import auth_bp
from notes_routes import notes_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'fallbackkey'
app.config['JWT_IDENTITY_CLAIM'] = 'sub'  # This ensures "sub" is used

jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(notes_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')