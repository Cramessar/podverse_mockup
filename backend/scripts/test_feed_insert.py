from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FeedFlagStatus(Base):
    __tablename__ = "feed_flag_status"
    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Feed(Base):
    __tablename__ = "feed"
    id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True, nullable=False)
    feed_flag_status_id = Column(Integer, nullable=False)

def print_feeds(session):
    feeds = session.query(Feed).all()
    print(f"Feeds in DB: {len(feeds)}")
    for f in feeds:
        print(f"ID: {f.id} URL: {f.url} Status ID: {f.feed_flag_status_id}")

def main():
    engine = create_engine("postgresql://podverse_admin:testest@database:5432/podverse_db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Ensure feed_flag_status with id=1 exists
        ffs_exists = session.query(exists().where(FeedFlagStatus.id == 1)).scalar()
        if not ffs_exists:
            print("Inserting feed_flag_status id=1")
            ffs = FeedFlagStatus(id=1, status="active")
            session.add(ffs)
            session.commit()
        else:
            print("feed_flag_status id=1 already exists")

        # Insert a test feed if not present
        feed_url = "http://example.com/testfeed/rss"
        feed_exists = session.query(exists().where(Feed.url == feed_url)).scalar()
        if not feed_exists:
            print("Inserting a test feed row")
            feed = Feed(url=feed_url, feed_flag_status_id=1)
            session.add(feed)
            session.commit()
        else:
            print("Test feed already exists")

        print_feeds(session)

    except Exception as e:
        print(f"Error during DB operations: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
