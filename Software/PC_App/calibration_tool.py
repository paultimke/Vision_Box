import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy as np
import json
import constants as cnst
from typing import List, Dict
import set_light
import pixel_converter as pix

corner_t = List[int]

############################### VARIABLES ################################
# List of reference points
ref_points = []

########################### MAIN PROGRAM BODY ############################
def write_params_json(corners: List[corner_t], pixel_metric) -> None:
    """ Updates config.json to new calibrated screen corners """
    dic = {
        "screen_corners": {
            "topL": corners[0],
            "topR": corners[1],
            "botR": corners[2],
            "botL": corners[3]
        },
        "pixel_metric": pixel_metric
    }

    # Serializing json
    json_obj = json.dumps(dic, indent=4)
    # Writing to file
    with open(cnst.CONFIG_FILE_NAME, "w") as outfile:
        outfile.write(json_obj)


def capture_frame(cam_obj) -> cv2.Mat:
    """ Captures live camera frame """
    #Load the image
    ret, frame = cam_obj.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    return frame

def click_Callback(event, x, y, flags, param):
    """ Callback function on click event to append reference point """
    # if left mouse button was clicked, record (x, y) coordinates 
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_points.append([x,y])

def draw_help_text(frame, n_saved_points):
    """ Draws helpful text messages and visual feedback on screen """
    # Draw help messages at the top of the screen
    (x_start, y_start) = (15, 30)
    COLOR_WHITE_BGR = (255, 255, 255)
    FONT_SCALE = 0.5
    msg = "Left click on the four screen corners in clockwise order\nPress \'s\' to save and quit | Press \'r\' to reset points"
    dy = 30 # Spacing for newlines
    for (i, line) in enumerate(msg.split('\n')):
        y = y_start + i*dy

        img = cv2.putText(frame, line, (x_start, y),
                        cv2.FONT_HERSHEY_SIMPLEX, fontScale=FONT_SCALE,
                        color=COLOR_WHITE_BGR)
        
    # Draw text to count number of recorded points on bottom of frame
    (x_start, y_start) = (x_start, frame.shape[0] - 30) # Get new y based on frame size
    points_msg = f"Recorded points: {n_saved_points}"
    img = cv2.putText(frame, points_msg, (x_start, y_start),
                      cv2.FONT_HERSHEY_SIMPLEX, fontScale=FONT_SCALE,
                      color=COLOR_WHITE_BGR)
    return img

def main():
    # Start pixel-dimensions calibrations
    set_light.Set_light(80, None)
    print("Vision Box Calibration Tool")
    print("Enter a 28mm circle or 10 MXN coin at the center of Vision Box")
    _ = input("Press ENTER when circle is ready and doors are closed")
    pixel_metric = pix.get_pixels_per_metric()
    print(f"Pixels per mm: {pixel_metric}") 
    set_light.Set_light(0, None)

    print("Remove coin and insert device")
    _ = input("Press ENTER when device is ready")

    # load the image, rotate it to face forwards and clone it
    vid = cv2.VideoCapture(cnst.DEFAULT_CAM_PORT)
    image = capture_frame(vid)
    clone = image.copy()

    cv2.namedWindow("Vision Box Calibration Tool")
    cv2.setMouseCallback("Vision Box Calibration Tool", click_Callback)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        image = capture_frame(vid)
        #cv2.imshow("Vision Box Calibration Tool", image)
        key = cv2.waitKey(1) & 0xFF

        # if there are two reference points, then draw polygon to 
        # wait for user feedback
        if len(ref_points) == 4:
            npy_ref_points = np.array(ref_points, np.int32)
            npy_ref_points = npy_ref_points.reshape((-1, 1, 2))
            cv2.polylines(image, [npy_ref_points], 
                          isClosed=True, color=(0,255,0), thickness=2)

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()
            ref_points.clear()

        # if the 'c' key is pressed, break from the loop
        if key == ord("s"):
            if len(ref_points) == 4:
                # Log to terminal
                print("Saved points are: ")
                print(f"Top-Left: {ref_points[0]}")
                print(f"Top-Right: {ref_points[1]}")
                print(f"Bottom-Left: {ref_points[2]}")
                print(f"Bottom-Right: {ref_points[3]})")

                # Modify configuration file
                print("\nUpdated configuration file config.json")

                write_params_json(ref_points, pixel_metric)
            break

        image = draw_help_text(image, len(ref_points))
        cv2.imshow("Vision Box Calibration Tool", image)
    # END while(TRUE)

    # close all open windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()