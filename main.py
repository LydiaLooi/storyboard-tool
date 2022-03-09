from constants import *
from mania_utils import Map, Note, Path
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DIFF = config["Map"]["Difficulty"]
FILEPATH = config["Map"]["Filepath"]
MAPNAME = config["Map"]["Mapname"]



def process_notes(note_rows):
    """
    Takes the list of tuples of note data and processes it into a dictionary of
    processed notes.
    
    Will check for 'purple notes'
    
    Key: Integer of the millisecond time
    Value: List of tuples with information of each note
    
    (start, end, col, note, length)
    start:    Start time of when the note should spawn in
    end:      End time of when the note should disappear. (The hit-time)
    col:      The x-position that the note should be at
    note:     The file name of the note sprite to be used
    length:   The length of the note in milliseconds or None if it's a rice note
    
    """
    processed_notes = {}
    for time in note_rows:
        if time not in processed_notes:
            processed_notes[time] = []

        if len(note_rows[time]) == 1: # There is only one note at the particular time there is no need to check for purple notes
            start, end, col, note, length = note_rows[time][0]
            if length == None:
                processed_notes[time] = note_rows[time]
            else:
                processed_notes[time].append((start, end, col, note, length)) # head

        else:
            for note in note_rows[time]:
                start, end, col, note_file, length = note
                                
                
                # if should_be_purple(note, note_rows[time]) and note not in processed_notes[time]:
                #     if (not already_exists_as_purple(note, processed_notes[time])):
                #         processed_notes[time].append((start, end, col, NOTE_P, length))
                # else:
                #     if length == None:
                #         if (start, end, col, NOTE_P, length) not in processed_notes[time]:
                #             processed_notes[time].append((start, end, col, note_file, length))
                #     else:
                #         processed_notes[time].append((start, end, col, note_file, length))     


    return processed_notes

def print_banner(message):
    """
    Simple method that sandwiches the message in between two lines of '=' symbols.
    """
    print("=" * 60)
    print(message)
    print("=" * 60)

def setup(filepath: str, map_name: str, diff: str):
    map: Map = Map(filepath, map_name, diff)

    print_banner(f"Processing {map.filename}")

    try:
        map.process_and_set_note_lines()
    except Exception as e:
        print(f"\nCould not read '{map.filename}' : \n{e}\n")
        input("\nPress enter to exit...")
        
        sys.exit()

    map.process_notes()

    return map

def main():

    map = setup(FILEPATH, MAPNAME, DIFF)
    
    map.print_map()
    


    # try:
    #     processed_notes = process_notes(map)
    #     # print(processed_notes)
    # except Exception as error:
    #     print_banner("An error has occured...\n" + str(error))
    #     print("Conversion stopped. osb file not written.")
    #     input("\nPress enter to exit...")
    #     sys.exit()
    # write_osb_file(processed_notes, OUTPUT)

    # print_note_stats(note_rows)

    # print_banner(f"'{OUTPUT}' file written!")
    # print_finished_info()
    input("\nPress enter to exit...")

if __name__ == "__main__":
    main()