import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import threading
import sys
import time
import cv2
import takeFunction as parser
import constants as cnst
import find_object as fOBJ
from comp_img import compare_image
from detect_text import find_text
from set_light import Set_light
from help import help_cmd, example_cmd
from vbox_logger import logger

############################### Global variables ##############################
debug_flag = False
cmd_queue = []
failed_commands = []
mutex = threading.Lock()

cmd_lookup_table = {
    'FICON': fOBJ.mainly,
    'FTEXT': find_text,
    'COMPIMAGE': compare_image,
    'SETLIGHT': Set_light,
    'HELPME': help_cmd,
    'EXAMPLE': example_cmd
}

########################### Main Program Functions ############################
def main():
    # Get command line args
    command_args = None
    if is_CLI_args_valid(sys.argv):
        command = parser.callFunction(sys.argv[1])
        command_args = command.parse()
        if sys.argv[-1] == cnst.CLI_DEBUG_FLAG_NAME:
            logger.enable_debug_level()
        
        # Do not generate log file on HELP or EXAMPLE commands
        if command_args[0] != 'HELPME' and command_args[0] != 'EXAMPLE':
            logger.preamble_log()
        else:
            logger.close_file()
            os.remove(cnst.DEFAULT_LOG_FILE_NAME)
    else:
        exit()

    # Call corresponding command
    match command_args:
        case ('TESTSTATUS', condition):
            # Start CLI and command-servicing threads
            cli = threading.Thread(target=CLI_handler, args=(condition, ), daemon=True)
            cmd_server = threading.Thread(target=process_command, daemon=False)
            cli.start()
            cmd_server.start()
            cli.join()
        case (None, None):
            logger.error("VB", "Command call Syntax Error")
            return
        case (cmd, arg):
            process_command(cmd, arg)
        case _:
            logger.error("VB", "Unknown Error")
    if len(failed_commands) == 0:
        logger.info("VB", f'\nPASSED')
    else:
        logger.info("VB", f'FAILED lines: {failed_commands}')
# END main()

def CLI_handler(condition: str):
    """ Thread to handle user CLI input """
    end = False
    if condition == 'START':
        print("\nTEST STARTED")
        logger.info("PC", "TESTSTATUS(START)")
        while not end:
            # Get string input from terminal
            input_str = input("[PC] >> ")
            command = parser.callFunction(input_str)
            (cmd, arg) = command.parse()

            # Log received command to log file
            logger.info("PC", f"{cmd}({arg})")
            print(f"[VB] >> ACK {cmd}({arg})")

            # Take image and build tuple to add to queue
            raw_input_image = None
            if cmd == 'FICON' or cmd == 'FTEXT' or cmd == 'COMPIMAGE':
                raw_input_image = inputIMG_init(cnst.DEFAULT_CAM_PORT)
            queue_params = ((cmd, arg), raw_input_image)

            # Append command to queue
            match (cmd, arg):
                case ('TESTSTATUS', 'START'):
                    logger.error("VB", "Can't start new TEST"
                                 "one is already running") 
                case ('TESTSTATUS', 'END'):
                    end = True
                    with mutex:
                        if len(cmd_queue) > 0:
                            logger.info("VB", "Command in queue")
                        print("Waiting on commands to finish processing...")
                        cmd_queue.append(queue_params)
                case (None, None):
                    logger.error("VB", f"Innvalid syntax: {input_str}")
                case _:
                    with mutex:
                        if len(cmd_queue) > 0:
                            logger.info("VB", "Command in queue")
                        cmd_queue.append(queue_params)
    else:
        # TESTSTATUS(END) was called before starting a TEST
        logger.error("Can not end a not started TESTSTATUS")
# END CLI_handler()

def process_command(cmd=None, arg=None):
    """ Thread to handle command processing. It takes commands\
        out of the common cmd_queue """
    def execute_command(cmd, arg, raw_im):
        status = cmd_lookup_table[cmd](arg, raw_im)
        if status is not None:
            failed_commands.append(status)

            
    # Commands were given directly and no concurrency is happening
    if (cmd, arg) != (None, None):
        raw_input_image = None
        if cmd == 'FICON' or cmd == 'FTEXT' or cmd == 'COMPIMAGE':
            raw_input_image = inputIMG_init(cam_port=cnst.DEFAULT_CAM_PORT)
        elif cmd == 'SETLIGHT':
            print("SETLIGHT command must be used inside a TESTSTATUS")
            return
        execute_command(cmd, arg, raw_input_image)
        return

    # TESTSTATUS was started, and cmd_queue is being filled by other thread
    commands_pending = False
    while True:
        with mutex:
            if len(cmd_queue) > 0:
                ((cmd, arg), raw_input_image) = cmd_queue.pop(0)
                commands_pending = True
        
        if commands_pending:
            commands_pending = False
            if (cmd, arg) == ('TESTSTATUS', 'END'):
                break
            else:
                execute_command(cmd, arg, raw_input_image)
# END process_command()
            

def is_CLI_args_valid(args):
    valid = False
    # Powershell takes parentheses differently than command prompt and already 
    # separates input. Hence, correct command will have three values. Concatenate
    # them to treat them equally as cmd prompt
    def match_PS_cmdPrompt_formats():
        command = sys.argv[1]
        command_arg = sys.argv[2]
        sys.argv.clear()
        sys.argv.append(command)
        sys.argv.append(f"{command}({command_arg})")


    match(len(args)):
        case 4:
            match_PS_cmdPrompt_formats()
            if args[3] == cnst.CLI_DEBUG_FLAG_NAME:
                valid = True
                match_PS_cmdPrompt_formats()
            else:
                logger.error("VB", f"Unknown argument {args[3]}")
        case 3:
            # 3rd argument could be Debug flag on cmd_prompt or command ran in powershell
            valid = True
            unknown_arg = args[2]
            if args[2] != cnst.CLI_DEBUG_FLAG_NAME:
                match_PS_cmdPrompt_formats()
            if args[0][:4] == args[1][:4]:
                valid = False
                print(f"Error: Unknown argument {unknown_arg}")
        case 2:
            valid = True
        case _:
            print(f"Error: Provide argument in the form COMMAND(ARG)")
            logger.error("VB", f"Argument is not in the form COMMAND(ARG)")
    return valid
# END is_CLI_args_valid()

def inputIMG_init(cam_port: str):
    """ Read input image """
    if cam_port == "0" or cam_port == "1" or cam_port == "2" or cam_port == "3" or cam_port == "4":
        cam = cv2.VideoCapture(int(cam_port), cv2.CAP_DSHOW)
        time.sleep(1)
        for i in range(0,6):
            _,input_image = cam.read() 
            time.sleep(0.2)
        cv2.waitKey(1)       
        cam.release()
    else:
        input_image = cv2.imread(cam_port)
        assert input_image is not None, "Failed to take picture, check camera port"

    if input_image is None:
        print("ERROR: Can not open camera")
    input_image = cv2.rotate(input_image, rotateCode= cv2.ROTATE_180)
    return input_image
            

if __name__ == '__main__':
    main()