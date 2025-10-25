"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, RevokedToken, Todos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from base64 import b64encode
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta, datetime, timezone
from sqlalchemy.exc import IntegrityError

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200


@api.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    # normalize and validate email
    email = (data.get("email") or "").strip().lower()
    data = {
        "email": email,
        "password": data.get("password"),
        "lastname": data.get("lastname"),
        "avatar": data.get("avatar", "https://i.pravatar.cc/300"),
        "is_active": True
    }

    if not data["email"] or not data["password"] or not data["lastname"]:
        return jsonify({"message": "Email, password, and lastname are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 409

    salt = b64encode(os.urandom(32)).decode('utf-8')
    password = generate_password_hash(data["password"] + salt)

    new_user = User(
        email=data["email"],
        password_hash=password,
        lastname=data["lastname"],
        avatar=data["avatar"],
        is_active=data["is_active"],
        salt=salt
    )
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating user", "error": str(e.args)}), 500


@api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    # normalize email for lookup
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).one_or_none()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 404

    if not check_password_hash(user.password_hash, password + user.salt):
        return jsonify({"message": "Invalid credentials"}), 401

    jti = os.urandom(16).hex()
    expires = timedelta(days=1)
    token = create_access_token(
        identity=str(user.id),
        expires_delta=expires,
        additional_claims={"jti": jti}
    )

    return jsonify({
        "token": token,
    }), 200


@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"This is a protected route. Current user ID: {current_user}"}), 200


@api.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200


@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    payload = get_jwt()

    jti = payload.get('jti')
    exp = payload.get('exp')  # timestamp en segundos

    if not jti or not exp:
        return jsonify({"message": "Token inválido, no se puede revocar"}), 400

    # convertir exp (timestamp) a datetime aware en UTC
    try:
        expires_at = datetime.fromtimestamp(int(exp), tz=timezone.utc)
    except Exception:
        return jsonify({"message": "Formato de 'exp' inválido en el token"}), 400

    revoked = RevokedToken(jti=jti, expires_at=expires_at)
    db.session.add(revoked)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        # Ya estaba revocado — tratamos como éxito (idempotente)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error revocando token", "error": str(e)}), 500

    return jsonify({"message": "Token revocado"}), 200


@api.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200


@api.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    current_user_id = get_jwt_identity()
    todos = Todos.query.filter_by(user_id=current_user_id).all()
    todos = {
        "todos": [todo.serialize() for todo in todos],
        "user_id": current_user_id
    }

    return jsonify(todos), 200


@api.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    label = data.get("label")
    if not label:
        return jsonify({"message": "Label is required"}), 400

    new_todo = Todos(
        label=label,
        is_done=False,
        user_id=current_user_id
    )
    db.session.add(new_todo)
    try:
        db.session.commit()
        return jsonify(new_todo.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating todo", "error": str(e)}), 500


@api.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    current_user_id = get_jwt_identity()
    todo = Todos.query.filter_by(
        id=todo_id, user_id=current_user_id).one_or_none()
    if not todo:
        return jsonify({"message": "Todo not found"}), 404

    data = request.get_json()
    label = data.get("label")
    is_done = data.get("is_done")

    if label is not None:
        todo.label = label
    if is_done is not None:
        todo.is_done = is_done

    try:
        db.session.commit()
        return jsonify(todo.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating todo", "error": str(e)}), 500


@api.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    current_user_id = get_jwt_identity()
    todo = Todos.query.filter_by(
        id=todo_id, user_id=current_user_id).one_or_none()
    if not todo:
        return jsonify({"message": "Todo not found"}), 404

    db.session.delete(todo)
    try:
        db.session.commit()
        return jsonify([]), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting todo", "error": str(e)}), 500
