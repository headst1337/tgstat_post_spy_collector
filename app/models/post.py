from datetime import datetime
from app import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    post_link = db.Column(db.String(128))
    group_link = db.Column(db.String(128))
    body = db.Column(db.Text)
    payment_data = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
