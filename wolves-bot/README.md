# Wolves Ay We — X bot

A revival of the original Raspberry Pi cron bot. Posts a random bit of Wolves
banter to X (Twitter) a handful of times a day, at random-ish hours, running
free on GitHub Actions — no Pi, no server, no cron to babysit.

## How it works

- **`tweets.txt`** — the banter list, one tweet per line. Edit this freely;
  blank lines and `#` comments are ignored. No code knowledge needed.
- **`bot.py`** — picks a random line and posts it via the X API v2 (Tweepy).
- **`.github/workflows/wolves-bot.yml`** — runs `bot.py` every hour.

### The scheduling trick

We want 6–12 posts a day at random times, but GitHub Actions only offers a
*fixed* hourly schedule and keeps no memory between runs. So instead of storing
a schedule, `bot.py` derives one from the date: it seeds the random generator
with today's date, picks a random count (6–12) and random hours, and only
tweets when the current hour is one of them. Every hourly run that day computes
the *same* plan, so the result is a guaranteed 6–12 posts, randomly spaced, a
fresh pattern each day — with nothing to store.

Active hours and the min/max post count are tunable at the top of `bot.py`.

## One-time setup

### 1. Get X API credentials

1. Go to the [X Developer Portal](https://developer.x.com/) and sign in.
2. Create a **Project** and an **App** (the **Free** tier is enough — it allows
   ~500 posts/month; 6–12/day stays well under that).
3. In the app's **User authentication settings**, enable **OAuth 1.0a** with
   **Read and Write** permissions (write is required to post — if you only see
   read, fix this *before* generating tokens).
4. From **Keys and tokens**, grab four values:
   - API Key  → `CONSUMER_KEY`
   - API Key Secret → `CONSUMER_SECRET`
   - Access Token → `ACCESS_TOKEN`
   - Access Token Secret → `ACCESS_TOKEN_SECRET`

   If you set Read/Write *after* creating the access token, regenerate the
   access token so it picks up write permission.

### 2. Add them as GitHub secrets

In the repo: **Settings → Secrets and variables → Actions → New repository
secret**, and add all four with the names above.

### 3. Done

The workflow runs automatically every hour. To test without waiting (or
posting), go to **Actions → wolves-bot → Run workflow** and tick **dry run**.

## Running locally

```bash
cd wolves-bot
pip install -r requirements.txt

# See today's plan without posting:
DRY_RUN=1 python bot.py

# Actually post (needs the four env vars set):
export CONSUMER_KEY=... CONSUMER_SECRET=... ACCESS_TOKEN=... ACCESS_TOKEN_SECRET=...
python bot.py
```

`DRY_RUN=1` prints the day's plan and what it *would* post, without hitting the
API or needing credentials.

## Notes

- The original Pi version flashed a green/red **LedBorg** LED on success/failure.
  That's hardware-specific and dropped here since this runs in the cloud. If you
  ever want the light back, that part belongs on a Pi (use the modern `gpiozero`
  library rather than the old `wiringpi2`).
