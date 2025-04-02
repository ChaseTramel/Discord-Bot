from atproto import Client


def get_latest_post(config, last_url=None):
    client = Client()
    client.login(config["handle"], config["app_password"])
    handle = config["handle"]

    feed = client.app.bsky.feed.get_author_feed({
        "actor": handle,
        "limit": 10
    })

    for post in feed.feed:
        if post.reply or post.reason:
            continue

        record = post.post.record
        text = getattr(record, "text", "").strip()

        if len(text) > 300:
            text = text[:297] + "..."

        uri = post.post.uri
        rkey = uri.split("/")[-1]
        post_url = f"https://bsky.app/profile/{handle}/post/{rkey}"
        did = post.post.author.did

        image = None
        embed = getattr(record, "embed", None)
        if embed and hasattr(embed, "images"):
            images = getattr(embed, "images", [])
            if isinstance(images, list) and len(images) > 0:
                blob = images[0].image
                if blob and hasattr(blob, "ref"):
                    cid = blob.ref.link
                    image = f"https://cdn.bsky.app/img/feed_fullsize/plain/{did}/{cid}@jpeg"

        return (post_url, None, text, image)

    return None
