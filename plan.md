# Discord Bot Plan

I’m looking to build a lightweight Discord bot that automatically posts links in a specific channel whenever I make a new post on Bluesky, Mastodon, Reddit, or my Ghost blog.

Every 15 minutes, it should check for new posts. When a new post if found, it should post a basic message with a link to the Discord channel. Something like "I posted on platform. Go like, comment, and share, if you will!" It should duplicates by tracking the most recent post from each source.

It should use Discord webhooks, as well as the Ghost Content API, the Mastodon API, an unofficial Bluesky API wrapper, and the Reddit API. I prefer minimal dependencies, because it must be lightweight and easy to maintain.

I'd like it in Python. I’ll be running this on a cloud VPS called DigitalOcean.

I don't need a frontend: I can just add and remove API keys via a config file or CLI. A basic console log or simple file log is fine.

For 'nice-to-haves', I'd love for it to support embeds or rich previews, as well as provide me with a simple alert in Discord if an error happens.
