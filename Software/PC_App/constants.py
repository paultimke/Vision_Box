################# File for handling all important constants ###################

###### General program constants
DEFAULT_CAM_PORT = 1                  # Default USB port for camera
CONFIG_FILE_NAME = "config.json"      # File name for configuration
CLI_DEBUG_FLAG_NAME = '-verbose'      # CLI argument name to trigger verbose output

###### FIND OBJECT constants
FOBJ_GRAY_THRESHOLD = 100             # Threshold for input image grayscale (0 - 255)
FOBJ_RESIZE_INPUT_STD = (2400, 2400)  # Standard resize values for input image (x,y)
FOBJ_RESIZE_TEMP_STD = 100            # Template resize (pixels)
FOBJ_MATCH_THRESHOLD = 95             # Acceptance threshold for matching template # Used to be 50, TODO: Ask @christian 
FOBJ_ACCEPTANCE_DIFF = 30             # Acceptance difference between found objects
FOBJ_MT_ITERATIONS = 100              # Iterations to apply Match template algorithm

##### COMPARE IMAGE constants
CIMG_IOU_MATCH_THRESHOLD = 0.8
CIMG_TEXT_MATCH_THRESHOLD = 0.9
