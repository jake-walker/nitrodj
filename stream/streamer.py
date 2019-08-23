import shout
from logzero import logger
import os

class Streamer:
    skip_current_song = False
    open = False

    def __init__(self, host, port, password):
        self.shout = shout.Shout()
        logger.info("Creating new streamer (libshout version %s)...", shout.version())

        # Set stream metadata
        self.shout.audio_info = {
            shout.SHOUT_AI_BITRATE: "128",
            shout.SHOUT_AI_SAMPLERATE: "44100",
            shout.SHOUT_AI_CHANNELS: "2"
        }
        self.shout.ogv = 0
        self.shout.format = "mp3"

        # Set connection information
        self.shout.host = host
        self.shout.port = int(port)
        self.shout.mount = "/stream"
        self.shout.user = "source"
        self.shout.password = password

        # Set stream information
        self.shout.name = "NitroDJ"
        self.shout.genre = "Various"
        self.shout.description = "NitroDJ instance"
        self.shout.url = "http://{}:{}/stream".format(host, port)

        self.shout.open()
        self.shout.close()

    def start(self):
        logger.info("Starting stream!")
        self.shout.open()
        self.open = True

    def stop(self):
        logger.info("Stopping stream")
        self.shout.close()
        self.open = False

    def skip_song(self):
        self.skip_current_song = True

    def send_file(self, song):
        if not os.path.exists(song["filename"]):
            raise Exception("Song file not found: %s".format(song["filename"]))

        logger.info("Streaming song '%s' (%d)", song["title"], song["id"])

        file = open(song["filename"], "rb")
        # Set song name on stream
        self.shout.set_metadata({
            "song": song["title"]
        })

        while True:
            if self.skip_current_song:
                logger.info("Skipping current song!")
                self.shout.sync()
                self.skip_current_song = False
                break

            buffer = file.read(4096)
            if not len(buffer):
                break

            try:
                self.shout.send(buffer)
                self.shout.sync()
            except shout.ShoutException:
                self.start()

        file.close()
