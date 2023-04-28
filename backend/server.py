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
import base64

user_data = pd.DataFrame(columns=["user_id", "access_token", "refresh_token", "user_data", "expires", "accepted_invites"])
app = Flask(__name__)

def hash(s):
    return base64.b64encode(hashlib.sha256(s+"salt_string".encode()).digest()).decode('utf-8')[:16]

@app.route('/', methods=["GET"])
def home_page():
    """
    Check if the user has authenticated with Spotify yet. If not, the frontend will
    render a button prompting the user to authenticate, otherwise it will give the user
    the option to invite others to the match.

    Returns { authenticated: bool }
    """
    access_token = request.cookies.get("access_token")
    if access_token is None:
        return jsonify({ "authenticated": False })
    user_id = hash(access_token)
    user_exists = user_data['user_id'] == user_id
    return jsonify({ "authenticated": user_exists.any() })


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

if __name__ == '__main__':
    app.run(debug=True, port=8000)