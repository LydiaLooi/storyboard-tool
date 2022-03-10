from typing import List
from constants import SCROLL

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Path():
    def __init__(self):
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

    def get_start_time_diff(self, note):
        # How early should the note spawn before when it hits the receptors
        return int(abs(self.start_coords[note.column_index].y - self.end_coords[note.column_index].y) / SCROLL)

    
    def get_start(self, lane_index: int) -> Coord:
        return self.start_coords[lane_index]

    def get_end(self, lane_index: int) -> Coord:
        return self.end_coords[lane_index]
