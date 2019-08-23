# NitroDJ

NitroDJ is a democratic radio station, allowing people to queue up songs to be played.

NitroDJ takes songs from YouTube and streams them to an Icecast Server.

## Installation

**Dependencies:** `libshout3`, `libshout3-dev`, `ffmpeg`, `node` and `yarn`

```shell script
# Install Python dependencies
python3 -m pip install -r requirements.txt

# Build web assets
cd app/
yarn install
yarn build
cd ../

# Start server
export NITRO_ICECAST_HOST="example.com"   # Icecast Server Host
export NITRO_ICECAST_PORT="8000"          # Icecast Server Port
export NITRO_ICECAST_PASSWORD="password"  # Icecast Source Password
export NITRO_YOUTUBE_KEY="12345"          # YouTube Data API Key
python3 index.py
```