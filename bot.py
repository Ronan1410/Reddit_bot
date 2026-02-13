import praw
import time
from datetime import datetime
from typing import List, Dict
import os

# Initialize Reddit API client
def get_reddit():
    return praw.Reddit(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        user_agent='YOUR_BOT_NAME',
        username='YOUR_USERNAME',
        password='YOUR_PASSWORD'
    )

def post_to_reddit(reddit, post: Dict) -> bool:
    """Post to a single subreddit with image support"""
    try:
        subreddit = reddit.subreddit(post['subreddit'])
        
        if post['type'] == 'image':
            # Image post
            if not os.path.exists(post['image_path']):
                raise FileNotFoundError(f"Image not found: {post['image_path']}")
            
            submission = subreddit.submit(
                title=post['title'],
                selftext=post.get('description', ''),
                image_path=post['image_path']
            )
        elif post['type'] == 'text':
            # Text post
            submission = subreddit.submit(
                title=post['title'],
                selftext=post['content']
            )
        elif post['type'] == 'link':
            # Link post
            submission = subreddit.submit(
                title=post['title'],
                url=post['url']
            )
        
        print(f"✓ Posted to r/{post['subreddit']} at {datetime.now()}")
        return True
    except Exception as e:
        print(f"✗ Error posting to r/{post['subreddit']}: {e}")
        return False

def post_all(posts: List[Dict], delay: int = 60) -> None:
    """Post to all subreddits with delay between posts"""
    reddit = get_reddit()
    for post in posts:
        post_to_reddit(reddit, post)
        time.sleep(delay)

if __name__ == '__main__':
    pass
