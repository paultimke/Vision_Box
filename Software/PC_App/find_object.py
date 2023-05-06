""" Find shapes inside an input image """
# Import Libraries
import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import imutils 
import logging

#----------------Create and configure logger----------------# 
def logger_init():
    """ Initialice logging message handler to create .log file """
    logging.basicConfig(filename="find_object.log", 
                        encoding='utf-8', 
                        filemode="w") 
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.StreamHandler()
    fh_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger


def inputIMG_init(cam_port: str):
    """ Read input image """
    if cam_port == "0" or cam_port == "1" or cam_port == "2" or cam_port == "3" or cam_port == "4":
        cam = cv2.VideoCapture(cam_port)
        _,input_image = cam.read() 
        cv2.waitKey(1)       
        cam.release()
    else:
        input_image = cv2.imread(cam_port)
        assert input_image is not None, "Failed to take picture, check camera port"
    return input_image


def visualize(img, title:str, figure:int):
    """ Use Matplotlib to show image """
    plt.figure(figure)
    plt.title(title) 
    plt.imshow(img, cmap="gray")
    plt.show()


def template_init(template_path):
    """ Read template image """
    template= cv2.imread(template_path)
    assert template is not None, "File could not be read, check with os.path.exists()"
    return template


def inputIMG_process(input_image, img_treshold, min_contour_area, margin_cut, xsize, ysize):
    """ Binarize input image, find screen contour and crop image,
        then resize to standard MACRO defeined size""" 
    gray_input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(gray_input_image,img_treshold,255,cv2.THRESH_BINARY )

    # Find screen contours and crop input image
    Contours,_ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in Contours:
        if cv2.contourArea(contour) > min_contour_area:
            [X, Y, W, H] = cv2.boundingRect(contour)   
    cropped_input_image = gray_input_image[Y+margin_cut : Y+H-margin_cut, X+margin_cut : X+W-margin_cut]

    # Resize input image
    cropped_input_image = cv2.resize(cropped_input_image, (xsize, ysize))
    return cropped_input_image


def template_process(template, template_size):
    """ Resize template to standard MACRO defined size and apply Canny filter """
    (tH, tW) = template.shape[:2]
    if tH < template_size or tW < template_size:
        cropped_template = template
    while tH > template_size or tW > template_size:
        cropped_template = cv2.resize(template, (round(tH*0.95), round(tW*0.95)))
        (tH, tW) = cropped_template.shape[:2]

    template = cv2.Canny(cropped_template, 50, 150)
    return template
    

def matchTemplate(input_img, template, mt_iterations):
    """ Iterate input image with different sizes to match with template """
    # Template Height and Width
    (tH, tW) = template.shape[:2]

    # Required variables init
    found = None
    foundList = []
    tempList = [0, 0, 0]

    # Loop over the scales of the image
    for scale in np.linspace(0.05, 1.0, mt_iterations)[::-1]:
        # resize the image according to the scale, and keep track of the ratio of the resizing
        resized = imutils.resize(input_img, width = int(input_img.shape[1] * scale))
        relation = input_img.shape[1] / float(resized.shape[1])
        # If Resized image is smaller than template, then break the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        # detect edges in the resized, grayscale image and apply template matching to find template in image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # if we have found a new maximum correlation value, then update bookkeeping variable
        if found is None or maxVal > found[0]:
            tempList = [maxVal,maxLoc,relation]
            foundList.append(tempList)
            found = (maxVal, maxLoc, relation)
    return foundList


def findObjects(foundList, template, display_image, found_treshold, acceptance_diff):
    """ Iterate in list of matched objetcs and filter by correlation value and position """
    # Template Height and Width
    (tH, tW) = template.shape[:2]

    # Variables init
    startX_T = startY_T = endX_T = endY_T = detected_objs = rejected_objects = 0
    detected_list = []
    rejected_list = []
    detected_temp = [0,0,0,0,0]
    failed_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2BGR)
    display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2BGR)

    # Loop to find objects
    for i in foundList:
        (startX, startY) = (int(i[1][0] * i[2]), int(i[1][1] * i[2]))
        (endX, endY) = (int((i[1][0] + tW) * i[2]), int((i[1][1] + tH) * i[2]))

        if i[0] > (found_treshold * 100000):
            if abs(startX-startX_T) > acceptance_diff and abs(startY-startY_T) > acceptance_diff:
                # draw a bounding box around the detected result
                cv2.rectangle(display_image, (startX, startY), (endX, endY), (255, 0, 0), 2)
                detected_temp = [startX, endX, startY, endY, i[0]]
                detected_objs+=1
                detected_list.append(detected_temp)
            startX_T = startX
            startY_T = startY
        else:
            # draw a bounding box around the failed result
            cv2.rectangle(failed_image, (startX, startY), (endX, endY), (255, 0, 0), 2)
            detected_temp = [startX, endX, startY, endY, i[0]]
            rejected_list.append(detected_temp)
            rejected_objects+=1
    return detected_list, detected_objs, display_image, rejected_list, rejected_objects, failed_image

def img_is_color(img):
    """ Helper function for show_image_list. Return if image is colored """
    if len(img.shape) == 3:
        # Check the color channels to see if they're all the same.
        c1, c2, c3 = img[:, : , 0], img[:, :, 1], img[:, :, 2]
        if (c1 == c2).all() and (c2 == c3).all():
            return True
    return False

def show_image_list(list_images, list_titles=None, list_cmaps=None, grid=True, num_cols=2, figsize=(20, 10), title_fontsize=30):
    """ Display images in a single figure """
    assert isinstance(list_images, list)
    assert len(list_images) > 0
    assert isinstance(list_images[0], np.ndarray)
    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), '%d imgs != %d titles' % (len(list_images), len(list_titles))
    if list_cmaps is not None:
        assert isinstance(list_cmaps, list)
        assert len(list_images) == len(list_cmaps), '%d imgs != %d cmaps' % (len(list_images), len(list_cmaps))
    num_images  = len(list_images)
    num_cols    = min(num_images, num_cols)
    num_rows    = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)
    # Create a grid of subplots.
    plt.figure(3)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]
    for i in range(num_images):
        img    = list_images[i]
        title  = list_titles[i] if list_titles is not None else 'Image %d' % (i)
        cmap   = list_cmaps[i] if list_cmaps is not None else (None if img_is_color(img) else 'gray')
        
        list_axes[i].imshow(img, cmap=cmap)
        list_axes[i].set_title(title, fontsize=title_fontsize) 
        list_axes[i].grid(grid)
    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)
    fig.tight_layout()
    #_ = plt.show()

#-------------------MAIN FUNCTION-------------------#
def mainly(cam_port, template_path, img_treshold, min_contour_area, margin_cut, xsize, ysize,
            template_size, mt_iterations, found_treshold, acceptance_diff, debg, ver):  
    logger = logger_init()
    raw_input_image = inputIMG_init(cam_port)
    raw_template = template_init(template_path)

    inputIMG = inputIMG_process(raw_input_image, img_treshold, min_contour_area, margin_cut, xsize, ysize)
    template = template_process(raw_template, template_size)  

    foundList = matchTemplate(inputIMG, template, mt_iterations)
    detected_list, detected_objs, display_image, rejected_list, rejected_objects, failed_image = findObjects(foundList, template, inputIMG, found_treshold, acceptance_diff)
    
    if debg:
        list_images = [raw_template, raw_input_image, template, inputIMG]
        show_image_list(list_images, 
                list_titles=['Raw template', 'Raw image', 'Processed Template', 'Processed image'],
                figsize=(5,5),
                grid=False,
                title_fontsize=8)
        cnt = 1
        for i in range(0,rejected_objects): ###
            logger.debug("Failed object %d coords: X(%d,%d) Y(%d,%d)    Correlation: %d", i+1, 
                        rejected_list[i][0], rejected_list[i][1], rejected_list[i][2], rejected_list[i][3], rejected_list[i][4])   
    
    if detected_objs != 0:
        logger.info("PASSED")
        logger.info("Number of objects detected: %d",detected_objs)
        for i in range(0,detected_objs):
            logger.info("Passed object %d coords: X(%d,%d) Y(%d,%d)    Correlation: %d", i+1, 
                        detected_list[i][0], detected_list[i][1], detected_list[i][2], detected_list[i][3], detected_list[i][4])   
        if ver:  
            visualize(display_image, "Objects found (red square)", 1)
    else:
        logger.warning("FAILED")
        cnt = 1
        for i in foundList:
            acceptance = i[0]
            logger.info("Failed matching object correlation %d: %d", cnt, acceptance) 
            cnt+=1
        if ver:  
            visualize(failed_image, "Objects found (red square)", 2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

