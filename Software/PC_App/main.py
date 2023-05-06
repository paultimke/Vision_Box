# Import Libraries
import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import imutils 
import argparse
import find_object as fOBJ

#------Construct the argument parser and parse the arguments#------#
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cam", default="1",
                help="Camera port select or path to input image")
ap.add_argument("-t", "--template", 
                help="Path to template image")
ap.add_argument("-f", "--function", required=True, choices=['find_object', 'find_text', 'compare_image', 'set_light'],
                help= "Select function to run. (find_object, find_text, compare_image, set_light)")
ap.add_argument("-v", "--visualize", type=bool, default=False,
                help="Flag indicating whether or not to visualize each iteration. (1=True)")
ap.add_argument("-j", "--iterations", type=int, default=100, 
                help= "Iterations to apply Match Template algorithm. Default=100")
ap.add_argument("-g", "--grayscale", type=int, default=100,
                help= "Grayscale treshold for processing input image. Default=100")
ap.add_argument("-a", "--acceptance", type=int, default=84,
                help = "Acceptance treshold for matching template. Default=84")
ap.add_argument("-d", "--debugg", type=bool, default=False,
                help= "Display images and info for debugging purposes")
args = vars(ap.parse_args())

#----------------------MACROS----------------------#
# Camera port
CAM_PORT = args["cam"] 
# Template to compare
TEMPLATE_PATH = args["template"]  
# Enum for choosing function
FUNCTION = args["function"]
# Minimun contour area to search screen (pixels)
MIN_CONTOUR_AREA = 300
# Margin to cut screen edges (pixels)
MARGIN_CUT = 10
# Resize values for input image
XSIZE = 1200
YSIZE = 1600
# Treshold for input image grayscale (0-255)
IMG_TRESHOLD = args["grayscale"]
# Template resize (pixels)
TEMPLATE_SIZE = 80
# Treshold for matching template 
FOUND_TRESHOLD = args["acceptance"]
# Acceptance difference between found objects (pixels)
ACCEPTANCE_DIFF = 20
# Iterations for Match Template
MT_ITERATIONS = args["iterations"]
# Flag indicating if debugg mode
DEBG = args["debugg"]
# Flag indicating if visualize result image
VER = args["visualize"]

#-------------------MAIN FUNCTION-------------------#
def main():  
    if FUNCTION == "find_object":
        fOBJ.mainly(CAM_PORT, TEMPLATE_PATH, IMG_TRESHOLD, MIN_CONTOUR_AREA, MARGIN_CUT, XSIZE, YSIZE,
                                        TEMPLATE_SIZE, MT_ITERATIONS, FOUND_TRESHOLD, ACCEPTANCE_DIFF, DEBG, VER)

if __name__ == "__main__":
    main()