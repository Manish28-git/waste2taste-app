# models/claim.py
from extensions import db
from datetime import datetime

class Claim(db.Model):
    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)
    claim_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="claimed", nullable=False) # e.g., claimed, collected

    # Foreign Keys
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False, unique=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    post = db.relationship("Post", backref="claim", uselist=False)
    receiver = db.relationship("User", backref="claims")