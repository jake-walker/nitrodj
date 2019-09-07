import sqlite3
from logzero import logger
import pafy
import os
import threading

def get_db_path():
    script_path = os.path.realpath(__file__)
    folder_path = os.path.dirname(script_path)
    db_path = os.path.abspath(os.path.join(folder_path, "/songs/nitro_{}.db"))
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    return db_path


class SongQueue:
    queue = []

    def __init__(self, queue_name="default"):
        logger.debug("Creating new song queue: %s", queue_name)
        self.conn = sqlite3.connect(get_db_path().format(queue_name), check_same_thread=False)
        self.c = self.conn.cursor()

        # Create table
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS "songs" (
                  "id"          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  "youtube_id"  TEXT NOT NULL UNIQUE,
                  "title"       TEXT,
                  "artist"      TEXT,
                  "filename"    TEXT,
                  "rating"      INTEGER DEFAULT 0
            );
        """)
        self.conn.commit()

        self.db_lock = threading.Lock()

    def add_song(self, youtube_id):
        logger.debug("Adding %s to the queue...", youtube_id)

        self.db_lock.acquire()
        self.c.execute("SELECT id FROM songs WHERE youtube_id = ?", (youtube_id,))
        result = self.c.fetchone()
        self.db_lock.release()

        id = -1
        if result is not None:
            self.queue.append(result[0])
            id = result[0]
        else:
            logger.debug("Downloading metadata for %s...", youtube_id)
            metadata = pafy.new("https://www.youtube.com/watch?v={}".format(youtube_id))

            self.db_lock.acquire()
            self.c.execute("INSERT INTO songs (youtube_id, title, artist) VALUES (?, ?, ?)", (youtube_id, metadata.title, metadata.author,))
            self.conn.commit()

            self.queue.append(self.c.lastrowid)
            id = self.c.lastrowid
            self.db_lock.release()

        logger.info("%s (%d) has been added to the queue", youtube_id, id)

    def get_song(self, index):
        try:
            id = self.queue[index]
        except IndexError:
            return None

        self.db_lock.acquire()
        self.c.execute("SELECT youtube_id, title, artist, filename, rating FROM songs WHERE id = ?", (id,))
        song = self.c.fetchone()
        self.db_lock.release()

        if song is None:
            raise Exception("Expected {} to be in the database!".format(id))
        return {
            "id": id,
            "youtube_id": song[0],
            "title": song[1],
            "artist": song[2],
            "filename": song[3],
            "rating": song[4]
        }

    def get_next_song(self, only_downloaded=False, only_undownloaded=False):
        for index in range(0, len(self.queue)):
            song = self.get_song(index)
            if only_downloaded:
                if song["filename"] is not None:
                    return song
            elif only_undownloaded:
                if song["filename"] is None:
                    return song
            else:
                return song
        return None

    def remove_song(self, id):
        self.queue.remove(id)

    def update_song(self, id, filename=None):
        self.db_lock.acquire()
        if filename is not None:
            self.c.execute("UPDATE songs SET filename = ? WHERE id = ?", (filename, id,))

        self.conn.commit()
        self.db_lock.release()

    def get_queue(self):
        return self.queue

    def __hash__(self):
        return hash(str(self.queue))