#!/bin/sh
# Runs the bot on a steady schedule inside the container. Because the server is
# always on, this is far more reliable than GitHub's cron -- and bot.py's
# catch-up logic still covers any container restart or downtime.
set -e

: "${DATA_DIR:=/config}"
: "${INTERVAL_MINUTES:=15}"
mkdir -p "$DATA_DIR"

# Seed an editable tweets.txt into the mounted volume on first run.
if [ ! -f "$DATA_DIR/tweets.txt" ]; then
  cp /app/tweets.txt.default "$DATA_DIR/tweets.txt"
  echo "Seeded $DATA_DIR/tweets.txt -- edit this file to change the banter."
fi

interval=$((INTERVAL_MINUTES * 60))
echo "Wolves bot started; checking every ${INTERVAL_MINUTES} min. Data dir: $DATA_DIR"

while true; do
  python /app/bot.py || echo "(bot.py exited non-zero -- see above)"
  # Sleep to the next interval boundary so runs land near the clock.
  now=$(date +%s)
  sleep $(( interval - now % interval ))
done
