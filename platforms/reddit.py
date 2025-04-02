import praw
from bs4 import BeautifulSoup


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
        permalink = f"https://reddit.com{submission.permalink}"

        if permalink == last_url:
            continue  # skip if already posted

        title = submission.title

        if submission.is_self:
            raw_text = submission.selftext_html or ""
            text = BeautifulSoup(raw_text, "html.parser").get_text().strip()
        else:
            text = ""

        if len(text) > 300:
            text = text[:297] + "..."

        image = None
    
        preview = getattr(submission, "preview", None)
        if preview and "images" in preview:
            images = preview["images"]
            if images:
                image = images[0]["source"]["url"]

        footer = f"👽 r/{submission.subreddit.display_name} via Reddit"

        return (permalink, title, text or None, image, footer)

    return None
