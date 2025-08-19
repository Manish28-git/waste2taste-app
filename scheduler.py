# scheduler.py
from extensions import db
from models.post import Post
from datetime import datetime

def delete_expired_posts_job(app):
    """
    This job runs periodically to find and delete posts that have expired.
    """
    with app.app_context():
        try:
            # Find posts where the expiry_time is in the past
            expired_posts = Post.query.filter(Post.expiry_time < datetime.utcnow()).all()

            if not expired_posts:
                print("Scheduler: No expired posts to delete.")
                return

            num_deleted = len(expired_posts)
            for post in expired_posts:
                db.session.delete(post)

            db.session.commit()
            print(f"Scheduler: Successfully deleted {num_deleted} expired post(s).")

        except Exception as e:
            print(f"Scheduler: Error deleting expired posts - {e}")
            db.session.rollback()