'''
Backend code. 

1. Sets up flask server.
2. Defines routes and route handlers.
3. Launches server on local port.

The backend will store a pandas dateframe of Spotify authenticated users and the
state of their pending/complete matches with other spotify authenticated users.
'''
from flask import Flask, request, jsonify
import pandas as pd
import hashlib
import time
import base64
from flask_cors import CORS, cross_origin
import spotify_client as sc

user_data = pd.DataFrame(columns=["user_id", "access_token", "refresh_token", "user_data", "expires", "accepted_invites"])
matches = pd.DataFrame(columns=["id", "host", "guest"])
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def hash(s):
    salt_string = 'salt_string'.encode()
    hash_object = hashlib.sha256(s.encode() + salt_string)
    hash_bytes = hash_object.digest()
    hash_b64 = base64.b64encode(hash_bytes)
    hash_str = hash_b64.decode('utf-8')
    return hash_str[:16]

@app.route('/', methods=["GET"])
def home_page():
    """
    Check if the user has authenticated with Spotify yet. If not, the frontend will
    render a button prompting the user to authenticate, otherwise it will give the user
    the option to invite others to the match.

    Returns { authenticated: bool }
    """
    sid = request.args.get("sid")
    if (sid == "null"):
        return jsonify({ "authenticated": False })
    user_exists = user_data['user_id'] == sid
    user_exists = True if user_exists.any() else False
    return jsonify({ "authenticated": user_exists })


@app.route('/match', methods=["GET"])
def match_page():
    """
    Takes two users, host and guest then:
    1. Queries the spotify API for their data.
    2. Generates their match data.
    3. Returns formatted, clean match data.

    Returns { match_data: { ... }}
    """
    pass

@app.route('/connect_account', methods=["GET"])
def connect_account():
    return jsonify({ "redirect_url": sc.get_connect_account_url() })

@app.route('/authorize', methods=["GET"])
@cross_origin()
def authorize():
    code = request.args.get("code")
    data = sc.authorize(code)
    user = {
        "user_id": hash(data["access_token"]),
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "user_data": None,
        "expires": data["expires_in"] + int(time.time())
    }
    global user_data
    user_data.loc[len(user_data)] = user
    res = jsonify({ "sid": user["user_id"] })
    return res 

if __name__ == '__main__':
    print(sc.CLIENT_ID, sc.CLIENT_SECRET)
    app.run(debug=True, port=8000)