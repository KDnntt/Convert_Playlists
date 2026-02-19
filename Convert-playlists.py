""" Turn iTunes playlists into rhythmbox playlists """

import sys
#import re # this is for string slicing on known flags
from fuzzywuzzy import fuzz

# my modules in separate files
import iTunes_extraction as itx
import RB_extraction as rbx
import tidy as td
import create_playlists as cpl

#---------------------------------------------------------------------------
rb_pathstem = '/path/to/folder/ends/Music/'

# get list of tracks in rhythmbox [rb_id, rb_path, rb_title]
with open('RB-All.pls', 'r', encoding='utf-8') as f:
    rb_tracks = []
    rbx.rb_extract_info(f, rb_pathstem, rb_tracks)

#---------------------------------------------------------------------------
# get list of tracks [iTunes_id, iTunes_track_name, iTunes_album, iTunes_path]
itunes_tracks = []
# get list of iTunes playlists [playlist names, track 1 ID, track 2 ID,...]
playlists = []

first_playlist = 'Abel Cello Concerto' # 'Name of first iTunes playlist'

# Read in iTunes xml as list
with open('iTunes-PlaylistsLibrary.xml', 'r', encoding='utf-8') as f:
    itx.create_itunes_lists(f, first_playlist, playlists, itunes_tracks)

# remove tracks not at all interested in
td.remove_ALW(itunes_tracks)

# create dictionary of iTunes track ID and file path
it_paths_dict = {itunes_tracks[i][0] : itunes_tracks[i][3] for i, n in enumerate(itunes_tracks)}

#---------------------------------------------------------------------------
# compare the number of tracks with the number of tracks in playlists.
#print(sum(len(v) for v in playlists))

# create list of playlists with iTunes file paths and ID numbers
pl_w_tracks = []
for p, pl in enumerate(playlists):
    pl_it_tracks = td.pl_as_it_paths(pl, it_paths_dict)
    pl_w_tracks.append(pl_it_tracks)

#print(pl_w_tracks[8])

# find most likely file path matches for a playlist (and return full info as probable)
# for some reason, runs quickly when here, but not as module
probable_pls = []
#pl = pl_w_tracks[8]
for p, pl in enumerate(pl_w_tracks):
    probable = pl[0]
    for i in range(1, len(pl)):
        #print(pl[i])
        str1 = pl[i][1]
        high_sim = 0
        # for each playlist item, create list: [[iTunes ID, iTunes path], rb_path, similarity]
        for j, m in enumerate(rb_tracks):
            str2 = m[1]
            sim = fuzz.ratio(str1.lower(), str2.lower())
            if sim > high_sim:
                high_sim = sim
                probable_rb_track = m[1]
        probable.append([pl[i], probable_rb_track, 'sim = ' + str(high_sim)])
    probable_pls.append(probable)

# each item in probable_pls is a playlist
# [playlist name (twice, for some reason), track 1 info, track 2 info etc.]
# where track info is [[iTunes ID, iTunes path], rb path, similarity of iTunes and rb paths]
#print(len(probable_pls[92]), probable_pls[92])
#print(len(probable_pls[-1]), probable_pls[-1])

# and now, having got all the paths matched up, can just print rb_playlists.
#print(len(probable_pls))

# no point in modularising...
# get first and last parts of rb xml file from example
with open('RB-Playlist.xml', 'r') as infile:
    start = []
    end = []
    follow = 0
    for line in infile:
        if follow == 0 and 'type="static"' in line:
        # stop adding to write at start
            #print('hit static playlists')
            follow = 1

        if follow == 0:
        # add line to stuff to write at start
            start.append(line)

        if follow == 1 and 'Play Queue' in line:
            follow = 2
            end.append(line)
        if follow == 2 and 'Play Queue' not in line:
            end.append(line)

#print(start, end)

## write to output file
with open('rb-test.xml', 'w') as outf:
    for i, l in enumerate(start):
        outf.write(l)
    for pl, playlist in enumerate(probable_pls):
        cpl.write_plist(playlist, rb_pathstem, outf)
    for i, l in enumerate(end):
        outf.write(l)

## and now, just copy to the correct place... e.g. ~/.local/share/rhythmbox/playlists.xml

#---------------------------------------------------------------------------
sys.exit()
