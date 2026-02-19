"""
Remove tracks not interested in, replace track IDs with paths in playlists.
Unused: split paths into segments.
"""

def remove_ALW(track_lists):
    """ Run through iTunes backwards and get rid of ALW stuff. """
    length = int(len(track_lists))-1
    for i in range(length, -1, -1):
        if "Lloyd" in track_lists[i][3]:
            #print('removing: ', track_lists[i][3])
            track_lists.pop(i)
    return track_lists

def pl_as_it_paths(playlist, it_dict):
    """ Replace iTunes IDs with paths (in list of playlists).
    Uses dictionary of iTunes IDs and iTunes paths (it_dict). """
    pl_it_tracks = [[track, it_dict.get(track, track)] for track in playlist]
    return pl_it_tracks

def split_paths(track_lists, loc):
    """ Split paths into list of folders/files according to '/'.
    loc is the location of the path in the information list for each track.
    """
    paths = []
    for i, track in enumerate(track_lists):
        track_path = track[loc].split('/')
#        print(track_path)
        paths.append(track_path)
    return paths
