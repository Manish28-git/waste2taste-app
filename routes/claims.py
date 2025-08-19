# routes/claims.py
from flask import Blueprint, jsonify
from extensions import db
from models.post import Post
from models.claim import Claim
from flask_jwt_extended import jwt_required, get_jwt_identity

claims_bp = Blueprint("claims", __name__)

@claims_bp.route("/posts/<int:post_id>/claim", methods=["POST"])
@jwt_required()
def claim_post(post_id):
    current_user_id = get_jwt_identity()

    post = Post.query.get(post_id)

    # Check if the post exists
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Check if the user is trying to claim their own post
    if str(post.donor_id) == current_user_id:
        return jsonify({"error": "You cannot claim your own post"}), 403

    # Check if the post is already claimed
    if Claim.query.filter_by(post_id=post_id).first():
        return jsonify({"error": "This post has already been claimed"}), 409 # 409 Conflict

    # Create the new claim
    new_claim = Claim(
        post_id=post_id,
        receiver_id=current_user_id
    )

    db.session.add(new_claim)
    db.session.commit()

    return jsonify({"message": f"Post {post_id} successfully claimed"}), 200

@claims_bp.route("/claims/my-claims", methods=["GET"])
@jwt_required()
def get_my_claims():
    current_user_id = get_jwt_identity()

    # Find all claims by the current user and join with the Post table to get post details
    user_claims = db.session.query(Claim, Post).join(Post, Claim.post_id == Post.id).filter(Claim.receiver_id == current_user_id).order_by(Claim.claim_time.desc()).all()

    claims_list = []
    for claim, post in user_claims:
        claims_list.append({
            "claim_id": claim.id,
            "post_id": post.id,
            "food_name": post.food_name,
            "location": post.location,
            "claim_time": claim.claim_time.isoformat()
        })

    return jsonify(claims_list), 200