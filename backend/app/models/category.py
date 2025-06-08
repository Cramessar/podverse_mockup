from app.extensions import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    display_name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    mapping_key = db.Column(db.String(255), nullable=False)
    
    # Many-to-many relationship with podcasts
    podcast_categories = db.relationship('PodcastCategory', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.display_name}>' 