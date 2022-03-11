"""
https://osu.ppy.sh/wiki/en/Storyboard/Scripting/Commands
"""

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


def write_vector_scale(outfile, startTime, endTime, startScaleX, startScaleY, endScaleX=None, endScaleY=None, easing=0):
    """
    Write the line to vector scale a sprite
    """
    if endScaleX is None:
        endScaleX = startScaleX
    if endScaleY is None:
        endScaleY = startScaleY
    outfile.write(f' V,{easing},{startTime},{endTime},{startScaleX},{startScaleY}, {endScaleX}, {endScaleY}\n')