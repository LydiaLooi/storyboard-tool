def write_sprite_header(outfile, sprite):
    """
    Writes the header line to declare a sprite
    """    
    outfile.write(f'Sprite,Foreground,Centre,"{sprite}",320,240\n')

def write_fade(outfile, startTime, endTime, startFade, endFade):
    """
    Writes the line to fade a sprite
    """
    outfile.write(f" F,0,{startTime},{endTime},{startFade},{endFade}\n")
    
    
def write_move(outfile, startTime, endTime, startX, startY, endX, endY):
    """
    Writes the line to move a sprite
    """
    outfile.write(f' M,0,{startTime},{endTime},{startX},{startY},{endX}, {endY}\n')
    
def write_scale(outfile, startTime, endTime, startScale, endScale):
    """
    Write the line to scale a sprite
    """
    outfile.write(f' S,0,{startTime},{endTime},{startScale},{endScale}\n')

def write_vertical_flip(outfile):
    """
    Write the line to flip a sprite vertically
    """
    outfile.write(f' P,0,0,,V\n')
    
def write_vertical_scale(outfile, startTime, endTime, startScale, endScale):
    """
    Write the line to scale a sprite
    """
    outfile.write(f' V,0,{startTime},{endTime},{startScale},{endScale}\n')    