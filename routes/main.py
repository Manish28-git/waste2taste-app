# routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/register")
def register_page():
    return render_template("register.html")

@main_bp.route("/login")
def login_page():
    return render_template("login.html")

@main_bp.route("/posts")
def posts_page():
    return render_template("posts.html")

# Add this new route for the create post page
@main_bp.route("/create-post")
def create_post_page():
    """Serves the page for creating a new food post."""
    return render_template("create_post.html")


@main_bp.route("/dashboard")
def dashboard_page():
    """Serves the donor dashboard page."""
    return render_template("donor_dashboard.html")

# Add this new route for the receiver's claim history
@main_bp.route("/my-claims")
def my_claims_page():
    """Serves the receiver's claim history page."""
    return render_template("receiver_dashboard.html")

@main_bp.route("/profile")
def profile_page():
    """Serves the user profile page."""
    return render_template("profile.html")