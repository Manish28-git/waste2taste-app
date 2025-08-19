# routes/auth.py

from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
# Import JWT functions
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# ... (your /register route stays the same) ...
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Add 'role' to the required fields check
    if not all(key in data for key in ["username", "email", "password", "role"]):
        return jsonify({"error": "Username, email, password, and role are required"}), 400

    # Validate the role
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
        role=role  # Set the user's role
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
        # Create a token! The "identity" is the data we store in the token.
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200 # Return the token
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# NEW PROTECTED ROUTE FOR TESTING
@auth_bp.route("/profile", methods=["GET"])
@jwt_required() # This decorator protects the route
def profile():
    # We can get the user's ID from the token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user:
        return jsonify(id=user.id, username=user.username, email=user.email), 200
    else:
        return jsonify({"error": "User not found"}), 404