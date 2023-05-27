################# File for handling all important constants ###################

###### General program constants
DEFAULT_CAM_PORT = 1                  # Default USB port for camera

###### FIND OBJECT constants
FOBJ_GRAY_THRESHOLD = 100             # Threshold for input image grayscale (0 - 255)
FOBJ_RESIZE_INPUT_STD = (2400, 2400)  # Standard resize values for input image (x,y)
FOBJ_RESIZE_TEMP_STD = 100            # Template resize (pixels)
FOBJ_MATCH_THRESHOLD = 95             # Acceptance threshold for matching template
FOBJ_ACCEPTANCE_DIFF = 30             # Acceptance difference between found objects
FOBJ_MT_ITERATIONS = 100              # Iterations to apply Match template algorithm

