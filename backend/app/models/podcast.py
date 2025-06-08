from app.extensions import db
from datetime import datetime

class Podcast(db.Model):
    __tablename__ = 'podcasts'
    
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    medium_id = db.Column(db.Integer, db.ForeignKey('medium.id'), nullable=False)
    id_text = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    slug = db.Column(db.String(100), nullable=False)
    
    # Relationships - many-to-many with PodcastCategory model
    podcast_categories = db.relationship('PodcastCategory', backref='podcast', lazy=True)
    
    def __repr__(self):
        return f'<Podcast {self.title}>'
