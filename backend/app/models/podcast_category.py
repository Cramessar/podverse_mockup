from app.extensions import db

class PodcastCategory(db.Model):
    __tablename__ = 'podcast_category'
    """ Many-to-many relationship between podcasts and categories """

    id = db.Column(db.Integer, primary_key=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f'<PodcastCategory podcast_id={self.podcast_id} category_id={self.category_id}>' 