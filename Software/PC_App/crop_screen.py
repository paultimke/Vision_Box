import numpy as np
import cv2
import json
import constants as cnst
from typing import Tuple

# Type Alias for Screen Corners
corner_t = Tuple[int, int, int, int]

def __reorderCornerPoints(corners: corner_t) -> corner_t:
    """ Reorder corners clockwise, starting from Top-Left"""
    def order_points(pts):
        Xorder = pts[np.argsort(pts[:, 0]), :]
        left = Xorder[:2, :]
        right = Xorder[2:, :]

        # Order along axes
        (tl, bl) = left[np.argsort(left[:, 1]), :]
        (tr, br) = right[np.argsort(right[:, 1]), :]
        return np.array([tl, tr, br, bl])

    Corners_ = []
    for corner in corners:
        Corners_.append([(corner[0], corner[1])])

    Corners_ = np.reshape(Corners_, (-1, 2))
    # order the points in clockwise order
    ordered_corners = order_points(Corners_)
    return ordered_corners

def __getScreenCorners(img: cv2.Mat) -> corner_t:
    """ Gets the corners of a quadrilateral bounding the screen """
    # convert img to grayscale
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = 255 - processed_img
    # blur image
    processed_img = cv2.GaussianBlur(processed_img, (3,3), 0)
    # do adaptive threshold on gray image
    processed_img = cv2.adaptiveThreshold(
        processed_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 2
    )
    processed_img = 255 - processed_img

    # apply morphology
    kernel = np.ones((5,5), np.uint8)
    rect = cv2.morphologyEx(processed_img, cv2.MORPH_OPEN, kernel)
    rect = cv2.morphologyEx(rect, cv2.MORPH_CLOSE, kernel)
    # thin
    kernel = np.ones((5,5), np.uint8)
    rect = cv2.morphologyEx(rect, cv2.MORPH_ERODE, kernel)

    # get largest contour
    contours = cv2.findContours(rect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        area_thresh = 0
        area = cv2.contourArea(c)
        if area > area_thresh:
            area = area_thresh
            big_contour = c

    # get rotated rectangle from contour
    rot_rect = cv2.minAreaRect(big_contour)
    box = cv2.boxPoints(rot_rect)
    box = np.int0(box)
 
    (tl, tr, br, bl) = __reorderCornerPoints(box)
    return (tl, tr, bl, br)

def StraightenAndCrop(img: cv2.Mat, width: int, height: int) -> cv2.Mat:
    """ Automatically finds screen in an image by looking for the biggest\
        and brightest spot. It then crops it and warps it to make it\
        a straight rectangle """
    # Corner coordinates of the original image
    corners = __getScreenCorners(img)
    input_points = np.float32([corners[0], corners[1], corners[2], corners[3]])

    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(img, matrix, (width, height))
    return img_output

def StraightenAndCrop_Calibrated(img: cv2.Mat, width: int, height: int) -> cv2.Mat:
    # Get corner coordinates from configuration file
    with open(cnst.CONFIG_FILE_NAME, "r") as infile:
        config_data = json.load(infile)
        corners = [
            config_data["screen_corners"]["topL"],
            config_data["screen_corners"]["topR"],
            config_data["screen_corners"]["botL"],
            config_data["screen_corners"]["botR"]
        ]
    
    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    input_points = np.float32([corners[0], corners[1], corners[2], corners[3]])

    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(img, matrix, (width, height))
    return img_output 

if __name__ == '__main__':
    from comp_img import img_show
    img = cv2.imread('Testing/screens_vbox_cam/T03_vbox_cam.png')
    img = cv2.rotate(img, cv2.ROTATE_180)
    ref = cv2.imread('Testing/screens/T03.png')
    img_show([img, ref])

    im1 = StraightenAndCrop(img, ref.shape[1], ref.shape[0])
    #img_show([img, im1, ref])

    im2 = StraightenAndCrop_Calibrated(img, ref.shape[1], ref.shape[0])
    img_show([im1, im2, ref])
    print("hola")