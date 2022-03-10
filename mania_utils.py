from collections import namedtuple
from typing import List
from constants import COL1, COL2, COL3, COL4, SPRITE_FILE
from storyboard_functions import *


Coord = namedtuple("Coord", "x y")

MAGIC = 13720 # Literal magic number
RAW_SCROLL = 20
SCROLL = 480 / (MAGIC / RAW_SCROLL)



class Path():
    def __init__(self, lane_index: int):
        self.start_coords: List["Coord"] = [
            Coord(410, -1000), 
            Coord(440, -1000), 
            Coord(470, -1000), 
            Coord(500, -1000)]
        self.end_coords: List["Coord"] = [
            Coord(410, 400), 
            Coord(440, 400), 
            Coord(470, 400), 
            Coord(500, 400)]
        self.lane_index = lane_index

    @property
    def start_time_diff(self):
        # How early should the note spawn before when it hits the receptors
        return int(abs(self.start_coords[self.lane_index].y - self.end_coords[self.lane_index].y) / SCROLL)

    @property
    def start(self) -> Coord:
        return self.start_coords[self.lane_index]

    @property
    def end(self) -> Coord:
        return self.end_coords[self.lane_index]


class Note:
    def __init__(self, hit_time: int, column_number: int, tail_time: int=None, path: Path=None):
        self._hit_time: int = hit_time
        self._tail_time: int = tail_time
        self._column_number: int = column_number
        self._path: Path = path

    @property
    def column_index(self):
        if self._column_number == COL1:
            return 0
        elif self._column_number == COL2:
            return 1
        elif self._column_number == COL3:
            return 2
        elif self._column_number == COL4:
            return 3
        else:
            raise Exception("Weird column number? {}".format(self._column_number))

    def set_tail_time(self, time: int):
        self._tail_time = time

    def write_path(self, outfile):
            write_sprite_header(outfile, SPRITE_FILE)
            write_move(
                outfile, 
                self._hit_time - self._path.start_time_diff, 
                self._hit_time, 
                self._path.start.x, self._path.start.y, 
                self._path.end.x, self._path.end.y)
            write_vector_scale(
                outfile, 
                self._hit_time - self._path.start_time_diff, 
                self._hit_time, 
                30, 10)

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

    def add_note(self, note: Note, path: Path=None):
        if path is None:
            path = Path(note.column_index)
        note._path = path
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


    def print_map(self):
        gap = 200

        working_row = [" "," "," "," "]
        working_time = None

        time_since_last_row = 0

        for i in range(len(self.notes) - 1, -1, -1):
            # print(self.notes[i])
            note = self.notes[i]

            if working_time is not None and working_time != note._hit_time:
                # print(working_row)
                s = ""
                for i in working_row:
                    s += i
                print(s)
                working_row = [" "," "," "," "]
                time_since_last_row = note._hit_time - working_time

                gaps = abs(time_since_last_row // gap)
                # print(f"{time_since_last_row}, {time_since_last_row % gap}, {gaps}")
                for i in range(gaps):
                    print()

            if working_time != note._hit_time:
                working_time = note._hit_time
            
            if note._tail_time:
                working_row[note.column_index] = "□"
            else:
                working_row[note.column_index] = "■"

    def write_map(self, outfile):
        for note in self.notes:
            note.write_path(outfile)