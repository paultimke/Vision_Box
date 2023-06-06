import logging
import os
import cv2
import matplotlib.pyplot as plt
import constants as cnst

def _configure_logger():
    return VBOX_logger()

def configure_img_logger():
    return Image_logger(cnst.OUTPUT_IMAGES_DIR)

def img_show(img_list):
    """ Shows a list of images """
    if len(img_list) == 1:
        plt.imshow(cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB))
    else:
        _, imarr = plt.subplots(1, len(img_list))
        for i in range(len(img_list)):
            imarr[i].imshow(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))

class Image_logger():
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self._ficon_img_counter = 0
        self._ftext_img_counter = 0
        self._comp_img_counter = 0
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)

    def img_save(self, cmd_name: str, img_list):
        #img = img_list[0]
        #img_show([img])
        #img_show(img_list)
        img = cv2.hconcat(img_list)
        #cv2.imshow("img",img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        #img_show(img)

        img_name = "Untitled"
        match cmd_name:
            case 'FICON':
                img_name = f"{cmd_name}_{self._ficon_img_counter}.png"
                self._ficon_img_counter += 1
            case 'FTEXT':
                img_name = f"{cmd_name}_{self._ftext_img_counter}.png"
                self._ftext_img_counter += 1
            case 'COMPIMAGE':
                img_name = f"{cmd_name}_{self._comp_img_counter}.png"
                self._comp_img_counter += 1
            case _:
                pass

        img_path = os.path.join(self.dir_path, img_name)
        cv2.imwrite(img_path, img)


class VBOX_logger:
    """ Wrapper around python's logging module to add specific features like\
        line number counting """
    
    def __init__(self, filename=cnst.DEFAULT_LOG_FILE_NAME):
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

    def close_file(self):
        self.fileHandler.close()
    
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
        if tag == "":
            msg = f"{self.curr_line_num} [{who}] {tag} {msg}"
        else:
            msg = f"{self.curr_line_num} [{who}]  {tag} WARNING: {msg}" 
        self.logger.warning(msg)
        self.curr_line_num += 1

    def error(self, who, msg, tag=""):
        msg = f"{self.curr_line_num} [{who}] {tag} ERROR: {msg}"
        self.logger.error(msg)
        self.curr_line_num += 1

if __name__ == 'vbox_logger':
    logger = _configure_logger()
    img_logger = configure_img_logger()