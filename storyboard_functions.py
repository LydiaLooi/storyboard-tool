"""
https://osu.ppy.sh/wiki/en/Storyboard/Scripting/Commands
"""

class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def write_sprite_header(outfile, sprite, origin="Centre"):
    """
    Writes the header line to declare a sprite
    """    
    outfile.write(f'Sprite,Foreground,{origin},"{sprite}",320,240\n')

def write_fade(outfile, startTime, endTime, startFade, endFade, easing=0):
    """
    Writes the line to fade a sprite
    """
    outfile.write(f" F,{easing},{startTime},{endTime},{startFade},{endFade}\n")
    
    
def write_move(outfile, startTime, endTime, startX, startY, endX, endY, easing=0):
    """
    Writes the line to move a sprite
    """
    outfile.write(f' M,{easing},{startTime},{endTime},{startX},{startY},{endX}, {endY}\n')
    
def write_scale(outfile, startTime, endTime, startScale, endScale, easing=0):
    """
    Write the line to scale a sprite
    """
    outfile.write(f' S,{easing},{startTime},{endTime},{startScale},{endScale}\n')

def write_vertical_flip(outfile, easing=0):
    """
    Write the line to flip a sprite vertically
    """
    outfile.write(f' P,{easing},0,,V\n')
    
def write_vertical_scale(outfile, startTime, endTime, startScale, endScale, easing=0):
    """
    Write the line to scale a sprite vertically ... ?
    """
    outfile.write(f' V,{easing},{startTime},{endTime},{startScale},{endScale}\n')    


def write_vector_scale(outfile, startTime, endTime, startScaleX, startScaleY, endScaleX, endScaleY, easing=0):
    """
    Write the line to vector scale a sprite
    """
    outfile.write(f' V,{easing},{startTime},{endTime},{startScaleX},{startScaleY},{endScaleX},{endScaleY}\n')

def write_colour(outfile, startTime, endTime, start: RGB, end: RGB, easing=0):
    """The virtual light source colour on the object. The colours of the pixels on the object are determined subtractively."""
    outfile.write(f' C,{easing},{startTime},{endTime},{start.r},{start.g},{start.b},{end.r},{end.g},{end.b}')