from copy import deepcopy
from typing import List
from constants import *
from storyboard_functions import *
from path import Path
from effect import DefaultNoteEffect, Effect, ScaleOutEffect




class Note:
    def __init__(self, hit_time: int, column_number: int, tail_time: int=None, path: Path=None):
        self._hit_time: int = hit_time
        self._tail_time: int = tail_time
        self._column_number: int = column_number
        self._path: Path = path
        self._effects: List["Effect"] = [DefaultNoteEffect()]


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

    def get_note_length(self):
        if self._tail_time is None:
            raise Exception("Not an LN btw")
        return self._tail_time - self._hit_time

    def set_tail_time(self, time: int):
        self._tail_time = time

    def add_effect(self, effect: Effect):
        self._effects.append(effect)

    def write_ln(self, outfile):
        ln_scale = (abs(self._path.get_spawn_buffer(self) - self._path.get_hit_pos(self)) / self._path.get_start_time_diff(self)) # pixels per milisecond
        scale = self.get_note_length() * ln_scale
        
        write_sprite_header(outfile, SPRITE_FILE, origin="BottomCentre")

        write_vector_scale(
            outfile, 
            self._hit_time,
            self._hit_time + self.get_note_length(),
            NOTE_WIDTH, scale,
            NOTE_WIDTH, 0)


        write_move(
            outfile, 
            self._hit_time - self._path.get_start_time_diff(self), 
            self._hit_time, 
            self._path.get_start(self.column_index).x, self._path.get_start(self.column_index).y, 
            self._path.get_end(self.column_index).x, self._path.get_end(self.column_index).y)



    def write_note(self, outfile):
            write_sprite_header(outfile, SPRITE_FILE, origin="BottomCentre")
            
            write_move(
                outfile, 
                self._hit_time - self._path.get_start_time_diff(self), 
                self._hit_time, 
                self._path.get_start(self.column_index).x, self._path.get_start(self.column_index).y, 
                self._path.get_end(self.column_index).x, self._path.get_end(self.column_index).y)
            # Write effects e.g., fade in, fade out, flash light...
            for e in self._effects:
                e.write_effect(outfile, self)

            if self._tail_time is not None:
                self.write_ln(outfile)

            self._path.update_path()


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
            path = Path()
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

        customPath = Path()

        for line in self.note_lines:
            self.process_line(line, customPath)


    def process_line(self, line, customPath: Path = None):

        col, _, hit_time, _, _, extra = line.split(",")
        hit_time = int(hit_time)
        col = int(col)
        extra = extra.split(":")

        note: Note = Note(hit_time, col)

        note.add_effect(ScaleOutEffect())

        if len(extra) > 5: # If is LN, else.
            tail = int(extra[0])
            note.set_tail_time(tail)

        if customPath:
            self.add_note(note, customPath)
        else:
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
            note.write_note(outfile)