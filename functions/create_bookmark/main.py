from datetime import datetime
import firebase_admin
from firebase_admin import firestore
import flask
import flask.typing
import functions_framework

@functions_framework.http
def create_bookmark(request: flask.Request) -> flask.typing.ResponseReturnValue:
    # Initialize Firebase Admin SDK if not already initialized
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app()
    
    # Set the CORS headers
    headers = {"Access-Control-Allow-Origin": "*"}
    if request.method == "OPTIONS":
        headers.update({
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        })
        return ("", 204, headers)

    if request.method != "POST":
        return ("", 405, headers)
    
    request_json = request.get_json()
    url = request_json.get("url")
    if not url:
        return ({"error": "'url' not provided"}, 400, headers)
    
    save_bookmark(url)

    return ({"message": f"Bookmark saved: {url}"}, 201, headers)


def save_bookmark(url: str):
    bookmark = {
        "url": url,
        "timestamp": datetime.now(),
        "digested": False,
    }
    db = firestore.client()
    db.collection("bookmarks").add(bookmark)