from seed_utils import run_seeder_with_retry

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


def main():
    print("\n🚀 Starting full seeding process...\n")
    for name, seeder in SEED_JOBS:
        run_seeder_with_retry(seeder, label=name)

    print("\n✅ All seeders completed. Database is ready!\n")


if __name__ == "__main__":
    main()