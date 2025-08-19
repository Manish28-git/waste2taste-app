# app.py
from flask import Flask, jsonify
from extensions import db
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.claims import claims_bp # 1. Import the new blueprint
from flask_jwt_extended import JWTManager
from routes.main import main_bp
from routes.profile import profile_bp
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import delete_expired_posts_job

def create_app():
    app = Flask(__name__)

    from flask import render_template 

    # --- Config remains the same ---
    SECRET = 'this-is-a-super-long-and-unchanging-secret-key'
    app.config['SECRET_KEY'] = SECRET
    app.config['JWT_SECRET_KEY'] = SECRET
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waste2taste.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt = JWTManager(app)

    # --- Blueprints remain the same ---
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(posts_bp, url_prefix="/api")
    app.register_blueprint(claims_bp, url_prefix="/api")
    app.register_blueprint(profile_bp, url_prefix="/api") # 2. Register it
    app.register_blueprint(main_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Waste2Taste API!"})

    # 2. Configure and start the scheduler
    scheduler = BackgroundScheduler()
    # Schedule the job to run every hour. Pass the 'app' instance to the job.
    scheduler.add_job(func=lambda: delete_expired_posts_job(app), trigger="interval", hours=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)