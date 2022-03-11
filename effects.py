from storyboard_functions import *
from constants import *

class Effect:
    def __init__(self):
        pass

    def write_effect(self, outfile, note):
        return

class DefaultNoteEffect(Effect):
    def write_effect(self, outfile, note):
        write_vector_scale(
                outfile, 
                note._hit_time - note._path.get_start_time_diff(note), 
                note._hit_time, 
                NOTE_WIDTH, NOTE_HEIGHT,
                NOTE_WIDTH, NOTE_HEIGHT)

class ScaleOutEffect(Effect):
    def write_effect(self, outfile, note):
        write_vector_scale(outfile, note._hit_time, note._hit_time + 100, NOTE_WIDTH, NOTE_HEIGHT, NOTE_WIDTH, 0)
        return super().write_effect(outfile, note)

class HiddenEffect(Effect):
    def write_effect(self, outfile, note):
        write_fade(outfile, note._hit_time - 350, note._hit_time - 250, 1, 0)
        return super().write_effect(outfile, note)


class FadeInEffect(Effect):
    def write_effect(self, outfile, note):
        write_fade(outfile, note._hit_time - 350, note._hit_time - 250, 0, 1)
        return super().write_effect(outfile, note)