################# File for handling all important constants ###################

###### General program constants
SW_VERSION_MAJOR = 0
SW_VERSION_MINOR = 1
SW_VERSION_REV = 0
PIXELS_PER_METRIC = 5.410714285714286
SOFTWARE_VERSION = f"{SW_VERSION_MAJOR}.{SW_VERSION_MINOR}.{SW_VERSION_REV}"

DEFAULT_CAM_PORT = '1'               # Default USB port for camera
DEFAULT_LOG_FILE_NAME = "vbox.log"    # Default file name for log
OUTPUT_IMAGES_DIR = "output_images"   # Output images directory
CONFIG_FILE_NAME = "config.json"      # File name for configuration
CLI_DEBUG_FLAG_NAME = "-verbose"      # CLI argument name to trigger verbose output

###### FIND OBJECT constants
FOBJ_GRAY_THRESHOLD = 100             # Threshold for input image grayscale (0 - 255)
FOBJ_RESIZE_INPUT_STD = (2400, 2400)  # Standard resize values for input image (x,y)
FOBJ_RESIZE_TEMP_STD = 100            # Template resize (pixels)
FOBJ_MATCH_THRESHOLD = 75             # Acceptance threshold for matching template # Used to be 50, TODO: Ask @christian 
FOBJ_ACCEPTANCE_DIFF = 30             # Acceptance difference between found objects
FOBJ_MT_ITERATIONS = 100              # Iterations to apply Match template algorithm

##### COMPARE IMAGE constants
CIMG_IOU_MATCH_THRESHOLD = 0.65
CIMG_TEXT_MATCH_THRESHOLD = 0.9


##### PIXEL CONVERTER constants
DIAMETER_10_COIN = 28                 # 10 pesos coin diameter is 28 mm 

