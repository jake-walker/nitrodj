from flask import Blueprint, jsonify, g
import search
import os

api = Blueprint("api", __name__, url_prefix="/api")
searcher = search.Searcher(api_key=os.environ["NITRO_YOUTUBE_KEY"])


@api.route("/queue", methods=["GET"])
def get_queue():
    queue = g.queue.get_queue()
    return jsonify(queue)


@api.route("/queue/add/<id>", methods=["GET"])
def add_to_queue(id):
    g.queue.add_song(id)
    return "OK"


@api.route("/search/<query>", methods=["GET"])
def get_search_results(query):
    query = query.strip().lower()
    return jsonify(searcher.query(query))