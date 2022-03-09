from typing import List

class Path:
    def __init__(self):
        pass


class Note:
    def __init__(self, hit_time: int, column_number: int, tail_time: int=None, path: Path=None):
        self._hit_time: int = hit_time
        self._tail_time: int = tail_time
        self._column_number: int = column_number
        self._path: Path = path

    def set_tail_time(self, time: int):
        self._tail_time = time

    def __str__(self):
        return f"{self._hit_time}, {self._column_number}, {self._tail_time}"
    
    def __repr__(self):
        return f"{self._hit_time}, {self._column_number}, {self._tail_time}"

class Map:
    def __init__(self, file_path: str, map_name: str, difficulty_name: str):
        self._file_path: str = file_path
        self._map_name: str = map_name
        self._difficulty_name: str = difficulty_name
        self._note_lines: List[str] = None
        self._notes: List["Note"] = []

    def process_and_set_note_lines(self):
        try:
            self._note_lines = self.read_file()
        except Exception as e:
            raise

    @property
    def filename(self):
        return f"{self._file_path}{self._map_name} [{self._difficulty_name}].osu"

    def add_note(self, note: Note):
        self._notes.append(note)

    @property
    def note_lines(self):
        return self._note_lines

    @property
    def notes(self):
        return self._notes

    def read_file(self):
        """
        Parses the give .osu file and returns a list of all the hitobject lines.
        """
        start = False
        infile = open(self.filename, 'r')
        lines = infile.readlines()
        note_lines = []
        
        for line in lines:
            line = line.strip("\n")
            if start is True:
                note_lines.append(line)
            elif line == "[HitObjects]":
                start = True

        infile.close()
        
        print(f"{len(note_lines)} total notes")
        
        return note_lines

    def process_notes(self):
        for line in self.note_lines:
            self.process_line(line)


    def process_line(self, line):
        """
        Processes the given hitobject line and parses it to be added to the note_rows
        list.
        
        The following tuple is what is added to the note_rows list:
        (start, hit_time, column, note, length)
        
        start:    Start time of when the note should spawn in
        hit_time: Hit time of when the note should disappear.
        column:   The x-position that the note should be at
        note:     The file name of the note sprite to be used
        length:   The length of the note in milliseconds or None if it's a rice note
        """
        col, _, hit_time, _, _, extra = line.split(",")
        hit_time = int(hit_time)
        col = int(col)
        extra = extra.split(":")

        note: Note = Note(hit_time, col)

        if len(extra) > 5: # If is LN, else.
            tail = int(extra[0])
            note.set_tail_time(tail)

        self.add_note(note)