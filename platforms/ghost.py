import requests


def get_latest_post(config, last_url=None):
    base_url = config['url'].rstrip('/')
    api_key = config['content_api_key']

    try:
        res = requests.get(
            f"{base_url}/ghost/api/content/posts/",
            params={
                "key": api_key,
                "limit": 1,
                "fields": "slug,url",
                "filter": "visibility:public"
            }
        )
        res.raise_for_status()
        posts = res.json().get("posts", [])

        if not posts:
            return None

        post = posts[0]
        post_url = post.get("url") or f"{base_url}/{post['slug']}/"

        return post_url if post_url != last_url else None

    except Exception as e:
        raise Exception(f"Ghost API error: {e}")