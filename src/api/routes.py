"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from base64 import b64encode
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200


@api.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    data = {
        "email": data.get("email"),
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
        password=password,
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

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).one_or_none()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 404

    if not check_password_hash(user.password, password + user.salt):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "token": create_access_token(identity=str(user.id), expires_delta=timedelta(days=1)),
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
