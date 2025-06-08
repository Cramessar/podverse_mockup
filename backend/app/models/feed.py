from app.extensions import db
from datetime import datetime

class Feed(db.Model):
    __tablename__ = 'feed'
    
    id = db.Column(db.Integer, primary_key=True)
    feed_flag_status_id = db.Column(db.Integer, db.ForeignKey('feed_flag_status.id'), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    last_parsed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship - one-to-many with Podcast model
    podcasts = db.relationship('Podcast', backref='feed', lazy=True)
    
    def __repr__(self):
        return f'<Feed {self.url}>' 