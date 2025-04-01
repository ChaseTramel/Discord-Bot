import praw


def get_latest_post(config, last_url=None):
    reddit = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        username=config["username"],
        password=config["password"],
        user_agent=config["user_agent"]
    )

    user = reddit.redditor(config["username"])
    for submission in user.submissions.new(limit=5):
        url = submission.url  # Direct link (e.g. to image or external site)
        permalink = f"https://reddit.com{submission.permalink}"  # Reddit post URL

        # Use permalink to avoid linking just to external URLs
        if permalink != last_url:
            return permalink

    return None
