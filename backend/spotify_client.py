from user_data import UserData

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
def authorize(client_id: str):  
    pass

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
def reauthorize(refresh_token: str):  
    pass

"""
Make multiple requests to Spotify API to get all the listening information of a user.

Args:
    access_token (str): The access token or the authenticated user to retrieve listening information of.

Returns: UserData object which contains all the user's relevant listening information.
"""
def get_user_data(access_token: str) -> UserData:
    pass