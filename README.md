# Playlists_conversions

Converts iTunes playlists to Ubuntu RhythmBox playlists.
- iTunes from c. 2016, RhythmBox on Ubuntu 22.
- iTunes playlists exported to xml and copied to ./ .
- In 'Convert-playlists.py', replace:
    - the path to where the files are saved on Ubuntu (L.14);
    - the name of the first playlist (L.27).
- Automatically sorts the changes to track pathnames and occasionally names.
- Creates .xml of playlists that can be loaded into RhythmBox (can be quite slow to load).

The iTunes playlists .xml file I put through this is over 64,000 lines:
- track IDs, information and file paths (information extracted);
- iTunes automatic playlists (e.g., most played) (ignored);
- my structured playlists (what want to extract to RhythmBox) (information extracted).

This is only something one uses once so there's no attempt at optimisation.
