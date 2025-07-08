from seed_utils import get_db_session
from app.models.category import Category
from faker import Faker
from sqlalchemy.exc import IntegrityError

fake = Faker()

parent_categories = [
    'Arts', 'Business', 'Comedy', 'Education', 'Fiction', 'Government', 'History',
    'Health & Fitness', 'Kids & Family', 'Leisure', 'Music', 'News',
    'Religion & Spirituality', 'Science', 'Society & Culture', 'Sports', 'Technology',
    'True Crime', 'TV & Film'
]

child_categories = {
    'Arts': ['Books', 'Design', 'Fashion & Beauty', 'Food', 'Performing Arts', 'Visual Arts'],
    'Business': ['Careers', 'Entrepreneurship', 'Investing', 'Management', 'Marketing', 'Non-Profit'],
    'Comedy': ['Comedy Interviews', 'Improv', 'Stand-Up'],
    'Education': ['Courses', 'How To', 'Language Learning', 'Self-Improvement'],
    'Fiction': ['Comedy Fiction', 'Drama', 'Science Fiction'],
    'Health & Fitness': ['Alternative Health', 'Fitness', 'Medicine', 'Mental Health', 'Nutrition', 'Sexuality'],
    'Kids & Family': ['Education for Kids', 'Parenting', 'Pets & Animals', 'Stories for Kids'],
    'Leisure': ['Animation & Manga', 'Automotive', 'Aviation', 'Crafts', 'Games', 'Hobbies', 'Home & Garden', 'Video Games'],
    'Music': ['Music Commentary', 'Music History', 'Music Interviews'],
    'News': ['Business News', 'Daily News', 'Entertainment News', 'News Commentary', 'Politics', 'Sports News', 'Tech News'],
    'Religion & Spirituality': ['Buddhism', 'Christianity', 'Hinduism', 'Islam', 'Judaism', 'Religion', 'Spirituality'],
    'Science': ['Astronomy', 'Chemistry', 'Earth Sciences', 'Life Sciences', 'Mathematics', 'Natural Sciences', 'Nature', 'Physics', 'Social Sciences'],
    'Society & Culture': ['Documentary', 'Personal Journals', 'Philosophy', 'Places & Travel', 'Relationships'],
    'Sports': ['Baseball', 'Basketball', 'Cricket', 'Fantasy Sports', 'Football', 'Golf', 'Hockey', 'Rugby', 'Running', 'Soccer', 'Swimming', 'Tennis', 'Volleyball', 'Wilderness', 'Wrestling'],
    'TV & Film': ['After Shows', 'Film History', 'Film Interviews', 'Film Reviews', 'TV Reviews']
}

def slugify(name):
    return name.lower().replace(" ", "-").replace("&", "and")

def camel_case(name):
    return slugify(name).replace("-", "")

def seed_category():
    session = get_db_session()
    category_map = {}

    try:
        for name in parent_categories:
            slug = slugify(name)
            category = Category(
                display_name=name,
                slug=slug,
                mapping_key=camel_case(name),
                parent_id=None
            )
            session.add(category)
            session.flush()
            category_map[name] = category.id

        for parent, children in child_categories.items():
            parent_id = category_map.get(parent)
            if parent_id:
                for child in children:
                    slug = slugify(child)
                    category = Category(
                        display_name=child,
                        slug=slug,
                        mapping_key=camel_case(child),
                        parent_id=parent_id
                    )
                    session.add(category)

        session.commit()
        print("✅ Categories seeded successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_category()
