from constants import *

def read_file(filename):
    """
    Parses the give .osu file and returns a list of all the hitobject lines.
    """
    start = False
    infile = open(filename, 'r')
    lines = infile.readlines()
    note_lines = []
    
    for line in lines:
        line = line.strip("\n");
        if start is True:
            note_lines.append(line)
        elif line == "[HitObjects]":
            start = True

    infile.close()
    
    print(f"{len(note_lines)} total notes")
    
    return note_lines

def process_line(line, note_rows):
    """
    Processes the given hitobject line and parses it to be added to the note_rows
    list.
    
    The following tuple is what is added to the note_rows list:
    (start, end, column, note, length)
    
    start:    Start time of when the note should spawn in
    end:      End time of when the note should disappear. (The hit-time)
    column:   The x-position that the note should be at
    note:     The file name of the note sprite to be used
    length:   The length of the note in milliseconds or None if it's a rice note
    """
    col, _, end, _, _, extra = line.split(",")
    end = int(end)
    col = int(col)

    column = NOTE_DATA[col][COLUMN]
    note = NOTE_DATA[col][NOTE]
    ln = NOTE_DATA[col][LN]
    cap = NOTE_DATA[col][CAP]


    start = end - START_BUFFER

    extra = extra.split(":")


    if end not in note_rows:
        note_rows[end] = []


    if len(extra) > 5:
        tail = int(extra[0])
        length = tail - end
        note_rows[end].append((start, end, column, note, length))

    else:
        note_rows[end].append((start, end, column, note, None))


    return note_rows