# Playlists_conversions

Convert iTunes playlists to Ubuntu RhythmBox playlists.
(Used for iTunes from c. 2016 to RhythmBox on Ubuntu 22.)
Since this is only something one uses once, there's no attempt at optimisation or elegance.

Usage instructions (main probable edits are flagged, but do check carefully):
- iTunes playlists exported to .xml and copied to ./ .
- Copy RythmBox tracklist (.pls) to ./ .
- In 'Convert-playlists.py', replace:
    - the path to where the files are saved on Ubuntu (L.14);
    - the name of the RythmBox tracklist (L.17);
    - the name of the first playlist (L.27);
    - the name of the iTunes playlist file (L.30);
    - comment out or update td.remove_ALW (L.34).
         -> in 'tidy.py', 'remove_ALW' removes tracks whose name/path includes ''Lloyd'';
          may want to generalise so specify key part of track name as part of module input.
- In 'iTunes_extraction.py' check path stem (in 'extract_iTunes_loc') and playlist delimiters (in 'create_itunes_lists').

Description:
- Reads in RythmBox track names .pls file.
- Reads in iTunes playlists .xml file (mine was over 64,000 lines), with rough structure:
    - track IDs, information and file paths (information extracted);
    - iTunes' automatic playlists (e.g., most played) (ignored);
    - my structured playlists (what want to extract to RhythmBox) (information extracted).
- Automatically sorts the changes to track pathnames and occasionally names.
- Creates .xml of playlists that can be loaded into RhythmBox (can be quite slow to load).
