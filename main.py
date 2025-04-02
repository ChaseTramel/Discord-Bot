import json
import logging
import os
import time
from datetime import datetime

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



from datetime import datetime


def buildEmbed(platform, title=None, url=None, description=None, image=None):
    embed = {
        "title": title or f"New {platform} Post",
        "description": description or f"Check out the latest {platform} post!",
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": f"Posted via {platform}"
        }
    }

    if image:
        embed["thumbnail"] = {"url": image}

    return embed



def postDiscord(webhook_url, platform, url, title=None, description=None, image=None):
    import requests
    try:
        embed = buildEmbed(platform, title=title, url=url, description=description, image=image)

        data = {
            "content": f"I posted on **{platform}**. Go like, comment, and share, if you will!",
            "embeds": [embed]
        }
    
        import jsonprint("Sending to Discord:\n", json.dumps(data, indent=2))

        response = requests.post(webhook_url, json=data)
        if response.status_code not in [200, 204]:
            raise Exception(f"Discord webhook error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Discord error: {e}")




def checkAll():
    config = loadConfig()
    last = loadLastPosts()

    updated = False

    for name, module in {
        "Ghost": ghost,
        "Mastodon": mastodon,
        "Reddit": reddit,
        "Bluesky": bluesky
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
