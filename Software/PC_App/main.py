import threading
import sys
import time
import takeFunction as parser
import find_object as fOBJ
import constants as cnst
from vbox_logger import logger

############################### Global variables ##############################
debug_flag = False
cmd_queue = []
mutex = threading.Lock()

########################### Main Program Functions ############################
def main():
    # Get command line args
    command_args = None
    if is_CLI_args_valid(sys.argv):
        command = parser.callFunction(sys.argv[1])
        command_args = command.parse()
        if sys.argv[-1] == cnst.CLI_DEBUG_FLAG_NAME:
            logger.enable_debug_level()
        logger.preamble_log()
    else:
        print("Must specify one command to run")
        exit()

    # Call corresponding command
    match command_args:
        case ('TESTSTATUS', condition):
            # Start CLI and command-servicing threads
            cli = threading.Thread(target=CLI_handler, args=(condition, ))
            cmd_server = threading.Thread(target=process_command, daemon=True)
            cli.start()
            cmd_server.start()
            cli.join()
        case (cmd, arg):
            print(f"Processing command {cmd}({arg})")
            #process_command(cmd, arg)
        case _:
            print("Unknown Error")
            pass
# END main()


def CLI_handler(condition: str):
    """ Thread to handle user CLI input """
    end = False
    if condition == 'START':
        print("\nTEST STARTED")
        while not end:
            # Get string input from terminal
            input_str = input("[PC] >> ")
            command = parser.callFunction(input_str)
            command_args = command.parse()

            # Log received command to log file
            logger.info(f"[PC] {command_args[0]}({command_args[1]})")

            # Append command to queue
            match command_args:
                case ('TESTSTATUS', 'START'):
                    logger.error("Can't start new TEST, one is already running") 
                case ('TESTSTATUS', 'END'):
                    end = True
                case _:
                    with mutex:
                        if len(cmd_queue) > 0:
                            logger.info("[VB] Command in queue")
                        cmd_queue.append(command_args)
    else:
        # TESTSTATUS(END) was called before starting a TEST
        logger.error("Can not end a not started TESTSTATUS")
# END CLI_handler()

def process_command():
    """ Thread to handle command processing. It takes commands\
        out of the common cmd_queue """
    def execute_command(cmd, arg):
        match (cmd, arg):
                case ('FICON', x):
                    time.sleep(7)
                    #log
                case ('FTEXT', x):
                    time.sleep(7)
                    #log
                case ('COMPIMAGE', x):
                    time.sleep(7)
                    #log
                case _:
                    pass
            
    # Commands were given directly and no concurrency is happening
    if (cmd, arg) != (None, None):
        execute_command(cmd, arg)

    # TESTSTATUS was started, and cmd_queue is being filled by other thread
    commands_pending = False
    while True:
        with mutex:
            if len(cmd_queue) > 0:
                (cmd, arg) = cmd_queue.pop(0)
                commands_pending = True
        
        if commands_pending:
            commands_pending = False
            execute_command(cmd, arg)
# END process_command()
            

def is_CLI_args_valid(args):
    """ Checks CLI input args are of valid length taking\
          Powershell and Command Prompt differences into account """
    valid = False
    # Powershell takes parentheses differently as command prompt and already 
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
                # TODO: Log error to log file
                print(f"Error: Unknown argument {args[3]}")
        case 3:
            valid = True
            # 3rd argument could be Debug flag on cmd_prompt or command ran in powershell
            if args[2] != cnst.CLI_DEBUG_FLAG_NAME:
                match_PS_cmdPrompt_formats
        case 2:
            valid = True
        case _:
            # TODO: Log error to log file
            print(f"Error: Provide argument in the form COMMAND(ARG)")
    return valid
            
############################# PROGRAM ENTRY POINT #############################
if __name__ == '__main__':
    main()