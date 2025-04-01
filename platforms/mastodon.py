import re

from mastodon import Mastodon


def get_latest_post(config, last_url=None):
    masto = Mastodon(
        access_token=config["access_token"],
        api_base_url=config["instance"]
    )

    # Fetch latest 5 statuses
    statuses = masto.account_statuses(masto.me()["id"], limit=5)

    for status in statuses:
        # Skip replies
        if status["in_reply_to_id"] is not None:
            continue

        # Extract status ID from URL
        post_url = status["url"]
        if post_url != last_url:
            return post_url

    return None
