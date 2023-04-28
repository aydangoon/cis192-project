
"""
Object for setting, organzing and getting user data
"""
class UserData:
    def __init__(self):
        pass
    def __str__(self):
        pass

    """
    Sets the User Data profile info, such as user icon, name, etc. based
    on the response from the spotify api client.

    Args:
        profile_res (dict): Spotify API client response for getting a user's profile

    Returns: None
    """
    def set_profile(self, profile_res):
        pass

    """
    Sets the User Data top items such as albums, artists, genres, etc. based
    on the response from the spotify api client.

    Args:
        top_items_res (dict): Spotify API client response for getting a user's top items

    Returns: None
    """
    def set_top_items(self, top_items_res):
        pass
    
    """
    Compare this UserData object with another UserData object. Returns the results as a
    dict.

    Args:
        other (UserData): other UserData to compare with

    Returns: dict with keys:
        TODO will determine exact metrics later
    """
    def compare_with(self, other):
       pass 
