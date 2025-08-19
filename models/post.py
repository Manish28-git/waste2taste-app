# models/post.py
from extensions import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    post_time = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_time = db.Column(db.DateTime, nullable=False)

    # Foreign Key to link to the user who created the post
    donor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship to access the User object
    donor = db.relationship("User", backref="posts")