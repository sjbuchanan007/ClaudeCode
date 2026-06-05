#!/usr/bin/env python3
"""Wolves Ay We — a wee X (Twitter) bot.

Posts a random line from tweets.txt a handful of times a day, at random-ish
hours, so it reads like a person rather than a clockwork machine.

Scheduling trick (so we need no database / no server keeping state):
the daily plan is derived deterministically from today's date. Every run that
day computes the SAME plan -- "post N times today, at these hours" -- and only
actually tweets when the current hour is one of the chosen slots. Run this
once an hour (see the GitHub Actions workflow) and you get a fresh, random
pattern of 6-12 posts every day with nothing to store between runs.
"""

import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import tweepy

# --- Tunables ---------------------------------------------------------------
# Local timezone the "waking hours" are measured in (Wolverhampton).
TIMEZONE = ZoneInfo("Europe/London")
# Don't tweet outside these hours (24h clock, inclusive start, exclusive end).
ACTIVE_START_HOUR = 8    # 08:00
ACTIVE_END_HOUR = 23     # up to 22:59
# Random number of posts per day, picked fresh each day.
MIN_TWEETS_PER_DAY = 6
MAX_TWEETS_PER_DAY = 12

TWEETS_FILE = Path(__file__).with_name("tweets.txt")


def load_tweets():
    """Read tweets.txt: one tweet per line, skipping blanks and # comments."""
    lines = []
    for raw in TWEETS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    if not lines:
        sys.exit(f"No tweets found in {TWEETS_FILE} -- add some lines first.")
    return lines


def todays_slots(now):
    """Return the set of hours we've decided to post at today.

    Seeded by the date, so it's stable across every run on the same day but
    different from one day to the next.
    """
    planner = random.Random(now.strftime("%Y-%m-%d"))
    count = planner.randint(MIN_TWEETS_PER_DAY, MAX_TWEETS_PER_DAY)
    active_hours = list(range(ACTIVE_START_HOUR, ACTIVE_END_HOUR))
    count = min(count, len(active_hours))
    return set(planner.sample(active_hours, count))


def should_post(now):
    return now.hour in todays_slots(now)


def make_client():
    """Build a Tweepy v2 client from environment variables."""
    try:
        return tweepy.Client(
            consumer_key=os.environ["CONSUMER_KEY"],
            consumer_secret=os.environ["CONSUMER_SECRET"],
            access_token=os.environ["ACCESS_TOKEN"],
            access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
        )
    except KeyError as missing:
        sys.exit(f"Missing required environment variable: {missing}")


def main():
    now = datetime.now(timezone.utc).astimezone(TIMEZONE)
    slots = todays_slots(now)
    print(f"{now:%Y-%m-%d %H:%M %Z} | today's plan: "
          f"{len(slots)} posts at hours {sorted(slots)}")

    if not should_post(now):
        print(f"Hour {now.hour} isn't a posting slot today -- nothing to do.")
        return

    # Pick the tweet with real (unseeded) randomness so the text varies even
    # if a slot is retried.
    text = random.SystemRandom().choice(load_tweets())

    if os.environ.get("DRY_RUN") == "1":
        print(f"[DRY RUN] would post: {text}")
        return

    client = make_client()
    try:
        client.create_tweet(text=text)
        print(f"Posted: {text}")
    except tweepy.TweepyException as err:
        sys.exit(f"Error posting to X: {err}")


if __name__ == "__main__":
    main()
