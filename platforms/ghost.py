import requests


def get_latest_post(config, last_url=None):
    import requests
    base_url = config['url'].rstrip('/')
    api_key = config['content_api_key']

    try:
        res = requests.get(
            f"{base_url}/ghost/api/content/posts/",
            params={
                "key": api_key,
                "limit": 1,
                "fields": "title,slug,url,feature_image,custom_excerpt,excerpt"
            }
        )
        res.raise_for_status()
        posts = res.json().get("posts", [])
        if not posts:
            return None

        post = posts[0]
        url = post.get("url") or f"{base_url}/{post['slug']}/"
        title = post.get("title", "New blog post")
        excerpt = (post.get("custom_excerpt") or post.get("excerpt") or "").strip()
        if len(excerpt) > 300:
            excerpt = excerpt[:297] + "..."
        image = post.get("feature_image")

        if url != last_url:
            return (url, title, excerpt, image)

        return None

    except Exception as e:
        raise Exception(f"Ghost API error: {e}")
