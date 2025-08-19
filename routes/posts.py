# routes/posts.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.user import User
from models.claim import Claim

posts_bp = Blueprint("posts", __name__)

# PROTECTED ROUTE: Create a new food post
@posts_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id) # Get the user object

    # Check the user's role
    if not user or user.role != 'donor':
        return jsonify({"error": "Only donors are authorized to create posts"}), 403 # 403 Forbidden

    data = request.get_json()

    # ... (the rest of the function remains the same) ...
    if not all(key in data for key in ["food_name", "quantity", "location", "expiry_time"]):
        return jsonify({"error": "Missing required fields"}), 400

    # ... (rest of the function) ...
    try:
        expiry_datetime = datetime.fromisoformat(data["expiry_time"])
    except ValueError:
        return jsonify({"error": "Invalid expiry_time format. Use ISO format like YYYY-MM-DDTHH:MM:SS"}), 400

    new_post = Post(
        food_name=data["food_name"],
        description=data.get("description"),
        quantity=data["quantity"],
        location=data["location"],
        expiry_time=expiry_datetime,
        donor_id=current_user_id
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "post_id": new_post.id}), 201

# PUBLIC ROUTE: Get all available food posts
@posts_bp.route("/posts", methods=["GET"])
def get_all_posts():
    # 2. Query for posts that are not expired AND are not claimed
    available_posts = Post.query.outerjoin(Claim).filter(
        Post.expiry_time > datetime.utcnow(),
        Claim.id == None
    ).order_by(Post.post_time.desc()).all()
    
    post_list = []
    for post in available_posts:
        post_list.append({
            "id": post.id,
            "food_name": post.food_name,
            "description": post.description,
            "quantity": post.quantity,
            "location": post.location,
            "post_time": post.post_time.isoformat(),
            "expiry_time": post.expiry_time.isoformat(),
            "donor_id": post.donor_id
        })
        
    return jsonify(post_list), 200

@posts_bp.route("/posts/my-posts", methods=["GET"])
@jwt_required()
def get_my_posts():
    current_user_id = get_jwt_identity()

    # Query for posts created by the current user
    user_posts = Post.query.filter_by(donor_id=current_user_id).order_by(Post.post_time.desc()).all()

    post_list = []
    for post in user_posts:
        # Check if the post has been claimed to determine its status
        claim = Claim.query.filter_by(post_id=post.id).first()
        status = "Claimed" if claim else "Available"

        post_list.append({
            "id": post.id,
            "food_name": post.food_name,
            "quantity": post.quantity,
            "post_time": post.post_time.isoformat(),
            "expiry_time": post.expiry_time.isoformat(),
            "status": status # Add the status field
        })

    return jsonify(post_list), 200

# NEW ROUTE: Delete a post created by the logged-in user
@posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    post = Post.query.get(post_id)

    # Check if the post exists
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Check if the logged-in user is the one who created the post
    if str(post.donor_id) != current_user_id:
        return jsonify({"error": "You are not authorized to delete this post"}), 403

    # If the post is claimed, you might want to prevent deletion or handle it differently
    # For now, we will delete it along with its claim.
    claim = Claim.query.filter_by(post_id=post_id).first()
    if claim:
        db.session.delete(claim)

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200