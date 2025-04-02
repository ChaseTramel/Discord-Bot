from bs4 import BeautifulSoup
from mastodon import Mastodon


def get_latest_post(config, last_url=None):
    masto = Mastodon(
        access_token=config["access_token"],
        api_base_url=config["instance"]
    )

    me = masto.me()
    statuses = masto.account_statuses(me["id"], limit=5)

    for status in statuses:
        if status["in_reply_to_id"] is not None:
            continue  # skip replies

        post_url = status["url"]
        if post_url == last_url:
            continue  # skip if already posted

        soup = BeautifulSoup(status["content"], "html.parser")
        content = soup.get_text().strip()

        if len(content) > 280:
            content = content[:277] + "..."

        media = status.get("media_attachments", [])
        image = media[0]["preview_url"] if media else None

        return (post_url, None, content, image)

    return None
