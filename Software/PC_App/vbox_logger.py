import logging

def logger_init(filename='vbox.log', debug=False):
    logger = logging.getLogger('vbox')
    fh = logging.FileHandler(filename)
    fh_Formatter = logging.Formatter('[%(asctime)s] - %(message)s',
                                     datefmt='%Y-%m-%d-%H-%M-%S')
    fh.setFormatter(fh_Formatter)
    logger.addHandler(fh)
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger