import logging
import constants as cnst

def _configure_logger():
    return VBOX_logger()

class VBOX_logger:
    """ Wrapper around python's logging module to add specific features like\
        line number counting """
    
    def __init__(self, filename='vbox.log'):
        self.curr_line_num = 0
        self.debug_flag = False
        self.logger = logging.getLogger('vbox')
        self.fileHandler = logging.FileHandler(filename)
        fh_Formatter = logging.Formatter('%(message)s')
        self.fileHandler.setFormatter(fh_Formatter)
        self.logger.addHandler(self.fileHandler)

        # The flag logging.DEBUG is no longer needed since debug printing
        # is now handled through the self.debug_flag variable
        self.logger.setLevel(logging.INFO)
    
    def preamble_log(self):
        self.logger.info("VISION BOX LOG FILE")
        self.logger.info(f"Vision Box software version {cnst.SOFTWARE_VERSION}")
        self.logger.info("Starting light level: 0")
        self.logger.info(f"Verbose Output enabled: {self.debug_flag}\n")

        TS_PADDING = 21 - len('TIMESTAMP') # TIMESTAMP uses 21 char columns
        self.logger.info(f"TIMESTAMP{' '*TS_PADDING}  #  who  DESCRIPTION")

        fh_Formatter = logging.Formatter('[%(asctime)s]  %(message)s',
                                        datefmt='%Y-%m-%d-%H-%M-%S')
        self.fileHandler.setFormatter(fh_Formatter)
        self.logger.addHandler(self.fileHandler)

    def enable_debug_level(self):
        self.debug_flag = True

    def info(self, who, msg, tag=""):
        if tag == "":
            msg = f"{self.curr_line_num} [{who}] {tag} {msg}"
        else:
            msg = f"{self.curr_line_num} [{who}]  {tag} {msg}" 
        self.logger.info(msg)
        self.curr_line_num += 1

    def debug(self, who, msg, tag=""):
        if self.debug_flag:
            self.info(who, msg, tag)

    def warning(self, who, msg, tag=""):
        msg = f"{self.curr_line_num} [{who}] {tag} WARNING: {msg}"
        self.logger.warning(msg)
        self.curr_line_num += 1

    def error(self, who, msg, tag=""):
        msg = f"{self.curr_line_num} [{who}] {tag} ERROR: {msg}"
        self.logger.error(msg)
        self.curr_line_num += 1

if __name__ == 'vbox_logger':
    logger = _configure_logger()