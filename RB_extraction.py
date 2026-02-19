""" Extract rhythmbox track information (compare on paths). """

import re # this is for string slicing on known flags

def extract_rb_text(line):
    """ Extract text information from a line of a rhythmbox xml file. """
    delims = r"=(.*?)\n"
    text = re.findall(delims, line)[0]
    return text

def extract_rb_key(line):
    """ Extract rhythmbox track number (not actually needed). """
    delims = r"File(.*?)="
    text = re.findall(delims, line)[0]
    return text

def rb_extract_info(file, pathstem, rb_track_list):
    """ Extract information about tracks from a rhythmbox xml file. """
    info = []
    for line in file:
        if "File" in line:
            path = extract_rb_text(line)
            fullpathstem = "file://" + pathstem
            # take out start of path name, so can compare paths
            path = re.sub(fullpathstem, "", path)
            key = extract_rb_key(line)
            info.append(key)
            info.append(path)
        if "Title" in line:
            title = extract_rb_text(line)
            info.append(title)
        if len(info) == 3:
            #print(info)
            rb_track_list.append(info)
            info = []
    return rb_track_list
