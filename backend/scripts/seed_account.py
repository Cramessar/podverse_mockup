from seed_utils import get_db_session, fake
from app.models.account import Account, SharableStatus
from sqlalchemy.exc import IntegrityError
import random

def seed_account(n=100):
    session = get_db_session()
    try:
        statuses = session.query(SharableStatus).all()
        if not statuses:
            print("⚠️  No sharable_status rows found. Please seed sharable_status first.")
            return

        accounts = []
        for _ in range(n):
            id_text = fake.unique.user_name()
            verified = fake.boolean(chance_of_getting_true=10)
            sharable_status_id = random.choice(statuses).id

            account = Account(
                id_text=id_text,
                verified=verified,
                sharable_status_id=sharable_status_id
            )
            accounts.append(account)

        session.add_all(accounts)
        session.commit()
        print(f"✅ Seeded {len(accounts)} accounts successfully")

    except IntegrityError as e:
        session.rollback()
        print("⚠️  Integrity error while inserting accounts:", str(e))
    finally:
        session.close()

if __name__ == "__main__":
    seed_account()
