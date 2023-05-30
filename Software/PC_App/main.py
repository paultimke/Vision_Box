# Import Libraries
from typing import List
import sys
import constants as cnst
import takeFunction as parser
import find_object as fOBJ

# Flag indicating if debugg mode
DEBG = False

def is_CLI_args_valid(args: List[str]) -> bool:
    return len(args) == 2

#-------------------MAIN FUNCTION-------------------#
def main():  
    # Get command line arguments
    command_args = None
    if is_CLI_args_valid(sys.argv):
        command = parser.callFunction(sys.argv[1])
        if command.check():
            command_args = command.parse()

    # Initialize cam port
    cam_port = "Testing/screens_cam18/T03_cam_18.png" #''cnst.DEFAULT_CAM_PORT

    # Call corresponding command
    match command_args:
        # TODO: Add suport for HELP, EXAMPLE and SETLIGHT commands
        case ('TESTSTATUS', condition):
            pass
        case ('FTEXT', text):
            pass
        case ('FICON', path):
            # Acceptance match threshold before refactor was on 50, although
            # the default is 95
            fOBJ.mainly(cam_port, path, DEBG)
        case ('COMPIMAGE', path):
            pass
        case _:
            # Log error message of unrecognized command
            pass

if __name__ == "__main__":
    main()