
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    
    if not all(key in data for key in ["username", "email", "password", "role"]):
        return jsonify({"error": "Username, email, password, and role are required"}), 400

    
    role = data.get("role")
    if role not in ['donor', 'receiver']:
        return jsonify({"error": "Invalid role. Must be 'donor' or 'receiver'"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(
        username=data["username"],
        email=data["email"],
        role=role  
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User registered successfully as a {role}"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200 
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required() 
def profile():
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user:
        return jsonify(id=user.id, username=user.username, email=user.email), 200
    else:
        return jsonify({"error": "User not found"}), 404