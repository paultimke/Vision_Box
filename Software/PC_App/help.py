from vbox_logger import logger
import constants as cnst

# Wildcard _ is added as arg althought none is used, as every command must 
# have the same signature for program compatibility
def help_cmd(_, x):
    """ Prints help information to console about command usage """
    PADDING = 2
    MAX_CMD_WIDTH = len("COMPIMAGE(\"path\")") + PADDING

    print(f"Vision Box Software {cnst.SOFTWARE_VERSION}\n")
    print("Usage: vbox [Commands] [Options]\n")

    # Commands
    print("Commands")
    cmd = "TESTSTATUS(cond)" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "where cond can be one of START or END for a\n"
                                      f"{' '*MAX_CMD_WIDTH} multi-command test")
    cmd = "FICON(\"path\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "where path is the path to the image to search")
    cmd = "FTEXT(\"text\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "where text is an ascii string to search")
    cmd = "COMPIMAGE(\"path\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "where path is the path to a reference image to compare")
    cmd = "SETLIGHT(range)" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "where range is an integer range (0-100) to set brightness")
    cmd = "HELPME" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "help information about the usage of commands")
    cmd = "EXAMPLE" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "EXAMPLE print examples of command usages")

    # Options
    print("\nOptions")
    cmd = "-verbose"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "Enable verbose output in log file")
    pass
# END help_cmd()

# Wildcard _ is added as arg althought none is used, as every command must 
# have the same signature for program compatibility
def example_cmd(_, x):
    """ Prints help information to console about command usage """
    PADDING = 2
    MAX_CMD_WIDTH = len("COMPIMAGE(\"path\")") + PADDING

    print(f"Vision Box Software {cnst.SOFTWARE_VERSION}\n")
    print("Usage: vbox [Commands] [Options]\n")

    # Commands
    print("Commands")
    cmd = "TESTSTATUS(cond)" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "TESTSTATUS(START) or TESTSTATUS(END)")
    cmd = "FICON(\"path\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "FICON(\"assets/small_icon.png\")")
    cmd = "FTEXT(\"text\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "FTEXT(\"hello\")")
    cmd = "COMPIMAGE(\"path\")"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "COMPIMAGE(\"Frames/screen_01/png\")")
    cmd = "SETLIGHT(range)" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "SETLIGHT(75) sets light to 75 percent brightness")
    cmd = "HELPME" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "HELPME")
    cmd = "EXAMPLE" 
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "EXAMPLE")

    # Options
    print("\nOptions")
    cmd = "-verbose"
    print(f"{cmd:<{MAX_CMD_WIDTH}}", "TESTSTATUS(START) -verbose")
    pass