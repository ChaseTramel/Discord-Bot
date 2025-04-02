import json
import logging
import os
import time
from datetime import datetime, timezone

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

PLATFORM_STYLE = {
    "Ghost": {
        "color": 0xF6F6F6,
        "icon": "https://ghost.org/images/ghost-orb-1.png"
    },
    "Mastodon": {
        "color": 0x6364FF,
        "icon": "https://upload.wikimedia.org/wikipedia/commons/4/48/Mastodon_Logotype_%28Simple%29.svg"
    },
    "Reddit": {
        "color": 0xFF4500,
        "icon": "https://www.redditinc.com/assets/images/site/reddit-logo.png"
    },
    "Bluesky": {
        "color": 0x4C9EEB,
        "icon": "https://bsky.app/favicon.ico"
    }
}

def buildEmbed(platform, title=None, url=None, description=None, image=None):
    style = PLATFORM_STYLE.get(platform, {})
    embed = {
        "title": title or f"New {platform} Post",
        "url": url,
        "description": description or f"Check out the latest {platform} post!",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "footer": {
            "text": f"Posted via {platform}",
            "icon_url": style.get("icon")
        },
        "color": style.get("color", 0xCCCCCC)
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

        print("Sending to Discord:\n", json.dumps(data, indent=2))

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
        # "Mastodon": mastodon,
        # "Reddit": reddit,
        # "Bluesky": bluesky
    }.items():
        try:
            result = module.get_latest_post(config[name.lower()], last.get(name))
            print(f"Result from {name}: {result}")

            if result:
                if isinstance(result, tuple):
                    url, title, description, image = result
                else:
                    url, title, description, image = result, None, None, None

                postDiscord(config["discord_webhook"], name, url, title, description, image)
                last[name] = url
                updated = True
                logging.info(f"Posted {name} update: {url}")
        except Exception as e:
            logging.error(f"{name} error: {e}")
            postDiscord(
                config["discord_webhook"],
                name,
                url=config["ghost"]["url"],  # fallback to Ghost URL just to pass validation
                title=f"❗ Error fetching {name}",
                description=str(e)
            )

    if updated:
        saveLastPosts(last)

schedule.every(loadConfig()["interval_minutes"]).minutes.do(checkAll)

if __name__ == "__main__":
    logging.info("Starting Discord autoposter bot.")
    checkAll()
    while True:
        schedule.run_pending()
        time.sleep(1)
