from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint("profile", __name__)

# GET the user's profile
@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "full_name": user.full_name,
        "location": user.location
    }), 200

# UPDATE the user's profile
@profile_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.full_name = data.get("full_name", user.full_name)
    user.location = data.get("location", user.location)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200