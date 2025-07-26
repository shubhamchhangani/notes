from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()
auth_bp = Blueprint('auth', __name__)

def get_db():
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB")
    )

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        db.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except MySQLdb.IntegrityError:
        return jsonify({"msg": "User already exists"}), 400
    finally:
        db.close()

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if user and check_password_hash(user[1], password):
        user_id = str(user[0])  # ✅ force it to string!
        print("Creating token for user_id:", user_id)
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401