# youtube-playlist-snapshot
Ever cataloged youtube videos with a Youtube playlist, only to one day encounter the dreadful message, "One or more videos have been removed from the playlist because they were deleted from YouTube."? Did you then find yourself cursing the sky, shouting "WHICH ONES, YOUTUBE? WHICH ONES!?"

This is a utility for that. Use it to snapshot the contents of your youtube playlists. If you run it again and a video is missing, it will bring it to your attention.

## Usage

    snapshot.py [playlistID...]
All videos will be indexed in "plists.xml". If you run the script with no playlist ID parameter(s), it will snapshot the playlists already present in "plists.xml".
