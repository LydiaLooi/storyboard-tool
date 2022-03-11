from constants import *
from mania_utils import Map
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DIFF = config["Map"]["Difficulty"]
FILEPATH = config["Map"]["Filepath"]
MAPNAME = config["Map"]["Mapname"]


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
    
    outfile = open(f"{OUTPUT_DIR}{MAPNAME}.osb", 'w')
    
    outfile.write(HEADER)
    map.write_map(outfile)
    outfile.write(FOOTER)

    outfile.close()
    # map.print_map()
    
    print()


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