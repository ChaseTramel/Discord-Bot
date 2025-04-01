import json
import logging
import os
import time

import schedule

from platforms import bluesky, ghost, mastodon, reddit

CONFIG_PATH = 'config.json'
STATE_PATH = 'last_posts.json'

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def loadConfig():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def loadLastPosts():
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH) as f:
        return json.load(f)

def saveLastPosts(data):
    with open(STATE_PATH, 'w') as f:
        json.dump(data, f)

def postDiscord(webhook_url, platform, url):
    import requests
    data = {
        "content": f"✅ Hello from your bot! Platform: {platform}\nLink: {url}"
    }
    r = requests.post(webhook_url, json=data)
    print("Discord response:", r.status_code, r.text)

def checkAll():
    config = loadConfig()
    last = loadLastPosts()

    updated = False

    for name, module in {
        #"Ghost": ghost,
        "Mastodon": mastodon,
        # "Reddit": reddit,
        # "Bluesky": bluesky
    }.items():
        try:
            url = module.get_latest_post(config[name.lower()], last.get(name))
            if url:
                postDiscord(config["discord_webhook"], name, url)
                last[name] = url
                updated = True
        except Exception as e:
            logging.error(f"{name} error: {e}")
            postDiscord(config["discord_webhook"], "Error", f"❗ Error fetching {name}: {e}")

    if updated:
        saveLastPosts(last)

schedule.every(loadConfig()["interval_minutes"]).minutes.do(checkAll)

if __name__ == "__main__":
    logging.info("Starting Discord autoposter bot.")
    checkAll()
    while True:
        schedule.run_pending()
        time.sleep(1)
