# Reddit Bot Manager

A UI-based Reddit bot that lets you manage posts to multiple subreddits with image support.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a Reddit app:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create Application"
   - Choose "script"
   - Save the client ID and client secret

3. Edit `bot.py` and replace these values:
   ```python
   client_id='YOUR_CLIENT_ID'
   client_secret='YOUR_CLIENT_SECRET'
   user_agent='YOUR_BOT_NAME'  # e.g., 'MyBot/1.0'
   username='YOUR_USERNAME'
   password='YOUR_PASSWORD'
   ```

## Usage

Run the UI:
```
python ui.py
```

### Features

- **Manage Subreddits**: Add/remove subreddits to post to
- **Create Posts**: 
  - Image posts with title + description
  - Text posts with title + content
  - Link posts with title + URL
- **Edit/Delete**: Modify or remove existing posts
- **Preview**: View post details before posting
- **Post Now**: Submit a post immediately
- **Auto-save**: Posts and subreddits saved to `posts_config.json`

## File Structure

- `bot.py` - Core Reddit API logic
- `ui.py` - Tkinter GUI application
- `posts_config.json` - Saved posts and subreddits (auto-created)
- `requirements.txt` - Python dependencies
