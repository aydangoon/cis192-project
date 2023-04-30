import base64
from user_data import UserData
import json
from flask import request
import urllib.parse
import requests
import os

CLIENT_ID = '4d3f871c854b41d1ac57aa40321a98cf'
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SCOPE = 'user-read-private user-read-email'
AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
FRONTEND_URL = "http://localhost:3000/"

def get_connect_account_url():
    """
    Return the url that the frontend should redirect the user to in order to connect their Spotify account.

    Returns:
        url (str): the url that the frontend should redirect the user to in order to connect their Spotify account.
    """
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": FRONTEND_URL,
        "scope": SCOPE
    }
    query_string = urllib.parse.urlencode(params)
    return AUTHORIZE_URL + "?" + query_string

def authorize(code):  
    """
    Wrapper for all interactions with the spotify API.
    """

    """
    Authorize a user through Spotify.

    Args:
        client_id (str): the id of the client to authorize.

    Returns: dict with keys:
        access_token (str): spotify access token
        token_type (str): access token allowance type
        scope (str): A space-separated list of scopes which have been granted for this access_token
        expires_in (int): time period in seconds before token expires
        refresh_token (str): token that can be sent before expiration of current access_token in order
        to acquire a new one
    """
    body_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": FRONTEND_URL,
    }
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode('utf-8'))
    auth_header_value = client_creds_b64.decode('utf-8')
    headers = {
        "Authorization": f"Basic {auth_header_value}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    body = urllib.parse.urlencode(body_params)
    res = requests.post(TOKEN_URL, headers=headers, data=body)
    if (res.status_code != 200):
        print('Error:', res.text)
    return json.loads(res.text)



def reauthorize(refresh_token: str):  
    """
    Reauthorize a user through Spotify whose current access token is about to expire.

    Args:
        refresh_token: the refresh token of the user

    Returns:
        access_token (str): spotify access token
        token_type (str): access token allowance type
        scope (str): A space-separated list of scopes which have been granted for this access_token
        expires_in (int): time period in seconds before token expires
    """
    pass

def get_user_data(access_token: str) -> UserData:
    """
    Make multiple requests to Spotify API to get all the listening information of a user.

    Args:
        access_token (str): The access token or the authenticated user to retrieve listening information of.

    Returns: UserData object which contains all the user's relevant listening information.
    """
    pass