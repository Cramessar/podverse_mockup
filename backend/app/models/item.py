from app.extensions import db
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    
    def __repr__(self):
        return f'<Item {self.title}>' 