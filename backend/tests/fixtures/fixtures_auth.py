import pytest
from datetime import datetime, timedelta
import jwt
from app.extensions import db
from app.models.account import Account

@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = Account(
        email='test@example.com',
        username='testuser',
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    admin = Account(
        email='admin@example.com',
        username='adminuser',
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def auth_headers(app, test_user):
    """Generate authentication headers."""
    token = jwt.encode(
        {
            'user_id': test_user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return {'Authorization': f'Bearer {token}'} 