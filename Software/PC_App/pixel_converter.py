import cv2
import constants as cnst
import imutils

def take_pic(cam_port):
    """ Read input image """
    if cam_port == "0" or cam_port == "1" or cam_port == "2" or cam_port == "3" or cam_port == "4":
        cam = cv2.VideoCapture(cam_port)
        _,input_image = cam.read() 
        cv2.waitKey(1)       
        cam.release()
    else:
        input_image = cv2.imread(cam_port)
        assert input_image is not None, "Failed to take picture, check camera port"
    input_image = cv2.rotate(input_image, rotateCode= cv2.ROTATE_180)
    return input_image

def obj_size(input_img):
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)           # Grayscale image
    blur_gray = cv2.medianBlur(gray, 15)                         # Blur image
    canny = cv2.Canny(blur_gray, 50, 100)                        # Remove noise 

    cnts = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL,    # Find contours
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < 100:   # Contour treshold to avoid noise
            continue
        else: 
            _,_,w,h = cv2.boundingRect(c)

    diameter = ((w+h)/2)
    return diameter

def get_pixels_per_metric():
    input_img = take_pic("Testing/screens/10_coin.png")    #cnst.DEFAULT_CAM_PORT
    diameter = obj_size(input_img)
    return (diameter / cnst.DIAMETER_10_COIN)              #5.410714285714286


