from app.extensions import db

class FeedFlagStatus(db.Model):
    __tablename__ = 'feed_flag_status'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text, nullable=False)  # active/spam
    
    # Relationship - one-to-many with Feed model
    feeds = db.relationship('Feed', backref='feed_flag_status', lazy=True)
    
    def __repr__(self):
        return f'<FeedFlagStatus {self.status}>' 