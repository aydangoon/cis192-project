"""
Backend code. 

1. Sets up flask server.
2. Defines routes and route handlers.
3. Launches server on local port.

The backend will store a pandas dateframe of Spotify authenticated users and the
state of their pending/complete matches with other spotify authenticated users.
"""
from flask import Flask, request, jsonify
import pandas as pd
import hashlib
import time
import base64
import secrets
import string
from flask_cors import CORS, cross_origin
import spotify_client as sc

user_data = pd.DataFrame(
    columns=[
        "user_id",
        "access_token",
        "refresh_token",
        "user_data",
        "expires",
        "accepted_invites",
    ]
)
matches = pd.DataFrame(columns=["id", "host", "guest"])
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def hash(s):
    salt_string = "salt_string".encode()
    hash_object = hashlib.sha256(s.encode() + salt_string)
    hash_bytes = hash_object.digest()
    hash_b64 = base64.b64encode(hash_bytes)
    hash_str = hash_b64.decode("utf-8")
    return hash_str[:16]


def create_match_id():
    alphabet = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(alphabet) for _ in range(16))
    return random_string


@app.route("/", methods=["GET"])
def home_page():
    """
    Check if the user has authenticated with Spotify yet. If not, the frontend will
    render a button prompting the user to authenticate, otherwise it will give the user
    the option to invite others to the match.

    Returns { authenticated: bool }
    """
    sid = request.args.get("sid")
    if sid == "null":
        return jsonify({"authenticated": False})
    user_exists = user_data["user_id"] == sid
    user_exists = True if user_exists.any() else False
    return jsonify({"authenticated": user_exists})


@app.route("/match_state/<string:match_id>", methods=["GET"])
def match_state(match_id):
    """
    Checks the state of the match.
    Returns { match_data: { ... }}
    """
    global matches
    match = matches[matches["id"] == match_id]
    if match.empty:
        return jsonify({"state": "invalid", "reason": "no match with that id"})
    sid = request.args.get("sid")
    if sid == "null":
        return jsonify({"state": "invalid", "reason": "no sid given"})
    host = match["host"].iloc[0]
    guest = match["guest"].iloc[0]
    is_host = host == sid
    if is_host and guest is None:
        return jsonify({"state": "waiting"})
    elif not is_host and guest is None:
        matches.loc[matches["id"] == match_id, "guest"] = sid
        return jsonify({"state": "generating"})
    elif is_host and guest is not None:
        return jsonify({"state": "generating"})
    return jsonify({"state": "invalid", "reason": "no case matched"})


@app.route("/match/<string:match_id>", methods=["GET"])
def match(match_id):
    """
    Returns the match data for the given match id.
    """
    error = jsonify({"error": "there was an error"})
    match = matches[matches["id"] == match_id]
    if match.empty:
        return error
    host = match["host"].iloc[0]
    guest = match["guest"].iloc[0]
    if guest is None or host is None:
        return error
    host_access_token = user_data[user_data["user_id"] == host]["access_token"].iloc[0]
    guest_access_token = user_data[user_data["user_id"] == guest]["access_token"].iloc[
        0
    ]
    print("getting host data...")
    host_data = sc.get_user_data(host_access_token)
    print("getting guest data...")
    guest_data = sc.get_user_data(guest_access_token)
    comparison = host_data.compare_with(guest_data)
    return jsonify(
        {
            "host": host_data.to_dict(),
            "guest": guest_data.to_dict(),
            "match": comparison,
        }
    )


@app.route("/create_match", methods=["GET"])
def create_match():
    """
    Creates a match with the given match id.
    """
    # generate random match id
    match_id = create_match_id()
    sid = request.args.get("sid")
    if sid == "null":
        return jsonify({"error": "no user id"})
    global matches
    match = matches[matches["id"] == match_id]
    if not match.empty:
        return jsonify({"error": "match id already exists"})
    matches.loc[len(matches)] = {"id": match_id, "host": sid, "guest": None}
    print("create match:", {"id": match_id, "host": sid, "guest": None})
    return jsonify({"match_id": match_id})


@app.route("/connect_account", methods=["GET"])
def connect_account():
    return jsonify({"redirect_url": sc.get_connect_account_url()})


@app.route("/authorize", methods=["GET"])
@cross_origin()
def authorize():
    code = request.args.get("code")
    data = sc.authorize(code)
    user = {
        "user_id": hash(data["access_token"]),
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "user_data": None,
        "expires": data["expires_in"] + int(time.time()),
    }
    global user_data
    user_data.loc[len(user_data)] = user
    res = jsonify({"sid": user["user_id"]})
    return res


if __name__ == "__main__":
    print(sc.CLIENT_ID, sc.CLIENT_SECRET)
    app.run(debug=True, port=8000)
