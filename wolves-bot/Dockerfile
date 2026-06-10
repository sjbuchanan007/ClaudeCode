FROM python:3.12-slim

WORKDIR /app

# Python dependencies (baked in, so no install on every run)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code. tweets.txt is shipped as a default that's copied into the mounted
# /config volume on first run, so you can edit it on the server without rebuilding.
COPY bot.py platforms.py ./
COPY tweets.txt ./tweets.txt.default
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# tweets.txt + state.json live here; mount a host folder to persist them.
ENV DATA_DIR=/config
VOLUME /config

ENTRYPOINT ["./entrypoint.sh"]
