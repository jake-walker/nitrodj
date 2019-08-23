from youtube_api import YouTubeDataAPI

class Searcher:
    def __init__(self, api_key):
        self.yt = YouTubeDataAPI(api_key)

    def query(self, query):
        results = self.yt.search(query, topic_id="/m/04rlf", video_duration="short", safe_search="strict")
        output = []
        for result in results:
            output.append({
                "title": result["video_title"],
                "artist": result["channel_title"],
                "thumbnail": result["video_thumbnail"],
                "id": result["video_id"]
            })
        return output