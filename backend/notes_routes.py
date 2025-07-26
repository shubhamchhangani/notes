from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()
notes_bp = Blueprint('notes', __name__)

def get_db():
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        passwd=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB")
    )

@notes_bp.route('/api/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = int(get_jwt_identity())  # cast back to int
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, content, created_at FROM notes WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()
    db.close()
    return jsonify([{"id": n[0], "title": n[1], "content": n[2], "created_at": n[3].isoformat()} for n in notes])

@notes_bp.route('/api/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = int(get_jwt_identity())  # cast back to int
    data = request.get_json()
    title = data['title']
    content = data['content']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)",
                   (user_id, title, content))
    db.commit()
    db.close()
    return jsonify({"msg": "Note created successfully"}), 201

@notes_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = int(get_jwt_identity())  # cast back to int
    data = request.get_json()
    title = data['title']
    content = data['content']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE notes SET title=%s, content=%s WHERE id=%s AND user_id=%s",
                   (title, content, note_id, user_id))
    db.commit()
    db.close()
    return jsonify({"msg": "Note updated"}), 200

@notes_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = int(get_jwt_identity())  # cast back to int
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM notes WHERE id=%s AND user_id=%s", (note_id, user_id))
    db.commit()
    db.close()
    return jsonify({"msg": "Note deleted"}), 200