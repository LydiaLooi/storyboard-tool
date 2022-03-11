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
    
    try:
        outfile.write(HEADER)
        map.write_map(outfile)
        outfile.write(FOOTER)
        outfile.close()
    except Exception as e:
        print_banner("An error has occured...\n" + str(e))
    
    input("\nPress enter to exit...")

if __name__ == "__main__":
    main()