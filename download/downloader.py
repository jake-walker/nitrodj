import youtube_dl
from logzero import logger
import os


class DownloaderLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        logger.warn(msg)

    def error(self, msg):
        logger.error(msg)


def get_download_path():
    script_path = os.path.realpath(__file__)
    folder_path = os.path.dirname(script_path)
    download_path = os.path.abspath(os.path.join(folder_path, "../songs"))
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return download_path


class Downloader:
    ytdl = None
    last_filename = ""
    downloading = False
    download_directory = ""

    def progress_hook(self, data):
        if data["status"] == "finished":
            # data["filename"] has a .webm extension, we need to convert it to a .mp3
            filename = data["filename"]
            filename = filename.split(".")
            filename[-1] = "mp3"
            filename = ".".join(filename)
            self.last_filename = filename

    def __init__(self):
        self.download_directory = get_download_path()
        logger.debug("Initializing YouTube download... (downloads will be stored at %s)", self.download_directory)
        self.ytdl = youtube_dl.YoutubeDL({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }],
            "logger": DownloaderLogger(),
            "progress_hooks": [
                self.progress_hook
            ]
        })

    def download(self, youtube_id):
        logger.info("Downloading %s...", youtube_id)
        self.downloading = True
        self.last_filename = ""

        url = "https://www.youtube.com/watch?v={}".format(youtube_id)

        os.chdir(self.download_directory)

        errors = self.ytdl.download([url])
        if errors:
            raise Exception("There was an unknown error whilst downloading")
        if self.last_filename == "":
            raise Exception("The filename could not be found")
        if not os.path.exists(self.last_filename):
            raise Exception("The downloaded file does not exist")

        self.downloading = False
        logger.debug("Download complete!")
        return os.path.join(self.download_directory, self.last_filename)
