<h1 align="center">
    NitroDJ
</h1>

<h3 align="center">
    A self-hosted democratic radio station.
</h3>

## Overview

NitroDJ is designed for parties and allows users to queue up their own music and be in charge of the music.

NitroDJ takes songs from YouTube and streams them to an Icecast Server. This solution takes a lot of the heavy lifting from a client and should allow it to work better in restricted environments like behind firewalls and over mobile data.

**What is Icecast?** 'Icecast is a streaming media (audio/video) server... It can be used to create an Internet radio station or privately running jukebox and many things in between.'

## Installation

**At the moment, NitroDJ only seems to work on Linux machines.** If developing on Windows, it is recommended to develop normally and run in either a Virtual Machine with shared folder or inside [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

To run NitroDJ you will need to host both NitroDJ itself and also an Icecast server to stream to.

**Dependencies:** `libshout3`, `libshout3-dev`, `ffmpeg`, `node` and `yarn`

```bash
# DEBIAN BASED DISTROS ONLY
# Install dependencies
sudo apt install libshout3 libshout3-dev ffmpeg
# Install Node
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash -
sudo apt-get install -y nodejs
# Install yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn


# Install Python dependencies
python3 -m pip install -r requirements.txt


# Build web assets (this only has to be done once if the web assets don't change!)
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

## Project Structure

<pre><code>
|- app <i><small>(the decompiled Vue.js web app)</small></i>
|   |- public
|    ` src <i><small>(the source code for the web app)</small></i>
|       |- assets <i><small>(images, css, etc...)</small></i>
|       |- components <i><small>(Vue.js components)</small></i>
|       |   |- Queue.vue
|       |    ` Search.vue
|       |- plugins 
|       |- App.vue
|        ` main.js
|- download
|   |- <i>songs</i> <i><small>(the downloaded songs, only visible after first run)</small></i>
|   |- downloader.py <i><small>(the code for downloading songs from the queue)</small></i>
|- search
|   |- searcher.py <i><small>(the code for handling YouTube searches)</small></i>
|- stream
|   |- streamer.py <i><small>(the code for streaming songs to Icecast)</small></i>
|- web
|   |- <i>static</i> <i><small>(the compiled web app, only visible after 'yarn build')</small></i>
|   |- <i>templates</i> <i><small>(the compiled web app, only visible after 'yarn build')</small></i>
|   |- __init__.py <i><small>(the main Flask application)</small></i>
|    ` api.py <i><small>(the API routes for Flask)</small></i>
|- index.py <i><small>(the main application)</small></i>
 ` songqueue.py <i><small>(the code for managing song queues)</small></i>
</pre></code>

### How it works

There are 3 seperate threads: the downloader, the streamer and the web app.

The web app takes song requests from users and handles searches, then songs get added to the queue. Once a song has been added, metadata about the song is downloaded and added to the database.

The downloader keeps finding songs in the queue that haven't been downloaded yet. Once one is found, the song is downloaded into the `./download/songs/` folder and that path is stored in the database for future reference. Then the downloader looks for more songs.

The streamer takes the next downloaded song from the queue, splits it up into chunks and sends them off to the Icecast server.

All of these different pieces are constantly working in order to make a seamless experience behind the scenes.