from seed_utils import get_db_session, fake, random_past_date, random_device_info, random_location
from app.models.user import User
import uuid
import random

def seed_user(n=200):
    session = get_db_session()
    try:
        users = []
        for _ in range(n):
            email = fake.unique.email()
            username = fake.user_name()
            role = "admin" if random.random() < 0.05 else "user"
            created_at = random_past_date()
            last_login = random_past_date()
            is_active = random.random() > 0.1
            total_listen_time_seconds = random.randint(0, 10_000_000)
            referral_token = str(uuid.uuid4())
            device_info = random_device_info()
            location = random_location()

            user = User(
                email=email,
                username=username,
                role=role,
                created_at=created_at,
                last_login=last_login,
                is_active=is_active,
                total_listen_time_seconds=total_listen_time_seconds,
                referral_token=referral_token,
                device_info=device_info,
                location=location,
            )
            users.append(user)

        session.add_all(users)
        session.commit()
        print(f"✅ Seeded {n} users successfully")

    except Exception as e:
        session.rollback()
        print("⚠️  Error while seeding users:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_user()