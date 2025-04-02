# Discord Bot : Starship Odyssey Intercom

I made this super tiny Python bot for my personal use. It auto-posts your latest content to a Discord channel using a webhook.
It checks Ghost, Mastodon, Reddit, and Bluesky every few minutes and sends an embed to Discord that has some variation so people don't tune it out.

---

## Features

-   Watches your feeds every 15 minutes
-   Posts new content to Discord using a webhook
-   Includes nice looking embeds with information from each platform
-   Skips reposts automatically using `last_posts.json`
-   Adds a fun randomized message each time

## Step-Up

1. Clone this repo.
2. Copy `config.sample.json` to `config.json` .
3. Fill in your API keys and info .
4. Install dependencies.

```bash
pip install -r requirements.txt

```

5. Run it.

```bash
python main.py

```

6. (optional) To add auto-start on reboot, use `launch.sh` to start the bot and log output. Add it to `crontab` like this:

```bash
@reboot /path/to/Discord-Bot/launch.sh
```

## Notes

_Your_ `config.json` is ignored by Git. Don't push your API keys!

## Conclusion

This was just a simple evening project for me. Thank you.
