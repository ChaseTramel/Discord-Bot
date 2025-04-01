from atproto import Client


def get_latest_post(config, last_url=None):
    client = Client()
    client.login(config["handle"], config["app_password"])

    feed = client.app.bsky.feed.get_author_feed({
        "actor": config["handle"],
        "limit": 10
    })

    print("Fetched posts:")
    for post in feed.feed:
        # print("---")
        # print("URI:", post.post.uri)
        # print("Reason type:", getattr(post.reason, '__class__', type(None)).__name__)
        # print("Reply:", post.reply)
        # print("Text:", getattr(post.post.record, 'text', '[no text]'))

        if post.reason or post.reply:
            continue

        uri = post.post.uri
        rkey = uri.split("/")[-1]
        handle = config["handle"]
        post_url = f"https://bsky.app/profile/{handle}/post/{rkey}"

        if post_url != last_url:
            return post_url

    return None
