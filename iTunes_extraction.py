""" Extract track and playlist information from iTunes xml file. """
import re # this is for string slicing on known flags

def extract_iTunes_id(line):
    """ Extract extract Track ID number from a line of an iTunes xml file. """
    delims = r"integer>(.*?)</integer"
    identifier = re.findall(delims, line)
    return identifier

def extract_iTunes_name(line):
    """ Extract string (track, album or playlist title) from a line of an iTunes xml file. """
    delims = r"string>(.*?)</string"
    name = re.findall(delims, line)
    return name

def extract_iTunes_loc(line):
    """ Extract file path from a line of an iTunes xml file. """
    delims = r"Media/Music/(.*?)</string"
    loc = re.findall(delims, line)
    return loc

def extract_type(line):
    """ Extract file type (mp3 or m4a) from a line of an iTunes xml file. """
    if 'mp3' in line:
        ending = 'mp3'
    if 'm4a' in line:
        ending = 'm4a'
    return ending

def track_info(line, info):
    """ Put together information of each track needed for RB playlist. """
    # keep this as developed, even though actually using locations not info
    if 'Track ID' in line:
        info.append(extract_iTunes_id(line)[0])
#    if '>Album Artist<' in line:
    # causes problems because tracks can have have >Artist<, >Album Artist< or both.
    # but not of interest anyway...
#       info.append(extract_iTunes_name(line)[0])
    if '>Album<' in line:
        info.append(extract_iTunes_name(line)[0])
    if '>Name<' in line:
        info.append(extract_iTunes_name(line)[0])
    if '>Location<' in line:
#        info.append(extract_type(line))
        info.append(extract_iTunes_loc(line)[0])
    return info

def create_itunes_lists(file, first_playlist, playlists, track_lists):
    """ Extract playlists (names and track IDs) from iTunes xml file. """
    # integer for defining blocks of interest
    follow = 1
    info = []
    plist = []
    for line in file:
        # ignore playlists unless interesting ones (manual switches)
        # at start of Playlists - first few include all tracks
        if 'Playlists' in line:
            follow = 0
        # after my playlists
        if 'string>90’s' in line:
            follow = 0
            # append the last playlist to the full list!
            playlists.append(plist)
            # quit reading xml file, no more information of interest
            break
        # at first of my playlists
        if follow == 0 and first_playlist in line:
            follow = 2

        # pick up all track names and info (this all works perfectly)
        if follow == 1:
            track_info(line, info)
            # when track info complete, add to track_lists and reset info
            if len(info) == 4:
                track_lists.append(info)
                info = []

        # make lists of playlist name and Track IDs of tracks in playlist
        if follow == 2:
            if '>Name<' in line:
                # if have a playlist, append to list of playlists and reset
                if len(plist) >= 2:
                    playlists.append(plist)
                    plist = []
                # extract and add playlist name to (blank) playlist
                plist.append(extract_iTunes_name(line)[0])
            if 'Track ID' in line:
                # extract and add Track IDs to playlist
                plist.append(extract_iTunes_id(line)[0])
    return playlists, track_lists
