import pylast
from typing import Set, Tuple, Any
from domain import Track, Artist

if __name__ == '__main__':
    from decouple import config

    LAST_FM_API_KEY = config('LAST_FM_API_KEY')
    LAST_FM_API_SECRET = config('LAST_FM_API_SECRET')
    LAST_FM_USERNAME = config('LAST_FM_USERNAME')
    LAST_FM_PASSWORD_MD5 = pylast.md5(config('LAST_FM_PASSWORD'))

    network = pylast.LastFMNetwork(
        api_key=LAST_FM_API_KEY,
        api_secret=LAST_FM_API_SECRET,
        username=LAST_FM_USERNAME,
        password_hash=LAST_FM_PASSWORD_MD5,
    )

    library = pylast.Library(user='zurpz', network=network)
    user = library.get_user()

    i = 0

    tracklist :Set[Tuple[Track, Any]] = set()

    for played_track in user.get_recent_tracks(stream=True, limit=10):
        if i == 10:
            break

        last_fm_track = played_track.track

        artist = Artist(name= last_fm_track.artist)

        entity = Track(
            title= last_fm_track.title,
            length= float(last_fm_track.get_duration()),
            artists= [artist]
        )

        tracklist.add( (entity, last_fm_track) )

        i += 1

    for entity, last_fm_track in tracklist:
        entity.play_count= last_fm_track.get_userplaycount()

    from json import dumps

    print( dumps([ t.dump() for t, _ in tracklist ], default=str, indent=2) )

    # for library_item in library.get_artists(stream=True, limit=10):
    #     if i == 10:
    #         break

    #     artist :pylast.Artist = library_item.item

    #     i += 1