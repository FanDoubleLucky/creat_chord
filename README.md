# creat_chord
OMR preprocessing with chord scores
Firstly, a random note musicxml is downloaded from http://randomsheetmusic.lasconic.com.
The first step is modifying the musicxml file. The addTie.py, addClef_Key_Slur.py and addBarline.py
can add notation, accidental, clef, key, chord elements into the original musicxml file. The output of this step is a new musicxml.
The second step is exporting PNG files from the new musicxml an the MuseSocre can finish the work. The output of this step is PNGs.
The next step is segmentation. The segment_line_random_paste.py can segments one whole PNG into some pictures by staff lines. And 
the segment_measure.py can segments one whole PNG into some pictures by every measure but this procedure need the corresponding muisicxml.
The final step extracts the corresponding label information for every line picture. The output of this step is CSV files.
