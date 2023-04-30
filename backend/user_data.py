
"""
Object for setting, organzing and getting user data
"""
class UserData:
    def __init__(self, data):
        self.name = data["display_name"]
        self.country = data["country"]
        self.pfp_url = data["images"][0]["url"]
    def __str__(self):
        pass

    def set_top_artists(self, artists):
        self.top_artists = [ artist["name"] for artist in artists ]

    def set_top_tracks(self, tracks):
        self.top_tracks = [track["name"] for track in tracks]

    def set_top_genres(self, artists):
        genres = [[genre for genre in artist["genres"]] for artist in artists]
        genres = [genre for sublist in genres for genre in sublist]
        self.top_genres = {genre: genres.count(genre) for genre in genres}
        # sort genres by count
        self.top_genres = {k: v for k, v in sorted(self.top_genres.items(), key=lambda item: item[1], reverse=True)}
        # convert to list of just genres but in sorted order
        self.top_genres = list(self.top_genres.keys())
    """
    Compare this UserData object with another UserData object. Returns the results as a
    dict.

    Args:
        other (UserData): other UserData to compare with

    Returns: dict with keys:
        TODO will determine exact metrics later
    """
    def compare_with(self, other):
       # find any shared artists between this and other
        shared_artists = [artist for artist in self.top_artists if artist in other.top_artists]
        # find any shared genres between this and other
        shared_genres = [genre for genre in self.top_genres if genre in other.top_genres][:50]
        # find any shared tracks between this and other
        shared_tracks = [track for track in self.top_tracks if track in other.top_tracks]
        match_percentage = 100 * ((len(shared_artists) + len(shared_genres) + len(shared_tracks)) / 150)
        return {
            "percentage": match_percentage,
            "top_artist": shared_artists[0] if len(shared_artists) > 0 else 'null',
            "top_track": shared_tracks[0] if len(shared_tracks) > 0 else 'null',
            "top_genre": shared_genres[0] if len(shared_genres) > 0 else 'null',
        }

    def to_dict(self):
        return {
            'name': self.name,
            'country': self.country,
            'pfp_url': self.pfp_url
        }
