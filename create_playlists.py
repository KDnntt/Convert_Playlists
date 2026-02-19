""" Write playlists properly formatted for rhythmbox (note whitespaces). """
import re # this is for string slicing on known flags

def write_plist_name(pname, outfile):
    """ Write playlist name (properly formatted) to rb .xml file. """
    outfile.write('  <playlist name="'+str(pname)+
    '" show-browser="true" browser-position="190" search-type="search-match" type="static">\n')

def write_track_loc(track_loc, pathstem, outfile):
    """ Write track location properly formatted to rb .xml file.
        Includes restoring the full path.
    """
    if '&' in track_loc:
        track_loc = re.sub(r'(&)', '&amp;', track_loc)
    outfile.write('    <location>file://' + pathstem + track_loc + '</location>\n')

def write_plist(plist, pathstem, outfile):
    """ Write playlist to rb .xml file."""
    pname = plist[0]
    write_plist_name(pname, outfile)
    #print(len(plist))
    for i in range(2, len(plist)):
        track_loc = plist[i][1]
        #print(track_loc)
        write_track_loc(track_loc, pathstem, outfile)
    # and end the playlist!!
    outfile.write('  </playlist> \n')
