import argparse
from seed_utils import run_seeder_with_retry
from backend.app.utils.request_logger import get_logger
from app import create_app

# Import all seeders
from seed_user import seed_user
from seed_feed_flag_status import seed_feed_flag_status
from seed_feed import seed_feed
from seed_channel import seed_channel
from seed_item_flag_status import seed_item_flag_status
from seed_item import seed_item
from seed_sharable_status import seed_sharable_status
from seed_account import seed_account
from seed_stats_track_account_guid import seed_stats_track_account_guid
from seed_stats_event_channel import seed_stats_event_channel
from seed_stats_event_item import seed_stats_event_item
from seed_stats_aggregated_channel import seed_stats_aggregated_channel
from seed_stats_aggregated_item import seed_stats_aggregated_item

logger = get_logger(__name__)

# Seeder list (name, seeder function)
SEED_JOBS = [
    ("Users", seed_user),
    ("Feed Flag Status", seed_feed_flag_status),
    ("Feeds", seed_feed),
    ("Channels", seed_channel),
    ("Item Flag Status", seed_item_flag_status),
    ("Items", seed_item),
    ("Sharable Status", seed_sharable_status),
    ("Accounts", seed_account),
    ("Account GUIDs", seed_stats_track_account_guid),
    ("Stats Event Channel", seed_stats_event_channel),
    ("Stats Event Item", seed_stats_event_item),
    ("Stats Aggregated Channel", seed_stats_aggregated_channel),
    ("Stats Aggregated Item", seed_stats_aggregated_item),
]

def normalize_name(name: str):
    return name.lower().replace(" ", "_")

def main():
    parser = argparse.ArgumentParser(description="Seed the Podverse database")
    parser.add_argument("--only", help="Comma-separated list of seeders to run (normalized names)", type=str)
    parser.add_argument("--skip", help="Comma-separated list of seeders to skip (normalized names)", type=str)
    parser.add_argument("--count", help="Override count for seeders that accept n", type=int, default=None)

    args = parser.parse_args()

    only = set(normalize_name(name) for name in args.only.split(",")) if args.only else None
    skip = set(normalize_name(name) for name in args.skip.split(",")) if args.skip else set()

    # Create Flask app and push application context
    app = create_app()
    with app.app_context():
        logger.info("\nStarting full seeding process...\n")

        summary = []

        for label, func in SEED_JOBS:
            normalized = normalize_name(label)

            if only and normalized not in only:
                continue
            if normalized in skip:
                logger.info(f"Skipping {label}")
                continue

            logger.info(f"Seeding {label}...")
            if args.count is not None:
                try:
                    success = run_seeder_with_retry(lambda: func(n=args.count))
                except TypeError:
                    # For seeders that don't accept `n`
                    success = run_seeder_with_retry(func)
            else:
                success = run_seeder_with_retry(func)

            if success:
                logger.info(f"✅ {label} seeded successfully!\n")
                summary.append(f"✅ {label}")
            else:
                logger.error(f"❌ Failed to seed {label}\n")
                summary.append(f"❌ {label}")

        logger.info("\nSeeder Summary:")
        for entry in summary:
            logger.info(f"  {entry}")

        logger.info("\n✅ All seeders completed. Database is ready!\n")

if __name__ == "__main__":
    main()
