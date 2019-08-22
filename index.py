import songqueue
import threading
import download
import stream
import time
import os
from logzero import logger
import web


def download_task(q):
    # Create a new downloader instance
    dl = download.Downloader()
    last_update = None
    while True:
        if last_update == hash(q):
            time.sleep(5)
            continue
        last_update = hash(q)

        # Get the next song that hasn't been downloaded
        song = q.get_next_song(only_undownloaded=True)

        if song is None:
            time.sleep(5)
            continue

        # Download the song and store the filename
        filename = dl.download(song["youtube_id"])
        # Update the database with the filename
        q.update_song(song["id"], filename=filename)


def stream_task(q):
    # Create a new streamer instance
    st = stream.Streamer(host=os.getenv("NITRO_ICECAST_HOST", "localhost"),
                         port=os.getenv("NITRO_ICECAST_POST", 8000),
                         password=os.getenv("NITRO_ICECAST_PASSWORD", "hackme"))
    warned = False
    while True:
        # Get the next downloaded song
        song = q.get_next_song(only_downloaded=True)
        # If there is no song
        if song is None:
            if not warned and st.open:
                logger.warn("There are no songs on the queue!")
                warned = True
            # Wait 0.2 seconds and try again
            time.sleep(0.2)
            continue

        if not st.open:
            st.start()

        # Stream the song
        st.send_file(song)

        # Remove the song from the queue
        q.remove_song(song["id"])


if __name__ == "__main__":
    q = songqueue.SongQueue()

    download_thread = threading.Thread(target=download_task, args=(q,))
    download_thread.start()

    stream_thread = threading.Thread(target=stream_task, args=(q,))
    stream_thread.start()

    q.add_song("agQq0IsdlJQ")
    q.add_song("qAeybdD5UoQ")

    web.app.run(debug=True, host="0.0.0.0")