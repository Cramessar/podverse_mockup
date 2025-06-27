from seed_utils import get_db_session
from app.models.medium import Medium
from sqlalchemy.exc import IntegrityError

medium_values = [
    'publisher', 'podcast', 'music', 'video', 'film', 'audiobook', 'newsletter', 'blog', 'course',
    'mixed', 'podcastL', 'musicL', 'videoL', 'filmL', 'audiobookL', 'newsletterL', 'blogL', 'publisherL', 'courseL'
]

def seed_medium():
    session = get_db_session()
    try:
        for value in medium_values:
            medium = Medium(value=value)
            session.add(medium)
        session.commit()
        print("✅ Medium values seeded successfully")
    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_medium()
